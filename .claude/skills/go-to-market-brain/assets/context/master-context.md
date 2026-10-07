---
title: {{PROJECT}} Go-To-Market Master Context
project: {{PROJECT}}
type: gtm_context_file
purpose: Single source of truth for any AI agent executing {{PROJECT}} go-to-market work.
version: 1.0
last_updated: {{DATE}}
status_notes: {{WHAT_AN_AGENT_MAY_NOT_ASSUME, e.g. pricing undecided, certification in progress, capabilities in build}}
canonical_vocabulary: {{COMMA_SEPARATED_CANONICAL_TERMS}}
---

# {{PROJECT}} Go-To-Market Master Context

This file is the complete, distilled go-to-market for {{PROJECT}}. It exists so that any AI agent can absorb the entire strategy, ICP, positioning, messaging, competitive frame, funnels, and campaign plan in one read, then execute go-to-market work precisely and on-brand without re-deriving anything.

If you are an AI agent, read the next section first. It tells you how to use everything below.

---

## 0. Agent operating instructions

**What this file is.** The consolidated output of {{SOURCE_SUMMARY}}, distilled into one context file. Every section is authoritative unless a status flag says otherwise.

**How to use it.**

1. Before writing any customer-facing copy, load three things from this file: the canonical vocabulary (Section 2), the claim hygiene ledger (Section 4), and the status ledger (Section 3). These govern what you may say and how to name things. They override any instinct or older phrasing you might pattern-match to.
2. Match the audience. {{AUDIENCE_RULE}}
3. Respect the funnel stage. Section 13 gives the buyer mindset, the questions they are asking, and the asset that belongs at each stage. Write to the stage, not past it.
4. Obey the strategic verdicts in Section 9. They are decided. Do not write copy that contradicts them, and do not claim a decided direction as already shipped.
5. Honor the house writing rules in Section 1.

**Hard guardrails, never violate:**

{{HARD_GUARDRAILS_LIST}}

---

## 1. House writing rules

{{MECHANICS_TONE_SPECIFICITY_CLAIM_DISCIPLINE}}

---

## 2. Canonical vocabulary

This naming is used in the product, docs, and API. Mirror it exactly in all copy.

| Term | Rule |
|---|---|
| {{TERM}} | {{RULE}} |

---

## 3. Status ledger

Status flags govern what can be promised. Check this before writing about any capability.
Legend: SHIPPED = live now. PARTIAL = partially shipped. IN BUILD = committed, not yet shipped, mark "coming soon." ROADMAP = vision, not a launch claim.

### {{CAPABILITY_AREA}}
- {{Capability}}: {{FLAG}}.

---

## 4. Claim hygiene ledger

{{FORBIDDEN_CLAIMS_AND_SAFE_FORMS}}

---

## 5. What {{PROJECT}} is

{{PRODUCT_OR_SERVICE_FOUNDATION}}

---

## 6. Feature or capability matrix

{{WHAT_LEADS_MESSAGING_VS_TABLE_STAKES, with the scoring model that produced it}}

---

## 7. Competitive market analysis

{{MARKET_SHAPE_VECTORS_COMPETITOR_SET_WEDGE}}

---

## 8. Ideal customer profile

{{ICP_STAGES_BUYING_COMMITTEE_DESIGN_PARTNERS}}

---

## 9. Strategic verdicts (decided)

{{THE_FORKS_THAT_ARE_SETTLED_AND_WHY}}

---

## 10. Value proposition: {{AUDIENCE_1}}

{{BRAND_PROMISE_POSITIONING_PILLARS_REASONS_TO_BELIEVE}}

---

## 11. Value proposition: {{AUDIENCE_2}}

{{BRAND_PROMISE_POSITIONING_PILLARS_REASONS_TO_BELIEVE}}

---

## 12. Positioning statement

**Category:** {{CATEGORY}}
**Niche:** {{NICHE}}

{{POSITIONING_PARAGRAPH}}

**Differentiation and defensibility.** {{WHY_IT_IS_HARD_TO_COPY}}

**Objection handling, the two that matter most:**
- {{OBJECTION}}: {{ANSWER}}

---

## 13. Customer journey funnels

{{ONE_FUNNEL_PER_AUDIENCE, stage by stage: mindset, assets, KPI, owning function, then the critical success factor, primary blocker, and accelerator}}

---

## 14. Campaign and asset plan

{{THE_CAMPAIGNS, which are the priority, and the asset list under each}}

---

## 15. Quick-reference execution cheatsheet

For fast agent lookups.

- **One-line positioning:** {{...}}
- **Flagship differentiator:** {{...}}
- **Table stake to win:** {{...}}
- **Top-of-funnel hook:** {{...}}
- **Audiences:** {{...}}
- **ICP stages:** {{...}}
- **Proof points on file:** {{the closed set, nothing else is claimable}}
- **Signature reframe:** {{...}}
- **Primary rival:** {{...}}
- **Warm channels:** {{...}}
- **Do not say:** {{...}}
- **Always say it with:** {{mechanics}}

---

*End of {{PROJECT}} GTM master context. This file is the single source of truth. When status changes, update the relevant ledger here first, then let downstream copy follow.*
