package main

import (
  "bufio"
  "encoding/json"
  "flag"
  "fmt"
  "net"
  "os"
  "os/exec"
  "runtime"
  "strings"
  "sync"
  "time"
)

type Record struct {
  IP        string `json:"ip"`
  MAC       string `json:"mac,omitempty"`
  Hostname  string `json:"hostname,omitempty"`
  Reachable *bool  `json:"reachable,omitempty"`
  SeenVia   string `json:"seen_via"`
  Timestamp string `json:"timestamp"`
}

func nowISO() string { return time.Now().UTC().Truncate(time.Second).Format(time.RFC3339) }

func runCmd(name string, args ...string) string {
  cmd := exec.Command(name, args...)
  out, _ := cmd.CombinedOutput()
  return string(out)
}

func parseNeighbors() map[string]*Record {
  recs := map[string]*Record{}
  out := runCmd("ip", "neigh")
  if strings.TrimSpace(out) != "" {
    sc := bufio.NewScanner(strings.NewReader(out))
    for sc.Scan() {
      parts := strings.Fields(sc.Text())
      if len(parts) < 2 { continue }
      ip := parts[0]
      if net.ParseIP(ip) == nil { continue }
      mac := ""
      for i := 0; i < len(parts)-1; i++ {
        if parts[i] == "lladdr" { mac = strings.ToLower(parts[i+1]) }
      }
      recs[ip] = &Record{IP: ip, MAC: mac, SeenVia: "neigh", Timestamp: nowISO()}
    }
    return recs
  }
  out2 := runCmd("arp", "-an")
  sc := bufio.NewScanner(strings.NewReader(out2))
  for sc.Scan() {
    line := sc.Text()
    if strings.Contains(line, "(") && strings.Contains(line, ")") && strings.Contains(line, " at ") {
      i1 := strings.Index(line, "(")
      i2 := strings.Index(line, ")")
      i3 := strings.Index(line, " at ")
      ip := line[i1+1:i2]
      rest := line[i3+4:]
      fields := strings.Fields(rest)
      mac := ""
      if len(fields) > 0 { mac = strings.ToLower(fields[0]) }
      if net.ParseIP(ip) != nil {
        recs[ip] = &Record{IP: ip, MAC: mac, SeenVia: "arp", Timestamp: nowISO()}
      }
    }
  }
  return recs
}

func ipToU32(ip net.IP) uint32 {
  ip = ip.To4()
  return uint32(ip[0])<<24 | uint32(ip[1])<<16 | uint32(ip[2])<<8 | uint32(ip[3])
}
func u32ToIP(u uint32) net.IP {
  return net.IPv4(byte(u>>24), byte(u>>16), byte(u>>8), byte(u))
}
func iterHosts(cidr string) ([]string, error) {
  _, ipnet, err := net.ParseCIDR(cidr)
  if err != nil { return nil, err }
  ones, bits := ipnet.Mask.Size()
  if bits != 32 || ones < 8 || ones > 30 {
    return nil, fmt.Errorf("refusing prefix /%d (use /8..../30)", ones)
  }
  base := ipnet.IP.To4()
  if base == nil { return nil, fmt.Errorf("IPv4 only") }
  baseU := ipToU32(base)
  mask := uint32(0xFFFFFFFF) << (32 - ones)
  network := baseU & mask
  broadcast := network | ^mask
  start := network + 1
  end := broadcast - 1
  count := end - start + 1
  if count > 4096 { return nil, fmt.Errorf("refusing to scan %d hosts; use smaller subnet", count) }

  hosts := make([]string, 0, count)
  for u := start; u <= end; u++ { hosts = append(hosts, u32ToIP(u).String()) }
  return hosts, nil
}

func ping(ip string, timeoutMS int) bool {
  if runtime.GOOS == "windows" {
    return exec.Command("ping","-n","1","-w",fmt.Sprintf("%d",timeoutMS),ip).Run() == nil
  }
  sec := timeoutMS / 1000; if sec < 1 { sec = 1 }
  return exec.Command("ping","-c","1","-W",fmt.Sprintf("%d",sec),ip).Run() == nil
}

func reverseDNS(ip string) string {
  names, err := net.LookupAddr(ip)
  if err != nil || len(names) == 0 { return "" }
  return strings.TrimSuffix(names[0], ".")
}

func main() {
  subnet := flag.String("subnet","", "IPv4 CIDR (required for -active)")
  active := flag.Bool("active", false, "Opt-in ping sweep across subnet")
  dns := flag.Bool("dns", false, "Best-effort reverse DNS")
  outPath := flag.String("out","inventory.jsonl","Output JSONL path")
  timeout := flag.Int("timeout-ms", 750, "Ping timeout ms")
  workers := flag.Int("workers", 64, "Workers")
  flag.Parse()

  records := parseNeighbors()
  reach := map[string]bool{}

  if *active {
    if *subnet == "" { fmt.Fprintln(os.Stderr,"ERROR: -active requires -subnet"); os.Exit(2) }
    hosts, err := iterHosts(*subnet)
    if err != nil { fmt.Fprintln(os.Stderr,"ERROR:",err); os.Exit(2) }

    jobs := make(chan string, len(hosts))
    results := make(chan struct{ip string; ok bool}, len(hosts))

    var wg sync.WaitGroup
    for i:=0;i<*workers;i++ {
      wg.Add(1)
      go func() {
        defer wg.Done()
        for ip := range jobs {
          results <- struct{ip string; ok bool}{ip: ip, ok: ping(ip, *timeout)}
        }
      }()
    }
    for _, ip := range hosts { jobs <- ip }
    close(jobs)
    wg.Wait()
    close(results)

    for r := range results {
      reach[r.ip] = r.ok
      if r.ok {
        if _, ok := records[r.ip]; !ok {
          records[r.ip] = &Record{IP: r.ip, SeenVia: "ping", Timestamp: nowISO()}
        }
      }
    }

    // refresh neighbors after sweep
    post := parseNeighbors()
    for ip, rec := range post {
      if existing, ok := records[ip]; ok {
        if existing.MAC == "" && rec.MAC != "" { existing.MAC = rec.MAC }
        if existing.SeenVia == "ping" { existing.SeenVia = rec.SeenVia }
      } else {
        records[ip] = rec
      }
    }
  }

  if *dns {
    for ip, rec := range records {
      h := reverseDNS(ip)
      if h != "" { rec.Hostname = h }
    }
  }

  ts := nowISO()
  f, err := os.Create(*outPath)
  if err != nil { fmt.Fprintln(os.Stderr,"ERROR:",err); os.Exit(1) }
  defer f.Close()
  w := bufio.NewWriter(f)
  defer w.Flush()

  count := 0
  for ip, rec := range records {
    rec.Timestamp = ts
    if *active {
      if ok, has := reach[ip]; has { rec.Reachable = &ok }
    }
    b, _ := json.Marshal(rec)
    w.WriteString(string(b) + "\n")
    count++
  }
  fmt.Printf("Wrote %d record(s) to %s\n", count, *outPath)
}
