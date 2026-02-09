using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.NetworkInformation;
using System.Text.Json;

public class Record {
  public string ip { get; set; } = "";
  public string? mac { get; set; }
  public string? hostname { get; set; }
  public bool? reachable { get; set; }
  public string seen_via { get; set; } = "";
  public string timestamp { get; set; } = "";
}

public class Program {
  static string NowIso() => DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ");

  static uint IPv4ToU32(string ip) {
    var p = ip.Split('.').Select(int.Parse).ToArray();
    return (uint)((p[0] << 24) | (p[1] << 16) | (p[2] << 8) | p[3]);
  }
  static string U32ToIPv4(uint u) => string.Join(".", new [] { (u>>24)&255, (u>>16)&255, (u>>8)&255, u&255 });

  static IEnumerable<string> IterHosts(string cidr) {
    var parts = cidr.Split('/');
    if (parts.Length != 2) throw new Exception("Invalid CIDR");
    var baseIp = parts[0];
    var prefix = int.Parse(parts[1]);
    if (prefix < 8 || prefix > 30) throw new Exception($"Refusing prefix /{prefix} (use /8..../30)");

    uint baseU = IPv4ToU32(baseIp);
    uint mask = prefix == 0 ? 0u : (uint)(0xFFFFFFFF << (32 - prefix));
    uint network = baseU & mask;
    uint broadcast = network | ~mask;
    uint start = network + 1;
    uint end = broadcast - 1;

    uint count = end - start + 1;
    if (count > 4096) throw new Exception($"Refusing to scan {count} hosts; use a smaller subnet");

    for (uint u = start; u <= end; u++) yield return U32ToIPv4(u);
  }

  static string RunCmd(string file, string args) {
    try {
      var psi = new ProcessStartInfo(file, args) {
        RedirectStandardOutput = true, RedirectStandardError = true,
        UseShellExecute = false, CreateNoWindow = true
      };
      using var p = Process.Start(psi);
      if (p == null) return "";
      var outText = p.StandardOutput.ReadToEnd();
      var errText = p.StandardError.ReadToEnd();
      p.WaitForExit(3000);
      return outText + errText;
    } catch { return ""; }
  }

  static Dictionary<string, (string mac, string via)> ParseArp() {
    var map = new Dictionary<string, (string, string)>();
    var outText = RunCmd("arp", "-a");
    foreach (var line in outText.Split(new[] { "\r\n", "\n" }, StringSplitOptions.RemoveEmptyEntries)) {
      var l = line.Trim();
      if (l.StartsWith("Interface:", StringComparison.OrdinalIgnoreCase)) continue;
      if (l.StartsWith("Internet Address", StringComparison.OrdinalIgnoreCase)) continue;
      var parts = l.Split((char[])null, StringSplitOptions.RemoveEmptyEntries);
      if (parts.Length >= 2 && IPAddress.TryParse(parts[0], out var addr) &&
          addr.AddressFamily == System.Net.Sockets.AddressFamily.InterNetwork) {
        map[parts[0]] = (parts[1].Replace("-", ":").ToLowerInvariant(), "arp");
      }
    }
    return map;
  }

  static bool PingHost(string ip, int timeoutMs) {
    try {
      using var ping = new Ping();
      var reply = ping.Send(ip, timeoutMs);
      return reply != null && reply.Status == IPStatus.Success;
    } catch { return false; }
  }

  public static int Main(string[] args) {
    string subnet = ""; bool active = false; bool dns = false;
    string outFile = "inventory.json"; int timeoutMs = 750;

    for (int i = 0; i < args.Length; i++) {
      if (args[i] == "--subnet" && i+1 < args.Length) subnet = args[++i];
      else if (args[i] == "--active") active = true;
      else if (args[i] == "--dns") dns = true;
      else if (args[i] == "--out" && i+1 < args.Length) outFile = args[++i];
      else if (args[i] == "--timeout-ms" && i+1 < args.Length) timeoutMs = int.Parse(args[++i]);
    }

    var ts = NowIso();
    var records = new Dictionary<string, Record>();
    var reach = new Dictionary<string, bool>();

    foreach (var kv in ParseArp()) {
      records[kv.Key] = new Record{ ip=kv.Key, mac=kv.Value.mac, seen_via=kv.Value.via, timestamp=ts };
    }

    if (active) {
      if (string.IsNullOrWhiteSpace(subnet)) { Console.Error.WriteLine("ERROR: --active requires --subnet"); return 2; }
      foreach (var ip in IterHosts(subnet)) {
        bool ok = PingHost(ip, timeoutMs);
        reach[ip] = ok;
        if (ok && !records.ContainsKey(ip)) records[ip] = new Record{ ip=ip, seen_via="ping", timestamp=ts };
      }
      foreach (var kv in ParseArp()) {
        if (!records.ContainsKey(kv.Key)) records[kv.Key] = new Record{ ip=kv.Key, mac=kv.Value.mac, seen_via=kv.Value.via, timestamp=ts };
        else {
          var r = records[kv.Key];
          if (string.IsNullOrEmpty(r.mac) && !string.IsNullOrEmpty(kv.Value.mac)) r.mac = kv.Value.mac;
          if (r.seen_via == "ping") r.seen_via = kv.Value.via;
          records[kv.Key] = r;
        }
      }
    }

    if (dns) {
      foreach (var ip in records.Keys.ToList()) {
        try {
          var entry = Dns.GetHostEntry(ip);
          if (!string.IsNullOrEmpty(entry.HostName)) records[ip].hostname = entry.HostName;
        } catch {}
      }
    }

    if (active) {
      foreach (var ip in records.Keys.ToList()) if (reach.ContainsKey(ip)) records[ip].reachable = reach[ip];
    }

    var ordered = records.Values.OrderBy(r => r.ip).ToList();
    File.WriteAllText(outFile, JsonSerializer.Serialize(ordered, new JsonSerializerOptions{ WriteIndented=true }));
    Console.WriteLine($"Wrote {ordered.Count} record(s) to {outFile}");
    return 0;
  }
}
