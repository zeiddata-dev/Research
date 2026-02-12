# HOWTO — zeid_data_backup_verify

```bash
python3 zeid_data_backup_verify.py --input backup_targets.txt --max-age-hours 24 --out-dir out
```

Optional min size:
```bash
python3 zeid_data_backup_verify.py --input backup_targets.txt --max-age-hours 24 --min-size-bytes 1048576 --out-dir out
```
