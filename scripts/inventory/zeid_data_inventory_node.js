#!/usr/bin/env node
const { execFileSync } = require("child_process");
const os = require("os");
const fs = require("fs");

function nowIso() { return new Date().toISOString().replace(/\.\d{3}Z$/, "Z"); }
function run(cmd, args) {
  try { return execFileSync(cmd, args, { encoding: "utf8", stdio: ["ignore","pipe","pipe"] }); }
  catch (e) { return (e.stdout || "") + (e.stderr || ""); }
}
function ipv4ToU32(ip) {
  const p = ip.split(".").map(Number);
  if (p.length !== 4 || p.some(n => Number.isNaN(n) || n<0 || n>255)) return null;
  return ((p[0]<<24)>>>0) + (p[1]<<16) + (p[2]<<8) + p[3];
}
function u32ToIpv4(u){ return [(u>>>24)&255,(u>>>16)&255,(u>>>8)&255,u&255].join("."); }
function iterHosts(cidr){
  const [base, prefS] = cidr.split("/"); const pref = Number(prefS);
  if (!base || Number.isNaN(pref)) throw new Error("Invalid CIDR");
  if (pref < 8 || pref > 30) throw new Error(`Refusing prefix /${pref} (use /8..../30)`);
  const baseU = ipv4ToU32(base); if (baseU === null) throw new Error("Invalid IPv4");
  const mask = pref === 0 ? 0 : ((0xFFFFFFFF << (32-pref))>>>0);
  const netw = baseU & mask; const bcast = (netw | (~mask>>>0))>>>0;
  const start = (netw + 1)>>>0; const end = (bcast - 1)>>>0;
  const count = (end - start + 1)>>>0; if (count > 4096) throw new Error(`Refusing to scan ${count} hosts`);
  const hosts = []; for (let u=start; u<=end; u=(u+1)>>>0) hosts.push(u32ToIpv4(u));
  return hosts;
}
function ping(ip, timeoutMs){
  const plat = os.platform();
  if (plat === "win32") {
    const out = run("ping", ["-n","1","-w",String(timeoutMs),ip]);
    return /TTL=/i.test(out);
  } else {
    const sec = Math.max(1, Math.round(timeoutMs/1000));
    const out = run("ping", ["-c","1","-W",String(sec),ip]);
    return /1 received|bytes from/i.test(out);
  }
}
function parseNeighbors(){
  const recs = new Map();
  const plat = os.platform();
  if (plat === "win32") {
    const out = run("arp", ["-a"]);
    out.split(/\r?\n/).forEach(line=>{
      line=line.trim();
      if(!line || line.startsWith("Interface:") || /^Internet Address/i.test(line)) return;
      const parts=line.split(/\s+/);
      if(parts.length>=2 && ipv4ToU32(parts[0])!==null){
        recs.set(parts[0], {ip:parts[0], mac:parts[1].replace(/-/g,":").toLowerCase(), seen_via:"arp"});
      }
    });
  } else {
    const out = run("ip", ["neigh"]);
    if (out.trim()) {
      out.split(/\r?\n/).forEach(line=>{
        const parts=line.trim().split(/\s+/); if(parts.length<2) return;
        const ip=parts[0]; if(ipv4ToU32(ip)===null) return;
        let mac=""; for(let i=0;i<parts.length-1;i++){ if(parts[i]==="lladdr") mac=(parts[i+1]||"").toLowerCase(); }
        recs.set(ip,{ip,mac,seen_via:"neigh"});
      });
    } else {
      const out2 = run("arp", ["-an"]);
      out2.split(/\r?\n/).forEach(line=>{
        const m=line.match(/\((\d+\.\d+\.\d+\.\d+)\)\s+at\s+([0-9a-f:]{17})/i);
        if(m) recs.set(m[1], {ip:m[1], mac:m[2].toLowerCase(), seen_via:"arp"});
      });
    }
  }
  return recs;
}
function reverseDNS(ip){
  const out = run("nslookup", [ip]);
  const m = out.match(/name\s*=\s*([^\s]+)/i) || out.match(/Name:\s*([^\s]+)/i);
  return m ? String(m[1]).replace(/\.$/,"") : "";
}
function parseArgs(argv){
  const a={subnet:"", active:false, dns:false, out:"inventory.jsonl", timeoutMs:750};
  for(let i=2;i<argv.length;i++){
    if(argv[i]==="--subnet") a.subnet=argv[++i]||"";
    else if(argv[i]==="--active") a.active=true;
    else if(argv[i]==="--dns") a.dns=true;
    else if(argv[i]==="--out") a.out=argv[++i]||a.out;
    else if(argv[i]==="--timeout-ms") a.timeoutMs=Number(argv[++i]||"750");
    else throw new Error("Unknown arg: "+argv[i]);
  }
  return a;
}

(function main(){
  const args=parseArgs(process.argv);
  const ts=nowIso();
  const recs=parseNeighbors();
  const reach=new Map();

  if(args.active){
    if(!args.subnet) throw new Error("ERROR: --active requires --subnet (e.g., 192.168.1.0/24)");
    const hosts=iterHosts(args.subnet);
    hosts.forEach(ip=>{
      const ok=ping(ip,args.timeoutMs);
      reach.set(ip,ok);
      if(ok && !recs.has(ip)) recs.set(ip,{ip,mac:"",seen_via:"ping"});
    });
    const post=parseNeighbors();
    post.forEach((v,ip)=>{
      if(!recs.has(ip)) recs.set(ip,v);
      else {
        const r=recs.get(ip);
        if((!r.mac || r.mac==="") && v.mac) r.mac=v.mac;
        if(r.seen_via==="ping") r.seen_via=v.seen_via;
        recs.set(ip,r);
      }
    });
  }

  const lines=[];
  Array.from(recs.keys()).sort().forEach(ip=>{
    const r=recs.get(ip);
    const row={
      ip,
      mac: r.mac || null,
      hostname: null,
      reachable: args.active && reach.has(ip) ? reach.get(ip) : null,
      seen_via: r.seen_via,
      timestamp: ts
    };
    if(args.dns){ const h=reverseDNS(ip); if(h) row.hostname=h; }
    lines.push(JSON.stringify(row));
  });

  fs.writeFileSync(args.out, lines.join("\n")+"\n", "utf8");
  console.log(`Wrote ${lines.length} record(s) to ${args.out}`);
})();
