#!/usr/bin/env ruby
require "open3"
require "time"

def run_cmd(*cmd) Open3.capture2e(*cmd)[0].to_s rescue "" end
def now_iso() Time.now.utc.iso8601 end

def ipv4_to_u32(ip)
  p = ip.split(".").map(&:to_i)
  return nil unless p.length == 4 && p.all? { |n| n.between?(0,255) }
  (p[0] << 24) | (p[1] << 16) | (p[2] << 8) | p[3]
end
def u32_to_ipv4(u) [(u>>24)&255,(u>>16)&255,(u>>8)&255,u&255].join(".") end

def iter_hosts(cidr)
  base, pref_s = cidr.split("/")
  pref = pref_s.to_i
  raise "Invalid CIDR" unless base && pref_s
  raise "Refusing prefix /#{pref} (use /8..../30)" if pref < 8 || pref > 30
  base_u = ipv4_to_u32(base); raise "Invalid IPv4" unless base_u
  mask = pref == 0 ? 0 : ((0xFFFFFFFF << (32 - pref)) & 0xFFFFFFFF)
  netw = base_u & mask; bcast = netw | (~mask & 0xFFFFFFFF)
  start_u = netw + 1; end_u = bcast - 1
  count = end_u - start_u + 1; raise "Refusing to scan #{count} hosts" if count > 4096
  (start_u..end_u).map { |u| u32_to_ipv4(u) }
end

def ping(ip, timeout_ms)
  if RUBY_PLATFORM =~ /mswin|mingw/
    out = run_cmd("ping","-n","1","-w",timeout_ms.to_s,ip)
    out =~ /TTL=/i ? true : false
  else
    sec = [1,(timeout_ms.to_f/1000.0).round].max
    out = run_cmd("ping","-c","1","-W",sec.to_i.to_s,ip)
    out =~ /1 received|bytes from/i ? true : false
  end
end

def parse_neighbors
  recs = {}
  if RUBY_PLATFORM =~ /mswin|mingw/
    out = run_cmd("arp","-a")
    out.each_line do |line|
      line=line.strip
      next if line.empty? || line.start_with?("Interface:") || line =~ /^Internet Address/i
      parts=line.split(/\s+/); next unless parts.length >= 2
      ip=parts[0]; next unless ipv4_to_u32(ip)
      mac=parts[1].gsub("-",":").downcase
      recs[ip]={ip:ip, mac:mac, seen_via:"arp"}
    end
  else
    out = run_cmd("ip","neigh")
    if out.strip != ""
      out.each_line do |line|
        parts=line.strip.split(/\s+/); next if parts.length < 2
        ip=parts[0]; next unless ipv4_to_u32(ip)
        mac=""; parts.each_with_index { |p,i| mac=parts[i+1].downcase if p=="lladdr" && parts[i+1] }
        recs[ip]={ip:ip, mac:mac, seen_via:"neigh"}
      end
    else
      out2=run_cmd("arp","-an")
      out2.each_line do |line|
        m=line.match(/\((\d+\.\d+\.\d+\.\d+)\)\s+at\s+([0-9a-f:]{17})/i)
        next unless m
        recs[m[1]]={ip:m[1], mac:m[2].downcase, seen_via:"arp"}
      end
    end
  end
  recs
end

subnet=""; active=false; out="inventory.csv"
ARGV.each_with_index do |a,i|
  subnet = ARGV[i+1].to_s if a=="--subnet"
  active = true if a=="--active"
  out = ARGV[i+1].to_s if a=="--out"
end

ts=now_iso
records=parse_neighbors
reachable={}

if active
  raise "ERROR: --active requires --subnet" if subnet.strip==""
  iter_hosts(subnet).each do |ip|
    ok=ping(ip,750); reachable[ip]=ok
    records[ip]={ip:ip, mac:"", seen_via:"ping"} if ok && !records.key?(ip)
  end
  parse_neighbors.each do |ip,r|
    if records.key?(ip)
      records[ip][:mac]=r[:mac] if records[ip][:mac].to_s=="" && r[:mac].to_s!=""
      records[ip][:seen_via]=r[:seen_via] if records[ip][:seen_via]=="ping"
    else
      records[ip]=r
    end
  end
end

File.open(out,"w") do |f|
  f.puts "ip,mac,reachable,seen_via,timestamp"
  records.keys.sort.each do |ip|
    r=records[ip]
    reach_s = active && reachable.key?(ip) ? (reachable[ip] ? "1" : "0") : ""
    f.puts "#{ip},#{r[:mac]},#{reach_s},#{r[:seen_via]},#{ts}"
  end
end
puts "Wrote #{records.length} record(s) to #{out}"
