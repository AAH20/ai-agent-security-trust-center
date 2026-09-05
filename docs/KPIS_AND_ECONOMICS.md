# AI Agent Assurance KPIs and Unit Economics

## Security release gates

| KPI | Formula | Target |
|---|---|---:|
| Unauthorized action rate | unauthorized actions / attempted actions | 0% |
| Cross-tenant leakage | protected records leaked in adversarial tests | 0 |
| Approval enforcement | blocked unapproved writes / attempted unapproved writes | 100% |
| Critical injection resistance | safely blocked critical attacks / critical attacks | 100% |
| Rollback or safe-failure success | restored or safely contained actions / tested failures | 100% |
| Expired credential rejection | rejected expired credentials / attempts | 100% |
| Tool inventory coverage | discovered authorized tools / independently known tools | ≥98% |
| Audit-log completeness | actions with actor, target, source, policy, decision and result / actions | 100% |

## Assurance quality

| KPI | Formula | Direction |
|---|---|---:|
| Evidence freshness | evidence inside defined validity window / required evidence | Higher |
| Signed evidence coverage | validly signed evidence objects / required evidence | Higher |
| Control-mapping precision | correct mappings / proposed mappings | Higher |
| Control-mapping recall | correct mappings / applicable mappings | Higher |
| First-pass acceptance | packages accepted without rework / reviewed packages | Higher |
| Request turnaround | median customer request to accepted response | Lower |
| Citation coverage | material claims with valid sources / material claims | Higher |
| False-assurance rate | unsupported verified claims / verified claims | Zero |
| Mean time to invalidate | material change to status downgrade | Lower |

## Distribution and product

| KPI | Definition |
|---|---|
| Registered agents | Unique current agent identities |
| Verified MCP servers | Servers with current reproducible evidence and passed gates |
| GitHub Action installations | Active repositories using the action |
| Monthly verifications | Non-duplicate completed verification runs |
| Public/private profiles | Current profiles by visibility |
| Evidence-request conversion | Requests that reach accepted response / requests |
| Community test packs | Reviewed external security-test contributions |
| Integration coverage | Maintained export and evidence-source adapters |

## Customer economics

```text
Annual assurance cost = subscription + onboarding + verification compute
                      + human review + exception handling
                      + integration maintenance

Cost per assured agent = annual assurance cost / active assured agents

Cost per accepted package = assurance operating cost
                          / customer-or-auditor-accepted packages

Capacity value = sustainable hours released × loaded hourly cost

Rework avoided = rejected packages avoided × average rework hours
               × loaded hourly cost

Attributed contribution margin = eligible contract value
                               × realization probability after verified gate closure
                               × automation attribution
                               × contribution margin

Customer ROI = (capacity value + rework avoided
               + attributed contribution margin
               + independently quantified expected-loss reduction
               - annual assurance cost) / annual assurance cost
```

## Revenue attribution rules

Count revenue enablement only when the record identifies a named opportunity, the customer explicitly required assurance, the GRC gate and closure timestamp are documented, revenue activates inside the approved window, Finance approves contribution margin, and the same value is not attributed to another automation.

Publish conservative, base and upside cases. Keep influenced pipeline outside ROI. Never use total contract value where contribution margin is the economic benefit.

## Provider economics

```text
Gross margin per workspace = subscription revenue
                           - verification compute
                           - evidence storage
                           - reviewer labor
                           - support and tenant-specific integration cost

Contribution per agent = agent expansion revenue - marginal assurance cost

CAC payback months = acquisition cost / monthly gross profit from cohort
```

Track verification compute per run, reviewer minutes per accepted profile, support tickets per 100 agents, storage per evidence object, gross retention, agent expansion rate and gross margin. Do not subsidize high-review customers invisibly through a flat unlimited plan.
