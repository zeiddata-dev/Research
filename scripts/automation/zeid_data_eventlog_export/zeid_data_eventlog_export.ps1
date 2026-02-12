<#
zeid_data_eventlog_export.ps1

Exports Windows event logs for a time window.
Outputs CSV + JSON.

Because debugging without logs is just creative writing.
#>

[CmdletBinding()]
param(
    [ValidateSet("System","Application","Security")]
    [string]$LogName = "System",
    [int]$HoursBack = 24,
    [string]$OutDir = "out"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$start = (Get-Date).AddHours(-1 * $HoursBack)

$events = Get-WinEvent -FilterHashtable @{LogName=$LogName; StartTime=$start} |
    Select-Object TimeCreated, Id, LevelDisplayName, ProviderName, Message

$payload = [PSCustomObject]@{
    ComputerName = $env:COMPUTERNAME
    LogName      = $LogName
    HoursBack    = $HoursBack
    StartTimeUtc = $start.ToUniversalTime().ToString("o")
    ExportedAtUtc = (Get-Date).ToUniversalTime().ToString("o")
    Count        = ($events | Measure-Object).Count
    Events       = $events
}

$stamp = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")

$payload | ConvertTo-Json -Depth 6 | Out-File -Encoding utf8 -FilePath (Join-Path $OutDir "eventlog_${LogName}_${stamp}.json")
$events  | Export-Csv -NoTypeInformation -Encoding utf8 -Path (Join-Path $OutDir "eventlog_${LogName}_${stamp}.csv")

Write-Host ("Exported {0} events from {1} (last {2}h) to: {3}" -f $payload.Count, $LogName, $HoursBack, (Resolve-Path $OutDir))
