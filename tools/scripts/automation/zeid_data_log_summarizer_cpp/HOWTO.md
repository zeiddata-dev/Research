# HOWTO — zeid_data_log_summarizer

Build (Linux/macOS):
```bash
g++ -std=c++17 -O2 -o zeid_data_log_summarizer zeid_data_log_summarizer.cpp
```

Run:
```bash
./zeid_data_log_summarizer --in app.log --out summary.json --tokens ERROR,WARN,INFO
```
