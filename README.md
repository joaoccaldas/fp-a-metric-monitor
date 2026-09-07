# FP&A Continuous Metric Monitor

## Financial Planning & Analysis Monitoring

Automated FP&A metric monitoring with anomaly detection and insight notifications. Designed to help finance teams monitor key metrics such as revenue, gross margin, burn rate, and cash flow.

## Features
- Finance metrics fetching from configurable data sources
- Anomaly detection using configurable thresholds
- AI-assisted insight generation through a server-side model integration
- Flexible notifications (console, Slack, Discord, custom webhooks)

## Technology
Python with the `requests` library for API integrations.

## Status
Active development as a generic FP&A monitoring reference project. Public examples and fixtures must remain synthetic and must not contain employer, client, or personal production data.

Built by João Caldas.

## Validated source modes

Default mode now requires a private JSON file via `METRICS_FILE`. Use `METRICS_MODE=http` with `METRICS_URL` for an HTTPS JSON source, and optional server-side `METRICS_TOKEN`. Required numeric fields: revenue, expenses, gross_margin, burn_rate, accounts_receivable; include an ISO timestamp with timezone. Stale values (48 hours by default, configured by `METRICS_MAX_AGE_HOURS`), invalid numbers and failed sources stop the run.

Synthetic examples require `METRICS_MODE=demo` and are labelled. AI calls require `ENABLE_AI_INSIGHTS=1`; notification delivery requires `ENABLE_NOTIFICATIONS=1`. Keys alone no longer activate external effects. Tests run with `python -m unittest discover -v`.

Commercial gaps: authenticated customer onboarding, connector-specific accounting schemas/currencies, configurable business thresholds, scheduling and deduplication, tenant isolation and operational alerting. This is a validated adapter prototype, not a finished SaaS product.
