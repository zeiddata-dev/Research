import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.*;

public class zeid_data_inventory_java {
  static String nowIso() { return Instant.now().toString().replaceAll("\\.\\d{3}Z$", "Z"); }

  static long ipv4ToU32(String ip) {
    String[] p = ip.split("\\.");
    if (p.length != 4) throw new IllegalArgumentException("Invalid IPv4");
    long u = 0;
    for (int i=0;i<4;i++) {
      int b = Integer.parseInt(p[i]);
      if (b < 0 || b > 255) throw new IllegalArgumentException("Invalid IPv4");
      u |= ((long)b) << (24 - 8*i);
    }
    return u & 0xFFFFFFFFL;
  }
  static String u32ToIpv4(long u) {
    return String.format("%d.%d.%d.%d", (u>>24)&255,(u>>16)&255,(u>>8)&255,u&255);
  }

  static List<String> iterHosts(String cidr) {
    String[] parts = cidr.split("/");
    if (parts.length != 2) throw new IllegalArgumentException("Invalid CIDR");
    String base = parts[0];
    int prefix = Integer.parseInt(parts[1]);
    if (prefix < 8 || prefix > 30) throw new IllegalArgumentException("Refusing prefix /"+prefix+" (use /8..../30)");
    long baseU = ipv4ToU32(base);
    long mask = prefix == 0 ? 0 : (0xFFFFFFFFL << (32 - prefix)) & 0xFFFFFFFFL;
    long network = baseU & mask;
    long broadcast = network | (~mask & 0xFFFFFFFFL);
    long start = network + 1;
    long end = broadcast - 1;
    long count = end - start + 1;
    if (count > 4096) throw new IllegalArgumentException("Refusing to scan "+count+" hosts; use smaller subnet");
    List<String> hosts = new ArrayList<>();
    for (long u=start; u<=end; u++) hosts.add(u32ToIpv4(u));
    return hosts;
  }

  static String runCmd(String... cmd) {
    try {
      Process p = new ProcessBuilder(cmd).redirectErrorStream(true).start();
      ByteArrayOutputStream baos = new ByteArrayOutputStream();
      try (InputStream is = p.getInputStream()) { is.transferTo(baos); }
      p.waitFor();
      return baos.toString(StandardCharsets.UTF_8);
    } catch (Exception e) { return ""; }
  }

  static Map<String, String> parseArp() {
    Map<String, String> map = new HashMap<>();
    String out = runCmd("arp","-a");
    for (String line : out.split("\\r?\\n")) {
      line = line.trim();
      if (line.isEmpty()) continue;
      if (line.toLowerCase().startsWith("interface:")) continue;
      if (line.toLowerCase().startsWith("internet address")) continue;

      String[] parts = line.split("\\s+");
      if (parts.length >= 2) {
        String ip = parts[0].replace("(", "").replace(")", "");
        try {
          InetAddress addr = InetAddress.getByName(ip);
          if (!(addr instanceof Inet4Address)) continue;
        } catch (Exception e) { continue; }
        String mac = parts[1].replace("-", ":").toLowerCase();
        map.put(ip, mac);
      } else {
        if (line.contains("(") && line.contains(") at ")) {
          int i1 = line.indexOf("("), i2 = line.indexOf(")"), i3 = line.indexOf(") at ");
          if (i1>=0 && i2>i1 && i3>=0) {
            String ip = line.substring(i1+1,i2);
            String rest = line.substring(i3+5);
            String[] f = rest.split("\\s+");
            if (f.length>0) map.put(ip, f[0].toLowerCase());
          }
        }
      }
    }
    return map;
  }

  static boolean reachable(String ip, int timeoutMs) {
    try { return InetAddress.getByName(ip).isReachable(timeoutMs); }
    catch (Exception e) { return false; }
  }

  static String esc(String s) {
    if (s == null) return null;
    return s.replace("\\", "\\\\").replace("\"", "\\\"");
  }

