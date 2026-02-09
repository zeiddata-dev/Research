<#
Hunt-NewScheduledTasks.ps1
Uses TaskScheduler Operational log for task registration events.

Usage:
  .\Hunt-NewScheduledTasks.ps1 -Days 7
#>

param(
  [int]$Days = 7
)

$since = (Get-Date).AddDays(-$Days)

# Task Scheduler event 106 = "Task registered"
$events = Get-WinEvent -FilterHashtable @{
  LogName   = "Microsoft-Windows-TaskScheduler/Operational"
  Id        = 106
  StartTime = $since
} -ErrorAction SilentlyContinue

function Get-EventData($event, $name) {
  try {
    $xml = [xml]$event.ToXml()
    ($xml.Event.EventData.Data | Where-Object { $_.Name -eq $name } | Select-Object -First 1).'#text'
  } catch { $null }
}

$events |
  ForEach-Object {
    [pscustomobject]@{
      TimeCreated = $_.TimeCreated
      Computer    = $_.MachineName
      TaskName    = Get-EventData $_ "TaskName"
      User        = Get-EventData $_ "UserContext"
    }
  } |
  Sort-Object TimeCreated -Descending |
  Format-Table -AutoSize
