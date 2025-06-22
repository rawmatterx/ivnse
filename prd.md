# Product Requirements Document (PRD) — *Intrinsic Value Calculator*

Version 0.9 │ June 2025

---

## 1 · Purpose

Build a **batch‑driven valuation platform** that delivers end‑of‑day (EOD) intrinsic‑value estimates for NSE‑listed equities, consumable via REST API and Streamlit UI. The tool enables retail analysts, research desks, and automated swing‑trading bots to make data‑driven decisions before the next market open.

---

## 2 · Problem Statement

Indian investors lack an open, trustworthy, and reproducible source of intrinsic valuations that updates nightly and surfaces fundamental ratios alongside cash‑flow‑based models. Existing portals either charge hefty fees or rely on opaque black‑box algorithms. Our goal is to democratise fair‑value insights while keeping the stack lightweight and self‑hostable.

---

## 3 · Goals & Success Metrics

| Goal              | KPI                                   | Target                        | Source              |
| ----------------- | ------------------------------------- | ----------------------------- | ------------------- |
| Timely valuations | Symbols processed by **06:00 IST**    | ≥ 99 % of NSE listed equities | Airflow logs        |
| Model quality     | 30‑day MAPE vs consensus target price | ≤ 15 %                        | Back‑test pipeline  |
| Performance       | API P95 latency                       | ≤ 1 s                         | Prometheus          |
| Reliability       | Nightly ETL success rate              | ≥ 98 %                        | Airflow SLA monitor |
| Adoption          | Active API tokens within 90 days      | 100+                          | Auth DB             |

---

## 4 · User Personas

1. **Retail Analyst “Neha”** – Wants quick valuation snapshots with P/E, DCF, dividend yield to publish in Telegram channels.
2. **Algo‑Trader “Vikram”** – Pulls JSON via REST to filter gap‑up candidates by discount‑to‑intrinsic.
3. **Broker Research Desk “IC Broking”** – Needs bulk CSV export each morning for Excel models.
4. **Internal QA/Dev** – Monitors ETL health and valuation drift.

---

## 5 · Key Features (MVP)

| #   | Feature                      | Description                                                                                            | Priority |
| --- | ---------------------------- | ------------------------------------------------------------------------------------------------------ | -------- |
| F‑1 | **Nightly ETL**              | Airflow DAG fetches EOD prices (NSEpy) and fundamentals (Alpha Vantage, Tickertape), stores in DuckDB. | P0       |
| F‑2 | **DCF Service**              | FastAPI micro‑service computes discounted cash‑flow fair value.                                        | P0       |
| F‑3 | **DDM Service**              | FastAPI micro‑service for dividend‑discount valuation.                                                 | P0       |
| F‑4 | **REST & CSV APIs**          | `/v1/dcf/{symbol}`, `/v1/ddm/{symbol}`, and `/v1/bulk?date=YYYY‑MM‑DD&fmt=csv`.                        | P0       |
| F‑5 | **Streamlit UI**             | Web dashboard for single‑symbol lookup with charts, multiples, valuation delta.                        | P0       |
| F‑6 | **Auth & Rate‑limit**        | API tokens (JWT), 1000 req/day free tier.                                                              | P1       |
| F‑7 | **Sector Multiples Overlay** | Compare symbol vs sector P/E, EV/EBITDA.                                                               | P2       |
| F‑8 | **Batch PDF Report**         | Generates branded valuation PDF.                                                                       | P2       |

> P0 = must‑have for first release; P1 = next iteration; P2 = stretch.

---

## 6 · Functional Requirements

1. ETL loads must support **delta updates** and recover gracefully from partial failures.
2. Services read **read‑only DuckDB** mounted locally; no external HTTP calls during request path.
3. API returns **ISO‑8601 JSON**, decimal fields as strings to avoid float rounding.
4. Streamlit must cache previous symbol queries for the session.
5. Bulk CSV endpoint paginates at 10 000 rows to fit broker Excel limits.

---

## 7 · Non‑Functional Requirements

| Category          | Requirement                                                              |
| ----------------- | ------------------------------------------------------------------------ |
| **Availability**  | 99.5 % monthly SLO (see architecture blueprint).                         |
| **Performance**   | ≤ 1 s P95 for single‑symbol endpoint.                                    |
| **Scalability**   | Support 2500 API req/min sustained.                                      |
| **Security**      | OAuth2 token, AES‑256 rest/in‑flight, India data residency.              |
| **Observability** | Prometheus metrics for latency, ETL state; Grafana dashboards; ELK logs. |
| **Compliance**    | SOC24 checklist; nightly S3 snapshots for audit.                         |

---

## 8 · System Design Reference

See **“Core Architecture Blueprint – EOD‑batch”** canvas doc (ID #6857fe77ff508191937b6f70f41011f0) for layer diagram, ETL mermaid, and milestone plan. This PRD inherits that architecture verbatim.

---

## 9 · Milestone & Release Plan

1. **Sprint 0 (Setup, 2 wks)** — Repo skeleton, Docker baseline, provider layer test harness.
2. **Sprint 1 (ETL, 2 wks)** — Nightly DAG live, DuckDB populated for NSE top‑500.
3. **Sprint 2 (DCF svc + API, 2 wks)** — Endpoint `/v1/dcf/{symbol}`, Streamlit reads via REST.
4. **Sprint 3 (DDM svc + Bulk CSV, 2 wks)** — Complete P0 scope, release `v1.0‑beta`.
5. **Sprint 4 (Hardening, 2 wks)** — Auth, rate‑limit, SLA monitors; GA launch.

---

## 10 · Out of Scope

* Real‑time intraday valuations.
* Options/derivatives pricing.
* Multi‑asset classes (crypto, commodities).
* User‑defined custom models (planned Q1 2026).

---

## 11 · Risks & Mitigations

| Risk                            | Impact         | Likelihood | Mitigation                                                  |
| ------------------------------- | -------------- | ---------- | ----------------------------------------------------------- |
| Data vendor API quota changes   | Valuation lag  | Medium     | Keep NSEpy self‑scraper fallback; widen nightly window.     |
| DuckDB corruption on power loss | Service outage | Low        | Nightly S3 snapshots + weekly verify.                       |
| Model drift >15 % MAPE          | Reputational   | Medium     | Schedule quarterly back‑test & parameter tuning.            |
| Alpha Vantage licensing terms   | Legal/Cost     | Low        | Re‑platform to Tickertape Rapid or own scrape if fees rise. |

---

## 12 · Open Questions

* Confirm **dividend data** availability for all NSE tickers via Alpha Vantage — fallback to BSE?
* Legal sign‑off on Tickertape HTML scraping — permissible under ToS?
* Decide on **auth provider** — Firebase vs custom JWT vs Auth0.

---

### End of Document

Approved by: *<pending>*
Prepared by: Roy & Assistant (GPT‑o3)
