# Reconstructable Singularity and the Minimum Continuity-Resolving Perspective Set

Status: research formalism v0.1  
Scope: continuity reconstruction, admissibility matrices, and distributed observation

## 1. Purpose

This document formalizes the point at which a connected set of observational frameworks contains enough affirmative and exclusionary evidence to reconstruct one continuity-consistent state-transition history.

The model begins with four commitments:

1. Every realized outcome is a state change. Evaluation, `ALLOW`, `DENY`, `ESCALATE`, and an inadmissible execution are all transitions.
2. Between two adjacent realized states, one cost-bearing transition occurred and produced the resulting state.
3. Apparent multiplicity concerns unresolved observation or reconstruction across missing states; it does not establish that several actual transitions occurred between the same adjacent realized states.
4. Regions that disagree or exclude possibilities are not automatically defects. They can be necessary evidence of what cannot occupy a given region of the admissibility matrix.

## 2. State-transition continuity

Let a realized trajectory be

\[
\gamma=(S_0,T_0,C_0,S_1,\ldots,T_{m-1},C_{m-1},S_m),
\]

where:

- \(S_j\) is a realized state;
- \(T_j\) is the transition from \(S_j\) to \(S_{j+1}\);
- \(C_j\) is the incurred transition cost, including any relevant entropy, information, authority, or recoverability cost.

For adjacent realized states:

\[
S_j \xrightarrow{T_j,C_j} S_{j+1}.
\]

Continuity is the observable relation that preserves attribution between the prior state, the cost-bearing transition, and the resulting state. It does not certify that the transition was admissible.

## 3. Admissibility matrix

Let \(\Gamma\) be the set of candidate histories representable within the observational framework. Let

\[
\Gamma_A\subseteq\Gamma
\]

be the histories consistent with the complete state-transition admissibility matrix, including:

- required relations;
- permitted relations;
- forbidden relations;
- excluded regions;
- authority and policy conditions;
- transition-cost constraints;
- continuity constraints.

An actual transition may produce a state classified as inadmissible. That classification is itself part of the realized continuity path. Inadmissibility does not erase the transition or make it discontinuous.

## 4. Distributed observational frameworks

Let the connected observing entities be

\[
\mathcal E=\{1,2,\ldots,n\}.
\]

Each entity \(i\) contributes an observational framework \(O_i\). Its evidence may be decomposed as

\[
O_i=O_i^{+}\cup O_i^{-},
\]

where:

- \(O_i^{+}\) records what is observed, required, or positively supported;
- \(O_i^{-}\) records what is excluded or cannot occupy the observer's region.

The exclusionary portion is first-class evidence. It constrains the candidate-history space rather than being discarded as disagreement or noise.

For an observer subset \(I\subseteq\mathcal E\), define the surviving continuity histories:

\[
\mathcal C_A(I)
=
\left\{
\gamma\in\Gamma_A:
\gamma\models O_i
\text{ for every }i\in I
\right\}.
\]

Equivalently, using positive and negative evidence:

\[
\mathcal C_A(I)
=
\Gamma_A
\cap
\bigcap_{i\in I}O_i^{+}
\cap
\bigcap_{i\in I}\neg O_i^{-}.
\]

## 5. Reconstructable singularity

A reconstructable singularity is reached for observer subset \(I\) when the combined evidence leaves exactly one admissibility-consistent continuity history:

\[
\left|\mathcal C_A(I)\right|=1.
\]

The singularity is therefore not a physical collapse of many histories into one. It is the point at which the unresolved reconstruction space collapses, within the observational framework, to the one history consistent with all retained affirmative and exclusionary evidence.

## 6. Minimum perspective threshold

The minimum number of perspectives needed to construct the singularity is

\[
\boxed{
 k_A^{*}
 =
 \min_{I\subseteq\mathcal E}
 \left\{
 |I|:
 \left|\mathcal C_A(I)\right|=1
 \right\}
}
\]

The corresponding minimum observer set is

\[
\boxed{
 I_A^{*}
 \in
 \operatorname*{arg\,min}_{I\subseteq\mathcal E}
 \left\{
 |I|:
 \left|\mathcal C_A(I)\right|=1
 \right\}.
}
\]

Here:

- \(k_A^{*}\) is the threshold cardinality;
- \(I_A^{*}\) is a minimum continuity-resolving perspective set.

The minimum is structural, not merely numerical. Several observers may repeat the same information and add no resolving power, while one differently situated observer may exclude an entire unresolved region.

## 7. Injectivity formulation

Let each observer have a trajectory-observation map

\[
g_i:\Gamma_A\rightarrow\mathcal Y_i.
\]

For observer subset \(I\), define the combined map

\[
G_I(\gamma)=\big(g_i(\gamma)\big)_{i\in I}.
\]

The continuity-reconstruction threshold is equivalently

