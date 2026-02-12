<#
zeid_data_service_health.ps1

Checks one or more Windows services and optionally restarts stopped ones.
Outputs CSV + JSON.

Because services have feelings. Mostly about quitting.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string[]]$ServiceName,
    [string]$OutDir = "out",
    [switch]$RestartStopped
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$results = @()

foreach ($name in $ServiceName) {
    try {
        $svc = Get-Service -Name $name -ErrorAction Stop
        $action = "none"
        if ($RestartStopped -and $svc.Status -ne "Running") {
            Restart-Service -Name $name -Force -ErrorAction Stop
            $svc = Get-Service -Name $name
            $action = "restart"
        }
        $startMode = (Get-CimInstance Win32_Service -Filter "Name='$name'").StartMode

        $results += [PSCustomObject]@{
            ServiceName = $name
            Status      = $svc.Status.ToString()
            StartType   = $startMode
            Action      = $action
            TimestampUtc = (Get-Date).ToUniversalTime().ToString("o")
            Ok          = ($svc.Status -eq "Running")
            Error       = $null
        }
    } catch {
        $results += [PSCustomObject]@{
            ServiceName = $name
            Status      = "Unknown"
            StartType   = $null
            Action      = "none"
            TimestampUtc = (Get-Date).ToUniversalTime().ToString("o")
            Ok          = $false
            Error       = $_.Exception.Message
        }
    }
}

$results | ConvertTo-Json -Depth 4 | Out-File -Encoding utf8 -FilePath (Join-Path $OutDir "service_health.json")
$results | Export-Csv -NoTypeInformation -Encoding utf8 -Path (Join-Path $OutDir "service_health.csv")

Write-Host ("Done. Outputs in: {0}" -f (Resolve-Path $OutDir))
