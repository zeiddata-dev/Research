use std::collections::HashMap;
use std::env;
use std::process::Command;
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Clone, Debug)]
struct Rec {
  ip: String,
  mac: String,
  reachable: Option<bool>,
  seen_via: String,
  timestamp: String,
}

fn now_epoch() -> String {
  SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs().to_string()
}

fn run_cmd(program: &str, args: &[&str]) -> String {
  match Command::new(program).args(args).output() {
    Ok(o) => {
      let mut s = String::new();
      s.push_str(&String::from_utf8_lossy(&o.stdout));
      s.push_str(&String::from_utf8_lossy(&o.stderr));
      s
    }
    Err(_) => String::new(),
  }
}

fn parse_neighbors() -> HashMap<String, (String, String)> {
  let mut out: HashMap<String, (String, String)> = HashMap::new();
  let neigh = run_cmd("ip", &["neigh"]);
  if !neigh.trim().is_empty() {
    for line in neigh.lines() {
      let parts: Vec<&str> = line.split_whitespace().collect();
      if parts.len() < 2 { continue; }
      let ip = parts[0].to_string();
      let mut mac = String::new();
      for i in 0..parts.len() {
        if parts[i] == "lladdr" && i+1 < parts.len() {
          mac = parts[i+1].to_lowercase();
        }
      }
      out.insert(ip, (mac, "neigh".to_string()));
    }
    return out;
  }
  let arp = run_cmd("arp", &["-an"]);
  for line in arp.lines() {
    if let (Some(i1), Some(i2), Some(i3)) = (line.find('('), line.find(')'), line.find(" at ")) {
      let ip = line[i1+1..i2].to_string();
      let rest = &line[i3+4..];
      let fields: Vec<&str> = rest.split_whitespace().collect();
      let mac = if !fields.is_empty() { fields[0].to_lowercase() } else { "".to_string() };
      out.insert(ip, (mac, "arp".to_string()));
    }
  }
  out
}

fn ipv4_to_u32(ip: &str) -> Option<u32> {
  let parts: Vec<&str> = ip.split('.').collect();
  if parts.len() != 4 { return None; }
  let mut v: u32 = 0;
  for (i, p) in parts.iter().enumerate() {
    let b: u32 = p.parse().ok()?;
    if b > 255 { return None; }
    v |= b << (24 - 8*i);
  }
  Some(v)
}

fn u32_to_ipv4(u: u32) -> String {
  format!("{}.{}.{}.{}",
    (u >> 24) & 0xFF,
    (u >> 16) & 0xFF,
    (u >> 8) & 0xFF,
    u & 0xFF
  )
}

fn iter_hosts(cidr: &str) -> Result<Vec<String>, String> {
  let parts: Vec<&str> = cidr.split('/').collect();
  if parts.len() != 2 { return Err("Invalid CIDR".to_string()); }
  let base = ipv4_to_u32(parts[0]).ok_or("Invalid IPv4".to_string())?;
  let prefix: u32 = parts[1].parse().map_err(|_| "Invalid prefix".to_string())?;
  if prefix < 8 || prefix > 30 { return Err(format!("Refusing prefix /{} (use /8..../30)", prefix)); }

  let mask: u32 = if prefix == 0 { 0 } else { (!0u32) << (32 - prefix) };
  let network = base & mask;
  let broadcast = network | (!mask);
  let start = network + 1;
  let end = broadcast - 1;
  let count = end - start + 1;
  if count > 4096 { return Err(format!("Refusing to scan {} hosts; use smaller subnet", count)); }

  let mut hosts = Vec::new();
  let mut u = start;
  while u <= end {
    hosts.push(u32_to_ipv4(u));
    u += 1;
  }
  Ok(hosts)
}

fn ping(ip: &str, timeout_ms: u32) -> bool {
  if cfg!(target_os = "windows") {
    Command::new("ping").args(["-n","1","-w",&timeout_ms.to_string(), ip]).status().map(|s| s.success()).unwrap_or(false)
  } else {
    let sec = std::cmp::max(1, (timeout_ms as f64 / 1000.0).round() as i32);
    Command::new("ping").args(["-c","1","-W",&sec.to_string(), ip]).status().map(|s| s.success()).unwrap_or(false)
  }
}

fn main() {
  let mut subnet = String::new();
  let mut active = false;
  let mut out_path = "inventory.csv".to_string();

  let args: Vec<String> = env::args().collect();
  let mut i = 1;
  while i < args.len() {
    match args[i].as_str() {
      "--subnet" => { subnet = args.get(i+1).cloned().unwrap_or_default(); i += 2; }
      "--active" => { active = true; i += 1; }
      "--out" => { out_path = args.get(i+1).cloned().unwrap_or(out_path.clone()); i += 2; }
      _ => { eprintln!("Unknown arg: {}", args[i]); std::process::exit(2); }
    }
  }

  let ts = now_epoch();
  let mut records: HashMap<String, Rec> = HashMap::new();
  let mut reach: HashMap<String, bool> = HashMap::new();

  for (ip, (mac, via)) in parse_neighbors() {
    records.insert(ip.clone(), Rec{ ip, mac, reachable: None, seen_via: via, timestamp: ts.clone() });
  }

  if active {
    if subnet.is_empty() { eprintln!("ERROR: --active requires --subnet"); std::process::exit(2); }
    let hosts = iter_hosts(&subnet).unwrap_or_else(|e| { eprintln!("ERROR: {}", e); std::process::exit(2); });
    for ip in hosts {
      let ok = ping(&ip, 750);
      reach.insert(ip.clone(), ok);
      if ok && !records.contains_key(&ip) {
        records.insert(ip.clone(), Rec{ ip: ip.clone(), mac: "".to_string(), reachable: None, seen_via: "ping".to_string(), timestamp: ts.clone() });
      }
    }
    for (ip, (mac, via)) in parse_neighbors() {
      if let Some(r) = records.get_mut(&ip) {
        if r.mac.is_empty() && !mac.is_empty() { r.mac = mac; }
        if r.seen_via == "ping" { r.seen_via = via; }
      } else {
        records.insert(ip.clone(), Rec{ ip, mac, reachable: None, seen_via: via, timestamp: ts.clone() });
      }
    }
    for (ip, ok) in reach.iter() {
      if let Some(r) = records.get_mut(ip) { r.reachable = Some(*ok); }
    }
  }

  let mut keys: Vec<String> = records.keys().cloned().collect();
  keys.sort();

  let mut out = String::new();
  out.push_str("ip,mac,reachable,seen_via,timestamp\n");
  for ip in keys {
    let r = records.get(&ip).unwrap();
    let reach_s = match r.reachable { Some(true) => "1", Some(false) => "0", None => "" };
    out.push_str(&format!("{},{},{},{},{}\n", r.ip, r.mac, reach_s, r.seen_via, r.timestamp));
  }

  std::fs::write(&out_path, out).expect("write failed");
  println!("Wrote {} record(s) to {}", records.len(), out_path);
}
