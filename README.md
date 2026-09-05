# AI Agent Security Trust Center

[![Trust Center Verification](https://github.com/AAH20/ai-agent-security-trust-center/actions/workflows/verify.yml/badge.svg)](https://github.com/AAH20/ai-agent-security-trust-center/actions/workflows/verify.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

Open security assurance registry for **AI agents**, **MCP servers**, tools and autonomous workflows. Generate machine-readable profiles, enforce mandatory security gates, publish an AI trust center and export tamper-evident evidence for customers, auditors and GRC systems.

Search topics: AI agent security, MCP security, AI governance, AI compliance, agent identity, agent authorization, prompt injection, NIST AI RMF, ISO 42001, OWASP Agentic Top 10 and continuous assurance.

> **Evidence boundary:** v0.1 validates declared profiles and content hashes. It does not independently certify an agent, replace an auditor or manufacture cryptographic signatures. Public reliance requires reproducible evidence review and an organizational or Sigstore signature.

## The assurance gap

Organizations can scan an AI agent or document an AI policy, but customers still need current answers:

- Who owns the agent and its business purpose?
- Which identity, tools and data can it access?
- Which actions require approval?
- Did adversarial and isolation tests pass?
- Can operators stop, retry and reverse actions safely?
- Which evidence supports each assurance claim?
- Did a release or permission change invalidate prior approval?

This project makes those answers portable and testable.

## Architecture

```text
Agent, MCP and policy inventory
              │
              ▼
     Security test adapters
              │
              ▼
  agent-assurance.json profile
              │
       ┌──────┼──────────┐
       ▼      ▼          ▼
 GitHub gate  Evidence    Static trust
              bundle      center
       │      │          │
       └──────┼──────────┘
              ▼
 Customer, auditor and GRC review
```

## What works in v0.1

- Versioned `agent-assurance.json` schema
- Zero-dependency Python validator and CLI
- Five-dimension weighted assurance score
- Mandatory-gate status override
- Expiry enforcement
- Tamper-evident SHA-256 evidence manifests
- Bundle verification and tamper detection
- Responsive static trust-center generator
- Composite GitHub Action
- Synthetic reference agent and evidence
- NIST, OWASP, ISO and AIUC-1 mapping plan
- Security, assurance, distribution and economics KPIs

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .

agent-trust validate examples/procurement-agent/agent-assurance.json
agent-trust score examples/procurement-agent/agent-assurance.json
agent-trust bundle examples/procurement-agent/agent-assurance.json \
  --evidence examples/procurement-agent/evidence-summary.json \
  --output bundles/example.json
agent-trust verify bundles/example.json \
  --source-dir examples/procurement-agent
agent-trust render examples/procurement-agent/agent-assurance.json \
  --output site/generated/index.html
```

## GitHub Action

```yaml
- uses: AAH20/ai-agent-security-trust-center@v1
  with:
    profile: agent-assurance.json
    evidence: evidence-summary.json
    output: agent-assurance-bundle.json
```

The action validates and bundles. A later release will add approved test adapters and configurable release policies. Do not treat a workflow pass as independent certification.

## Assurance model

| Dimension | Weight | Measures |
|---|---:|---|
| Identity and authorization | 25% | Workload identity, delegation, credential life and effective scopes |
| Tool and data security | 20% | Tool inventory, MCP permissions, classification and data boundaries |
| Adversarial resilience | 20% | Injection, exfiltration, confused-deputy and privilege-escalation tests |
| Operational reliability | 15% | Idempotency, retry safety, kill switch, recovery and rollback |
| Governance evidence | 20% | Ownership, approvals, provenance, exceptions and control mappings |

A numeric score never overrides a mandatory failure.

| Mandatory gate | Failure result |
|---|---|
| Approval enforcement | `RESTRICTED` |
| Cross-tenant isolation | `RESTRICTED` |
| Audit-log completeness | `RESTRICTED` |
| Rollback or safe failure | `RESTRICTED` |

A profile declaring `VERIFIED` becomes `REVIEW_REQUIRED` when any mandatory gate remains untested. Expired profiles become `EXPIRED`.

## Assurance statuses

- `VERIFIED`: current evidence and all mandatory gates pass.
- `REVIEW_REQUIRED`: evidence or mandatory testing remains incomplete, or a material change occurred.
- `RESTRICTED`: a mandatory control failed or policy prohibits release.
- `EXPIRED`: the assurance validity period ended.

## Portfolio integration

The Trust Center acts as the distribution layer rather than duplicating scanners:

| Project | Adapter role |
|---|---|
| GRC Claw | Policy decisions, evidence envelopes and action receipts |
| AgentProof | AI-agent security scans and assurance passports |
| MCP Red Team | Adversarial testing of MCP tools and servers |
| Wazuh/Elastic control plane | Runtime host, finding and response evidence |
| OpenSearch control plane | Enriched findings and executive cyber-risk measures |
| CISO Assistant connector | Assets, evidence, findings and GRC metrics export |
| GRC platform benchmark | Destination capability and unit-economics comparison |

Adapters must preserve source provenance and claim status. A connector cannot upgrade simulated or documented evidence to verified evidence.

## KPIs and unit economics

The public specification is in [docs/KPIS_AND_ECONOMICS.md](docs/KPIS_AND_ECONOMICS.md). Core measures include unauthorized action rate, tool-inventory coverage, evidence freshness, first-pass customer acceptance, cost per continuously assured agent, security-review days avoided and risk-adjusted contribution margin enabled.

## Standards roadmap

See [framework mappings](frameworks/README.md). Crosswalks describe traceability, not certification or universal equivalence.

## Security and responsible use

- Use synthetic or explicitly authorized tenants and targets.
- Never commit credentials or sensitive evidence.
- Minimize public profile data.
- Verify signatures and bundle hashes before reliance.
- Treat profile claims as assertions until evidence is independently reviewed.
- Do not publish exploit details that create material harm.

Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).

## Roadmap

- **v0.2:** MCP manifest discovery, permission diff and release invalidation
- **v0.3:** AgentProof and GRC Claw adapters with provenance preservation
- **v0.4:** Sigstore bundle signing and verification
- **v0.5:** CISO Assistant and OSCAL exports
- **v0.6:** private profiles, customer evidence requests and reviewer decisions
- **v1.0:** independently reproducible test packs and signed public registry

## License

Apache-2.0. Standards names and trademarks belong to their respective owners.
