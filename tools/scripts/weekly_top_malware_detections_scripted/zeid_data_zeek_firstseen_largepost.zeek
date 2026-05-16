# zeek-firstseen-largepost.zeek
# Flags: internal host contacts a domain it hasn't seen before, then sends a large POST soon after.
# Requires Zeek http.log (HTTP analyzer).

@load base/frameworks/notice

module ZeidData;

export {
  redef enum Notice::Type += {
    FirstSeenDomain_LargePOST
  };
}

const post_threshold_bytes: count = 200000; # 200 KB (tune)
const window: interval = 15min;

global first_seen: table[addr, string] of time &write_expire=7day;

event http_request(c: connection, method: string, original_URI: string, unescaped_URI: string, version: string)
{
  if ( c$id$orig_h !in Site::local_nets ) return;

  local host = c$id$orig_h;
  local d = c$http?$host ? c$http$host : "";

  if ( d == "" ) return;

  if ( [host, d] !in first_seen ) {
    first_seen[host, d] = network_time();
  }

  if ( method == "POST" && c$http?$request_body_len ) {
    local fs = first_seen[host, d];
    if ( network_time() - fs <= window && c$http$request_body_len >= post_threshold_bytes ) {
      NOTICE([$note=FirstSeenDomain_LargePOST,
              $msg=fmt("First-seen domain with large POST: %s -> %s (%d bytes)", host, d, c$http$request_body_len),
              $conn=c]);
    }
  }
}
