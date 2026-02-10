<#
Hunt-RansomwarePreEncryptCommands.ps1
Detects common "prep" commands (shadow copy deletion, backup sabotage, log clearing).
Works best with Sysmon Event ID 1 OR Security 4688 with command-line auditing enabled.

Usage:
  .\Hunt-RansomwarePreEncryptCommands.ps1 -Days 7
#>

param(
  [int]$Days = 7
)

$since = (Get-Date).AddDays(-$Days)

$keywords = @(
  "vssadmin delete shadows",
  "wmic shadowcopy delete",
  "wbic shadowcopy delete",
  "wbadmin delete",
  "bcdedit /set",
  "wevtutil cl",
  "cipher /w:",
  "fsutil usn deletejournal",
  "net stop",
  "sc stop",
  "sc delete"
)

function Get-EventFieldValue($event, $fieldName) {
  try {
    $xml = [xml]$event.ToXml()
    ($xml.Event.EventData.Data | Where-Object { $_.Name -eq $fieldName } | Select-Object -First 1).'#text'
  } catch { $null }
}

$results = @()

# Sysmon Process Create
try {
  $sysmon = Get-WinEvent -FilterHashtable @{
    LogName = "Microsoft-Windows-Sysmon/Operational"
    Id      = 1
    StartTime = $since
  } -ErrorAction Stop

  foreach ($e in $sysmon) {
    $cmd = Get-EventFieldValue $e "CommandLine"
    if ([string]::IsNullOrWhiteSpace($cmd)) { continue }

    foreach ($k in $keywords) {
      if ($cmd.ToLower().Contains($k)) {
        $results += [pscustomobject]@{
          TimeCreated = $e.TimeCreated
          Source      = "Sysmon/1"
          Computer    = $e.MachineName
          User        = (Get-EventFieldValue $e "User")
          Image       = (Get-EventFieldValue $e "Image")
          CommandLine = $cmd
          Match       = $k
        }
        break
      }
    }
  }
} catch {}

# Security 4688 (Process Creation)
try {
  $sec = Get-WinEvent -FilterHashtable @{
    LogName = "Security"
    Id      = 4688
    StartTime = $since
  } -ErrorAction Stop

  foreach ($e in $sec) {
    $cmd = Get-EventFieldValue $e "CommandLine"
    if ([string]::IsNullOrWhiteSpace($cmd)) { continue }

    foreach ($k in $keywords) {
      if ($cmd.ToLower().Contains($k)) {
        $results += [pscustomobject]@{
          TimeCreated = $e.TimeCreated
          Source      = "Security/4688"
          Computer    = $e.MachineName
          User        = Get-EventFieldValue $e "SubjectUserName"
          Image       = Get-EventFieldValue $e "NewProcessName"
          CommandLine = $cmd
          Match       = $k
        }
        break
      }
    }
  }
} catch {}

$results |
  Sort-Object TimeCreated -Descending |
  Format-Table -AutoSize TimeCreated, Source, Computer, User, Image, Match

if ($results.Count -eq 0) {
  Write-Host "No matches found in last $Days day(s)."
}
