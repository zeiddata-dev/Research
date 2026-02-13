# Zeid Data — Island → ELK Connector (HTTP Push)
_If it happened in the browser and nobody logged it… congrats, it never happened._

This repo packages a simple **Island SIEM push → Logstash HTTP input → Elasticsearch → Kibana** pipeline.

**Why this exists:** you want Island browser activity in ELK without inventing a new religion. Island pushes, Logstash receives, Elasticsearch stores, Kibana makes it pretty.

---

## What you get
- ✅ **docker-compose** for Elasticsearch + Kibana + Logstash
- ✅ Logstash pipeline that:
  - accepts **JSON** over HTTP
  - does basic normalization (light ECS-ish fields)
  - optionally enforces a **shared secret**
  - writes to daily indices: `island-audits-YYYY.MM.dd`
- ✅ Sample events + test scripts
- ✅ Training “screenshots” (mocked) for onboarding humans

---

## Architecture (the 10,000 foot view)
```
Island (SIEM integration)
      |
      |  HTTPS POST (JSON)
      v
Logstash (HTTP input @ :8080)
      |
      |  Bulk/index
      v
Elasticsearch (:9200)  ---> Kibana (:5601)
```

---

## Quickstart (local)
1) Copy env template:
```bash
cp .env.example .env
```

2) Start the stack:
```bash
docker compose up -d
```

3) Post a test event (pretend it came from Island):
```bash
./scripts/post_test_event.sh
```

4) Open Kibana:
- http://localhost:5601

Create a data view for:
- `island-audits-*`

Then hit **Discover** and search `event.module : "island"`.

---

## Configure Island
In Island Admin Console:
- Go to **Settings → Integrations → SIEM**
- Choose a generic HTTP / SIEM push option (wording varies by tenant)
- Set **Server URL** to:
  - `http(s)://<your-logstash-host>:8080/island` (path is optional, we accept any)
- If Island supports an auth token / header, set it to:
  - `Bearer <your secret>` (matches `.env` / Logstash check)

See `HOWTO.md` for the step-by-step + training screenshots.

---

## Security notes (because reality exists)
- **Do not** leave Logstash HTTP input open to the internet.
- Put it behind a load balancer, private network, IP allowlist, mTLS, or at minimum a shared secret.
- Logs are evidence. Treat them like evidence. Chain-of-custody isn’t a vibe.

---

## Troubleshooting
- **No indices?** check Logstash logs:
  ```bash
  docker compose logs -f logstash
  ```
- **Kibana empty?** post a test event first (`./scripts/post_test_event.sh`).
- **Auth drops events?** set `ISLAND_SHARED_SECRET` in `.env` or disable auth in the pipeline.

---

## License
MIT. Use responsibly. Don’t be the reason your auditor develops a twitch.
