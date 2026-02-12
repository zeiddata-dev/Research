<#
zeid_data_local_admin_audit.ps1

Audits local Administrators group membership + local users.
Exports CSV + JSON.

Because "only IT has admin" is a bedtime story.
#>

[CmdletBinding()]
param([string]$OutDir = "out")

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

function Get-LocalAdmins {
    $group = [ADSI]"WinNT://$env:COMPUTERNAME/Administrators,group"
    $members = @()
    $group.psbase.Invoke("Members") | ForEach-Object {
        $m = $_
        $members += [PSCustomObject]@{
            Name   = $m.GetType().InvokeMember("Name", "GetProperty", $null, $m, $null)
            ADsPath = $m.GetType().InvokeMember("ADsPath", "GetProperty", $null, $m, $null)
        }
    }
    $members
}

function Get-LocalUsersSimple {
    try {
        Get-LocalUser | Select-Object Name,Enabled,LastLogon,PasswordLastSet
    } catch {
        Get-WmiObject -Class Win32_UserAccount -Filter "LocalAccount=True" |
            Select-Object @{n="Name";e={$_.Name}}, @{n="Enabled";e={-not $_.Disabled}}, @{n="LastLogon";e={$null}}, @{n="PasswordLastSet";e={$null}}
    }
}

$admins = Get-LocalAdmins
$users  = Get-LocalUsersSimple

$payload = [PSCustomObject]@{
    ComputerName = $env:COMPUTERNAME
    TimestampUtc = (Get-Date).ToUniversalTime().ToString("o")
    Administrators = $admins
    LocalUsers = $users
}

$payload | ConvertTo-Json -Depth 6 | Out-File -Encoding utf8 -FilePath (Join-Path $OutDir "local_admin_audit.json")
$admins | Export-Csv -NoTypeInformation -Encoding utf8 -Path (Join-Path $OutDir "local_admins.csv")
$users  | Export-Csv -NoTypeInformation -Encoding utf8 -Path (Join-Path $OutDir "local_users.csv")

Write-Host ("Wrote outputs to: {0}" -f (Resolve-Path $OutDir))
