# Intrinsic Value Calculator — Sprint Backlog & Task Tracker

*(mirrors PRD v0.9, canvas ID 6857fefa03348191b083c6731986fe73)*

> **Legend**
> • **Status:** ⬜ Todo │ 🔄 In‑Progress │ ✅ Done
> • **Owner:** initials until team roster set
> • **Est:** time in ideal hours (development + code‑review)

---

## Sprint 0 — Repo & CI Bootstrap (2 weeks)

| #    | Task                                                                    | Est | Owner | Status |
| ---- | ----------------------------------------------------------------------- | --- | ----- | ------ |
|  0.1 | Create new mono‑repo `ivc` with `python‑template` (pyproject, Makefile) | 3 h |  AR   | ⬜      |
|  0.2 | Configure GitHub Actions: lint → pytest → build Docker stub             | 4 h |  AR   | ⬜      |
|  0.3 | Import existing `ivnse` provider layer; ensure tests pass               | 3 h |  KP   | ⬜      |
|  0.4 | Draft CODEOWNERS + PR template + pre‑commit hooks                       | 2 h |  AR   | ⬜      |
|  0.5 | Container baseline: multi‑stage Dockerfile (python 3.11‑slim)           | 4 h |  RK   | ⬜      |
|  0.6 | Write initial docs/README quick‑start                                   | 2 h |  AR   | ⬜      |

---

## Sprint 1 — Nightly ETL & DuckDB (2 weeks)

| #    | Task                                                            | Est | Owner | Status |
| ---- | --------------------------------------------------------------- | --- | ----- | ------ |
|  1.1 | Design DuckDB schema: `prices_eod`, `fundamentals`, `dividends` | 5 h |  KP   | ⬜      |
|  1.2 | Implement NSEpy extractor (Δ‑load)                              | 6 h |  KP   | ⬜      |
|  1.3 | Implement Alpha Vantage EOD price backup                        | 4 h |  KP   | ⬜      |
|  1.4 | Fundamentals extractor (Alpha Vantage OVERVIEW)                 | 5 h |  RK   | ⬜      |
|  1.5 | Tickertape scraper for ratios (PE, PB, ROE)                     | 6 h |  RK   | ⬜      |
|  1.6 | Data validation layer (schema + sanity ranges)                  | 6 h |  KP   | ⬜      |
|  1.7 | Airflow DAG `eod_sync.py` (cron 02:00 IST)                      | 8 h |  AR   | ⬜      |
|  1.8 | Snapshot DuckDB to S3 nightly                                   | 3 h |  AR   | ⬜      |
|  1.9 | ETL SLA monitor (Airflow task‑timeout + email)                  | 4 h |  AR   | ⬜      |

---

## Sprint 2 — DCF Micro‑service & REST API (2 weeks)

| #    | Task                                           | Est | Owner | Status |
| ---- | ---------------------------------------------- | --- | ----- | ------ |
|  2.1 | Package `ivnse.models.dcf` into reusable wheel | 4 h |  KP   | ⬜      |
|  2.2 | FastAPI scaffold `/v1/dcf/{symbol}`            | 6 h |  KP   | ⬜      |
|  2.3 | Embed read‑only DuckDB mount in container      | 3 h |  RK   | ⬜      |
|  2.4 | Unit & integration tests (pytest + httpx)      | 6 h |  KP   | ⬜      |
|  2.5 | Prometheus metrics (latency, errors)           | 3 h |  RK   | ⬜      |
|  2.6 | Update CI to build & push `dcf-svc` image      | 2 h |  AR   | ⬜      |

---

## Sprint 3 — DDM Service, Bulk Export & UI Bridge (2 weeks)

| #    | Task                                         | Est | Owner | Status |
| ---- | -------------------------------------------- | --- | ----- | ------ |
|  3.1 | Implement `/v1/ddm/{symbol}` FastAPI service | 6 h |  KP   | ⬜      |
|  3.2 | Extend ETL to store dividend history         | 4 h |  RK   | ⬜      |
|  3.3 | Bulk CSV endpoint `/v1/bulk?date=&fmt=csv`   | 5 h |  KP   | ⬜      |
|  3.4 | Refactor Streamlit to consume REST APIs      | 6 h |  AR   | ⬜      |
|  3.5 | UI caching with `st.cache_data(ttl=1800)`    | 2 h |  AR   | ⬜      |

---

## Sprint 4 — Hardening & GA Launch (2 weeks)

| #    | Task                                      | Est | Owner | Status |
| ---- | ----------------------------------------- | --- | ----- | ------ |
|  4.1 | JWT auth middleware + token issuance CLI  | 6 h |  RK   | ⬜      |
|  4.2 | Rate limiter (1000 req/day IP or token)   | 4 h |  RK   | ⬜      |
|  4.3 | Grafana dashboards (ETL SLA, API latency) | 4 h |  AR   | ⬜      |
|  4.4 | Alertmanager rules (Slack/PagerDuty)      | 3 h |  AR   | ⬜      |
|  4.5 | Load‑test (k6) to 2500 req/min            | 5 h |  KP   | ⬜      |
|  4.6 | Security scan (dependabot + Trivy)        | 3 h |  AR   | ⬜      |
|  4.7 | GA documentation & onboarding guide       | 4 h |  AR   | ⬜      |

---

## Icebox / Future (Q4 2025)

* Sector multiples overlay API & UI charts
* Residual‑Income service
* PDF report generator
* Macro scenario toggles (WACC, GDP growth)

---

### Capacity snapshot

*Sprint capacity assumption:* 3 devs × 40 ideal h/wk × 2 wks = 240 h per sprint.

| Sprint | Planned hours | Capacity | Buffer |
| ------ | ------------- | -------- | ------ |
| 0      | 18 h          | 240 h    | ample  |
| 1      | 49 h          | 240 h    | ample  |
| 2      | 24 h          | 240 h    | ample  |
| 3      | 23 h          | 240 h    | ample  |
| 4      | 29 h          | 240 h    | ample  |

*Buffers allow for unplanned bug‑fixes, code‑reviews, and context‑switch overhead.*
