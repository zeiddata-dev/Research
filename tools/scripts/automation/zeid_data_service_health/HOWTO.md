# HOWTO — zeid_data_service_health

Check:
```powershell
powershell -ExecutionPolicy Bypass -File .\zeid_data_service_health.ps1 -ServiceName Spooler,w32time -OutDir out
```

Restart if stopped:
```powershell
powershell -ExecutionPolicy Bypass -File .\zeid_data_service_health.ps1 -ServiceName Spooler -RestartStopped -OutDir out
```