\[
\boxed{
 k_{\Gamma}^{*}
 =
 \min_{I\subseteq\mathcal E}
 \left\{
 |I|:
 G_I\text{ is injective on }\Gamma_A
 \right\}.
}
\]

Expanded:

\[
\boxed{
 k_{\Gamma}^{*}
 =
 \min_{I\subseteq\mathcal E}
 \left\{
 |I|:
 \forall\gamma,\gamma'\in\Gamma_A,
 G_I(\gamma)=G_I(\gamma')
 \Rightarrow
 \gamma=\gamma'
 \right\}.
}
\]

Injectivity means that no two distinct admissibility-consistent histories remain observationally indistinguishable under the selected perspective set.

## 8. Pairwise resolving and hitting-set formulation

For each distinct pair \(\gamma,\gamma'\in\Gamma_A\), define the observers capable of distinguishing them:

\[
D_{\gamma,\gamma'}
=
\left\{
 i\in\mathcal E:
 g_i(\gamma)\neq g_i(\gamma')
\right\}.
\]

A resolving perspective set must intersect every such distinguishing set:

\[
I\cap D_{\gamma,\gamma'}\neq\varnothing
\qquad
\forall\gamma\neq\gamma'.
\]

Therefore:

\[
\boxed{
 k_{\Gamma}^{*}
 =
 \min_{I\subseteq\mathcal E}|I|
 \quad\text{subject to}\quad
 I\cap D_{\gamma,\gamma'}\neq\varnothing
 \ \forall\gamma\neq\gamma'.
}
\]

This exposes the formal relationship to minimum resolving sets, observability, identifiability, and minimum hitting-set problems.

## 9. State-level observability

If the object being reconstructed is a complete state \(x\in\mathcal X_A\), and observer \(i\) has observation map

\[
h_i:\mathcal X_A\rightarrow\mathcal Y_i,
\]

then

\[
H_I(x)=\big(h_i(x)\big)_{i\in I}.
\]

The minimum state-observation threshold is

\[
\boxed{
 k_{\mathrm{obs}}^{*}
 =
 \min_{I\subseteq\mathcal E}
 \left\{
 |I|:
 H_I|_{\mathcal X_A}\text{ is injective}
 \right\}.
}
\]

This is weaker than complete trajectory reconstruction unless the observed state retains enough continuity structure to recover the full path.

## 10. Adjacent and nonadjacent observations

For adjacent realized states \(S_j\) and \(S_{j+1}\), the continuity relation concerns the one transition that occurred:

\[
S_j \xrightarrow{T_j,C_j} S_{j+1}.
\]

For separated observations \(S_a\) and \(S_b\), with \(b>a+1\), the observer may initially retain a constrained set of possible intermediate reconstructions:

\[
S_a\rightarrow S_{a+1}\rightarrow\cdots\rightarrow S_b.
\]

The multiplicity lies in the observer's unresolved reconstruction of omitted intermediate states. Each adjacent step in the realized path still has one transition, one incurred cost, and one resulting state.

## 11. Disagreement and exclusionary regions

Two perspectives need not agree in order to contribute to reconstruction. Their relationship may be:

- **affirmatively complementary**: each observes a different required part of the same history;
- **exclusionarily complementary**: one identifies what is present while another establishes what cannot be present;
- **resolution-different**: both describe the same continuity relation at different granularity;
- **coordinate-different**: both describe the same relation through different observational variables;
- **genuinely contradictory**: they make mutually exclusive claims under the same coordinates, time, definitions, and resolution.

Only the last category necessarily indicates a defect requiring reconciliation. Exclusionary regions maintain the complete admissibility matrix because reconstruction requires knowledge of both what can and what cannot occupy each region.

## 12. Determinism and observational uncertainty

This formalism does not require stochastic state transitions.

An observer may possess a maximally resolved description of the initial state available within its framework and still lack knowledge of the outcome before observing the transition. That epistemic limitation does not imply that several successor states were ontically selected.

Once adjacent realized states are observed, the continuity record concerns the transition that occurred, its cost, and its result. Apparent branching is a representation of unresolved observation, counterfactual analysis, or missing intermediate states—not evidence that multiple realized transitions connected the same adjacent states.

## 13. Provisional terminology

The following terms are introduced provisionally:

- **minimum continuity-resolving perspective set**: a smallest observer subset \(I_A^{*}\) whose evidence uniquely reconstructs the admissibility-consistent continuity history;
- **continuity-reconstruction dimension**:

\[
\operatorname{crdim}(\Gamma_A)=k_{\Gamma}^{*};
\]

- **collective reconstructable singularity**: the singleton reconstruction condition achieved by a connected set of perspectives, even when no individual perspective is independently sufficient.

## 14. Central statement

> The reconstructable-singularity threshold is the minimum connected set of observational frameworks whose combined affirmative and exclusionary constraints reduce the admissibility-consistent continuity histories to one.

This is a research formalism. It defines a testable mathematical structure; it does not by itself claim empirical proof, execution authority, publication authority, or release readiness.
