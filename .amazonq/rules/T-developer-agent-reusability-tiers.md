# T‑Developer Agent Reusability Tiers

T‑Developer classifies components based on the number of decision-making units ("brains"), which directly impacts their reusability and structural flexibility. This document defines the tiered classification of agent structures and reusability strategies.

---

## 1. Tier Classification

| Tier | Structure Type    | Brain Count | Reusability | Description                                          |
| ---- | ----------------- | ----------- | ----------- | ---------------------------------------------------- |
| A    | Tool              | 0           | Very High   | No decisions; can be plugged in anywhere             |
| B    | Agent             | 1           | High        | Single decision logic; reusable across many services |
| C    | Mini Team         | 2           | Medium      | Dual-role logic; lightweight composite functionality |
| D    | Full Team         | 3–4         | Low         | Purpose-specific composite structure                 |
| E    | SaaS System Block | 5 or more   | Very Low    | Complex flow, hard to reuse due to fixed structure   |

---

## 2. Reusability Evaluation Factors

| Factor                       | Description                                          |
| ---------------------------- | ---------------------------------------------------- |
| **Number of Brains**         | More decision units = higher dependency and rigidity |
| **I/O Standardization**      | Standardized input/output increases compatibility    |
| **External API/Agent Calls** | High dependency reduces structural flexibility       |
| **Specialization**           | Narrow use case = less likely to be reused           |

---

## 3. Reusability Strategy

* Tiers A–B: Freely composable and cacheable within the platform
* Tier C: Reusable as domain- or purpose-specific packages
* Tiers D–E: Better suited for cloning and refinement rather than direct reuse

---

## 4. Examples

| Name                      | Tier | Description                                                |
| ------------------------- | ---- | ---------------------------------------------------------- |
| GPTCallerTool             | A    | General-purpose text generation tool                       |
| SummarizerAgent           | B    | Single-role text summarizer                                |
| TranslateAndSummarizeTeam | C    | Two-step team for translation and summarization            |
| ReportPlannerTeam         | D    | Fixed team for summarizing, transforming, and storing data |
| GovChatServiceSystem      | E    | Full-scale SaaS system for policy recommendation           |

---

## 5. Usage Scenarios

* **PlannerAgent**: Prioritizes combining Tier A–C components; Tier D+ used only when needed
* **LLM Auto-Composer**: Uses reusability tiers to optimize for cost and performance
* **ClassifierAgent**: Automatically infers and assigns reusability tier in metadata

---

This reusability tier system is a core standard that ensures both scalability and efficiency of the T‑Developer platform.
