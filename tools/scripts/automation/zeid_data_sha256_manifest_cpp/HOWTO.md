# HOWTO — zeid_data_sha256_manifest

Build (Linux/macOS):
```bash
g++ -std=c++17 -O2 -o zeid_data_sha256_manifest zeid_data_sha256_manifest.cpp
```

Build (Windows):
```bat
cl /std:c++17 /O2 zeid_data_sha256_manifest.cpp
```

Run:
```bash
./zeid_data_sha256_manifest --dir ./artifacts --out manifest.csv
```
