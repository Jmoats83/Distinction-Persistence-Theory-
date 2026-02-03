# Distinction–Persistence Theory (DPT)
**Joshua D. Moats — Originator**

## What this is
Distinction–Persistence Theory (DPT) is a constraint framework for identifying what remains
*distinguishable* under sustained, legitimate pressure. It does not begin with matter,
fields, or spacetime as primitives. It begins with the minimum conditions required for an
identity to remain identifiable.

This repository cleanly separates:
- **Definitions and axioms** (what is asserted)
- **Derived consequences** (what follows if the axioms hold)
- **Explicit boundaries** (where DPT must connect to established physics to earn literal claims)

---

## 1. Core question
**What keeps working after everything easy, rewarded, explained, or enforced is gone?**

If a structure disappears under legitimate pressure, it is not fundamental.

---

## 2. Primitive objects

### 2.1 Distinction
A distinction is an operational separability: a rule that allows a reference process to tell
“this” from “not-this” across time.

Formally, a distinction is represented by a projector:
\[
\Pi: \mathcal{H} \to \mathcal{H}, \quad \Pi^2 = \Pi, \quad \Pi^\dagger = \Pi
\]
where \(\Pi\) defines an identity sector (the subspace counted as the entity).

### 2.2 Reference bath
A distinction exists only relative to a reference bath \(S_{\text{ref}}\)
(environment, coupling structure, or measurement regime).

DPT treats existence as *relative persistence*, not metaphysical absoluteness.

---

## 3. Canonical axioms

### Axiom I — Identity Existence Condition
An entity \(X\) exists in a reference bath \(S_{\text{ref}}\) iff there exists a projector
\(\Pi\) such that:
\[
\mathcal{P}(\Pi; S_{\text{ref}}) > 0
\]

Interpretation: existence is survival of distinguishability, not a label.

---

### Axiom II — Overhead Optimization Principle
Systems tend toward configurations that minimize a canonical overhead functional
\(\mathcal{O}^\star\). Reconfiguration occurs when:
\[
\mathcal{O}^\star(\Pi') < \mathcal{O}^\star(\Pi)
\]
for an alternative projector \(\Pi'\) that maintains persistence.

Interpretation: stable structure is least distinction effort under constraint.

---

### Axiom III — Congestion–Innovation Limit
As scale or pressure increases, maintaining a distinction requires structural innovation
or collapse:
\[
\text{pressure} \uparrow \; \Rightarrow \; \text{innovation} \; \text{or} \; \mathcal{P}(\Pi) \to 0
\]

Interpretation: growth without new architecture destroys persistence.

---

## 4. Core functionals

### 4.1 Persistence functional \(\mathcal{P}(\Pi)\)
\(\mathcal{P}\) measures how well the identity sector defined by \(\Pi\) remains
distinguishable under legitimate dynamics and coupling.

Minimum requirements:
- \(\mathcal{P}\) decreases under leakage or mixing
- \(\mathcal{P} \to 0\) corresponds to operational indistinguishability

A minimal template:
\[
\mathcal{P}(\Pi) = 1 - L(\Pi)
\]
where \(L(\Pi)\) is a leakage functional induced by dynamics and environment.

---

### 4.2 Canonical overhead functional \(\mathcal{O}^\star(\Pi)\)
\(\mathcal{O}^\star\) measures the cost of maintaining distinguishability, including:
- energetic and entropic cost
- control and stabilization cost
- encoding and compression cost
- fragility under perturbation

If \(\mathcal{O}^\star\) exceeds feasible bounds, reconfiguration is favored.

---

## 5. Derived consequences

1. **Identity is sectoral, not state-based.**  
   Persistence applies to subspaces, avoiding the “no attractors under unitarity” problem.

2. **Stability is variational.**  
   Structures persist when they are cheaper than alternatives that preserve identity.

3. **Scaling enforces architecture.**  
   Large systems require new compression or collapse under congestion.

These consequences follow directly from the axioms and do not require speculative physics.

---

## 6. Explicit boundary to physics
DPT makes literal physical claims only if its objects map into field theory.

Open boundary questions:
- What corresponds to \(\Pi\) in QFT (observable algebras, sectors, effective DOFs)?
- How does \(\mathcal{P}\) relate to decoherence, RG flow, and stability of excitations?
- Can DPT restrict (not merely accommodate) low-energy effective theories?

Until this bridge is formalized, DPT remains a constraint framework with explicit limits.

---

## 7. How to read this repository
1. Read **DPT_CORE.md** (this file)
2. Read the preprint (if present) in `docs/preprint/`
3. Examine the boundary document `QFT_BRIDGE.md`

---

## 8. Status
**State:** Foundational / Active  
This document defines the spine. Tighten definitions, then derive bounds, then build bridges.
