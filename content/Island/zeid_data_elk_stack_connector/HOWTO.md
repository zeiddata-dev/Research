# HOWTO — Island → ELK (HTTP Push)
You’re going to do this in three phases:
1) Bring up ELK
2) Verify ingestion with a test event
3) Point Island at your Logstash endpoint

Yes, you still have to do phase 2 even if you “feel like it should work.”

---

## 0) Prereqs
- Docker + Docker Compose
- A place for Island to reach Logstash (VM, k8s, etc.)
- A basic understanding that “open inbound port to the internet” is not a security strategy

---

## 1) Start the stack
```bash
cp .env.example .env
docker compose up -d
```

### Confirm health
```bash
docker compose ps
```

- Elasticsearch: http://localhost:9200
- Kibana: http://localhost:5601
- Logstash HTTP input: http://localhost:8080

---

## 2) Send a test event
```bash
./scripts/post_test_event.sh
```

Expected:
- Logstash returns HTTP 200
- Elasticsearch gets a document
- Kibana shows it

### Kibana check
1. Open Kibana → **Stack Management → Data Views**
2. Create a data view: `island-audits-*`
3. Go to **Discover**
4. Search:
   - `event.module : "island"`

Mock screenshots for training:
- `training/screenshots/03_kibana_discover_mock.png`
- `training/screenshots/04_kibana_dashboard_mock.png`

---

## 3) Configure Island SIEM push
In Island console:
1. Navigate to **Settings → Integrations → SIEM**
2. Set:
   - **Server URL**: `https://YOUR_LOGSTASH_FQDN:8080/island`
   - **Auth Token** (if supported): `Bearer YOUR_SHARED_SECRET`
3. Save / enable

Mock screenshot:
- `training/screenshots/01_island_siem_settings_mock.png`

### Shared secret behavior
If you set `ISLAND_SHARED_SECRET` in `.env`, Logstash will drop events that don’t present:
- `Authorization: Bearer <ISLAND_SHARED_SECRET>`

You can disable the check by setting:
- `ISLAND_SHARED_SECRET=` (blank) in `.env`

---

## 4) Production hardening checklist
- Put Logstash behind:
  - private network ingress, **and**
  - IP allowlist / security group, **and**
  - TLS termination (mTLS if you’re serious)
- Use separate indices or ILM if volume is high
- Add an index template (see `elastic/index-template-island.json`)
- Optional: create a Kibana dashboard + detections

---

## 5) Field mapping + pivots
We preserve vendor payload under:
- `island.*`

And add basic pivots:
- `event.module = island`
- `event.dataset = island.audit`
- `observer.vendor = Island`
- `observer.product = Enterprise Browser`

Use `training/KQL_QUERIES.md` for quick pivots.

---

## 6) Common failures (a.k.a. why you're here)
- **401/403**: auth mismatch → check header format
- **Empty body**: wrong codec or payload not JSON
- **Timestamp weirdness**: map your timestamp field in Logstash `date {}` filter

---

## 7) Next steps
Want this to feel like a real integration?
- ECS mappings
- saved objects export
- detection rules (Elastic Security)
- multi-tenant routing (index-per-tenant)

That’s where Zeid Data lives.
