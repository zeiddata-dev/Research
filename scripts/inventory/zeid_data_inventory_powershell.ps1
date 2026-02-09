<#
zeid_data_inventory_powershell.ps1
Authorized network inventory helper (Windows).

Passive: Get-NetNeighbor
Opt-in active: Test-Connection across subnet
Optional DNS: reverse lookup
Output: CSV or JSONL
#>

param(
  [string]$Subnet,
  [switch]$Active,
  [switch]$DNS,
  [string]$OutFile = "inventory.jsonl",
  [ValidateSet("csv","jsonl")] [string]$Format = "jsonl",
  [int]$TimeoutMs = 750
)

function Get-TimestampUtc { (Get-Date).ToUniversalTime().ToString("s") + "Z" }

function ConvertTo-UInt32([System.Net.IPAddress]$ip) {
  $b = $ip.GetAddressBytes(); [Array]::Reverse($b); [BitConverter]::ToUInt32($b,0)
}
function ConvertFrom-UInt32([uint32]$u) {
  $b = [BitConverter]::GetBytes($u); [Array]::Reverse($b); [System.Net.IPAddress]::new($b).ToString()
}
function Get-HostsFromCidr([string]$cidr) {
  if (-not $cidr -or ($cidr -notmatch "^(\d+\.){3}\d+\/\d+$")) { throw "Invalid CIDR: $cidr" }
  $parts = $cidr.Split("/")
  $ip = [System.Net.IPAddress]::Parse($parts[0])
  $prefix = [int]$parts[1]
  if ($prefix -lt 8 -or $prefix -gt 30) { throw "Refusing prefix /$prefix (use /8..../30)" }

  $ipU = ConvertTo-UInt32 $ip
  $mask = if ($prefix -eq 0) { [uint32]0 } else { [uint32]([uint64]0xFFFFFFFF -shl (32-$prefix)) }
  $network = $ipU -band $mask
  $broadcast = $network -bor ([uint32](0xFFFFFFFF -bxor $mask))
  $start = $network + 1
  $end = $broadcast - 1
  $count = ($end - $start + 1)
  if ($count -gt 4096) { throw "Refusing to scan $count hosts; use a smaller subnet." }

  $ips = New-Object System.Collections.Generic.List[string]
  for ($u = $start; $u -le $end; $u++) { $ips.Add((ConvertFrom-UInt32 $u)) }
  return $ips
}

$ts = Get-TimestampUtc
$records = @{}
$reachable = @{}

# Passive
try {
  Get-NetNeighbor -AddressFamily IPv4 -ErrorAction Stop |
    Where-Object { $_.State -ne "Incomplete" -and $_.IPAddress } |
    ForEach-Object {
      $ip = $_.IPAddress
      $records[$ip] = [ordered]@{ ip=$ip; mac=$_.LinkLayerAddress; hostname=$null; reachable=$null; seen_via="neighbor"; timestamp=$ts }
    }
} catch {}

# Active opt-in
if ($Active) {
  if (-not $Subnet) { throw "ERROR: -Active requires -Subnet (e.g., 192.168.1.0/24)" }
  $ips = Get-HostsFromCidr $Subnet
  foreach ($ip in $ips) {
    $ok = $false
    try { $ok = Test-Connection -ComputerName $ip -Count 1 -Quiet -TimeoutSeconds ([math]::Max(1,[int]($TimeoutMs/1000))) } catch {}
    $reachable[$ip] = $ok
    if ($ok -and -not $records.ContainsKey($ip)) {
      $records[$ip] = [ordered]@{ ip=$ip; mac=$null; hostname=$null; reachable=$null; seen_via="ping"; timestamp=$ts }
    }
  }
  # refresh neighbor table
  try {
    Get-NetNeighbor -AddressFamily IPv4 -ErrorAction Stop |
      Where-Object { $_.State -ne "Incomplete" -and $_.IPAddress } |
      ForEach-Object {
        $ip = $_.IPAddress
        if (-not $records.ContainsKey($ip)) {
          $records[$ip] = [ordered]@{ ip=$ip; mac=$_.LinkLayerAddress; hostname=$null; reachable=$null; seen_via="neighbor"; timestamp=$ts }
        } else {
          if (-not $records[$ip].mac -and $_.LinkLayerAddress) { $records[$ip].mac = $_.LinkLayerAddress }
          if ($records[$ip].seen_via -eq "ping") { $records[$ip].seen_via = "neighbor" }
        }
      }
  } catch {}
  foreach ($ip in $records.Keys) {
    if ($reachable.ContainsKey($ip)) { $records[$ip].reachable = [bool]$reachable[$ip] }
  }
}

# Optional DNS
if ($DNS) {
  foreach ($ip in $records.Keys) {
    try {
      $h = [System.Net.Dns]::GetHostEntry($ip).HostName
      if ($h) { $records[$ip].hostname = $h }
    } catch {}
  }
}

$rows = $records.Values | Sort-Object ip
if ($Format -eq "jsonl") {
  $rows | ForEach-Object { ($_ | ConvertTo-Json -Compress) } | Set-Content -Path $OutFile -Encoding UTF8
} else {
  $rows | Export-Csv -Path $OutFile -NoTypeInformation -Encoding UTF8
}
Write-Host ("Wrote {0} record(s) to {1}" -f $rows.Count, $OutFile)