  static String jsonLine(LinkedHashMap<String, Object> obj) {
    StringBuilder sb = new StringBuilder();
    sb.append("{");
    boolean first = true;
    for (var e : obj.entrySet()) {
      if (!first) sb.append(",");
      first = false;
      sb.append("\"").append(esc(e.getKey())).append("\":");
      Object v = e.getValue();
      if (v == null) sb.append("null");
      else if (v instanceof Boolean) sb.append(((Boolean)v) ? "true" : "false");
      else sb.append("\"").append(esc(String.valueOf(v))).append("\"");
    }
    sb.append("}");
    return sb.toString();
  }

  public static void main(String[] args) throws Exception {
    String subnet = ""; boolean active = false; boolean dns = false;
    String outPath = "inventory.jsonl"; int timeoutMs = 750;

    for (int i=0;i<args.length;i++) {
      if (args[i].equals("--subnet") && i+1<args.length) subnet = args[++i];
      else if (args[i].equals("--active")) active = true;
      else if (args[i].equals("--dns")) dns = true;
      else if (args[i].equals("--out") && i+1<args.length) outPath = args[++i];
      else if (args[i].equals("--timeout-ms") && i+1<args.length) timeoutMs = Integer.parseInt(args[++i]);
    }

    String ts = nowIso();
    Map<String, LinkedHashMap<String, Object>> recs = new HashMap<>();
    Map<String, Boolean> reach = new HashMap<>();

    for (var e : parseArp().entrySet()) {
      LinkedHashMap<String, Object> r = new LinkedHashMap<>();
      r.put("ip", e.getKey());
      r.put("mac", e.getValue());
      r.put("hostname", null);
      r.put("reachable", null);
      r.put("seen_via", "arp");
      r.put("timestamp", ts);
      recs.put(e.getKey(), r);
    }

    if (active) {
      if (subnet == null || subnet.isEmpty()) { System.err.println("ERROR: --active requires --subnet"); System.exit(2); }
      for (String ip : iterHosts(subnet)) {
        boolean ok = reachable(ip, timeoutMs);
        reach.put(ip, ok);
        if (ok && !recs.containsKey(ip)) {
          LinkedHashMap<String, Object> r = new LinkedHashMap<>();
          r.put("ip", ip); r.put("mac", null); r.put("hostname", null); r.put("reachable", null);
          r.put("seen_via", "reachable"); r.put("timestamp", ts);
          recs.put(ip, r);
        }
      }
      for (var e : parseArp().entrySet()) {
        if (!recs.containsKey(e.getKey())) {
          LinkedHashMap<String, Object> r = new LinkedHashMap<>();
          r.put("ip", e.getKey()); r.put("mac", e.getValue()); r.put("hostname", null); r.put("reachable", null);
          r.put("seen_via", "arp"); r.put("timestamp", ts);
          recs.put(e.getKey(), r);
        } else {
          var r = recs.get(e.getKey());
          if (r.get("mac") == null || String.valueOf(r.get("mac")).isEmpty()) r.put("mac", e.getValue());
          if ("reachable".equals(r.get("seen_via"))) r.put("seen_via", "arp");
        }
      }
    }

    if (dns) {
      for (String ip : new ArrayList<>(recs.keySet())) {
        try {
          String host = InetAddress.getByName(ip).getCanonicalHostName();
          if (host != null && !host.equals(ip)) recs.get(ip).put("hostname", host);
        } catch (Exception ignored) {}
      }
    }

    if (active) {
      for (String ip : new ArrayList<>(recs.keySet())) {
        if (reach.containsKey(ip)) recs.get(ip).put("reachable", reach.get(ip));
      }
    }

    List<String> ips = new ArrayList<>(recs.keySet());
    Collections.sort(ips);

    try (BufferedWriter w = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(outPath), StandardCharsets.UTF_8))) {
      for (String ip : ips) {
        w.write(jsonLine(recs.get(ip)));
        w.write("\n");
      }
    }
    System.out.println("Wrote " + recs.size() + " record(s) to " + outPath);
  }
}
