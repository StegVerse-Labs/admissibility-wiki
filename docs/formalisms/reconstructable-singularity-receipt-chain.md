---
title: Receipt-Chain Reconstruction — Derivations (DRAFT, candidate)
---

# Receipt-Chain Reconstruction — Derivations (DRAFT, candidate)

Status: **DRAFT / candidate derivations.** Prepared 2026-10-16 by Grok Bot for owner and practitioner review.

> **Disclaimer.** This is a working draft. It is not a statement of truth, not a legal or patentability determination, and grants no execution, release, publication or standing authority. Every item is a candidate for owner/practitioner review. Nothing here has been added to any repository.

Each step is tagged:
- **[STD]**: follows from a standard published result (cited);
- **[NEW]**: new derivation written in this draft (elementary, but not yet reviewed);
- **[ASSUME]**: explicit assumption;
- **[INTERP]**: interpretation or mapping, not a derivation.

## 0. Sources used

| Ref | Source | Path | Commit |
|---|---|---|---|
| RS | Reconstructable Singularity formalism v0.1 | `StegVerse-Labs/admissibility-wiki/docs/formalisms/reconstructable-singularity.md` (public at https://admissibility.stegverse.org/formalisms/reconstructable-singularity/) | repo HEAD `7b3f1ff2450d5e7b400233d5db43685099e245fc`; last change to file `e76a7dd9b846b451a34b6632c9dfa65a87f5fc1a` (2026-09-18) |
| RS-contract | schema/example/validator | `static/formalisms/reconstructable-singularity.v0.1.{schema,example}.json`, `scripts/check_reconstructable_singularity.py` | same HEAD; validator run 2026-10-16 → "RECONSTRUCTABLE SINGULARITY: PASS - schema assets present, singleton reconstruction computed, and selected perspective set is minimal" (fixture only) |
| AE-RS | Reconstruction Sufficiency | `Admissible-Existence/AE/docs/RECONSTRUCTION_SUFFICIENCY.md` | `7f02693666da633ecb120828d074e9e08e36570f` |
| STCM-N | STCM bounded derivations | `Admissible-Existence/STCM/docs/MATHEMATICAL_NOTATION.md` | `abf119f0cda0681ad9844592bc108173207d5cb1` |
| STCM-L | STCM v0.4 sequential receipt lineage | `Admissible-Existence/STCM/docs/STCM_V0_4_SEQUENTIAL_RECEIPT_LINEAGE.md` | `abf119f0…` |
| TT-N | TT replay preservation (TT-PC-004) | `Admissible-Existence/TT/docs/MATHEMATICAL_NOTATION.md` §Replay preservation | `ba3cca71b6928cf739ab6b321c939860fd1edbb1` |

External standard references. **(v)** means the bibliographic details were verified this session; **(c)** means they are cited from memory and need a practitioner check:
- [M79] R. C. Merkle, *Secrecy, Authentication, and Public Key Systems*, Ph.D. thesis, Stanford University, 1979. (v)
- [HS91] S. Haber, W. S. Stornetta, "How to time-stamp a digital document," *J. Cryptology* 3(2):99–111, 1991, doi:10.1007/BF00196791. (v)
- [D89] I. Damgård, "A Design Principle for Hash Functions," CRYPTO '89 (LNCS 435), 1990; and [M89] R. C. Merkle, "One Way Hash Functions and DES," same volume. (c; the Merkle–DES item is listed in HS91's references)
- [S48] C. E. Shannon, "A Mathematical Theory of Communication," *Bell Syst. Tech. J.* 27, 1948. (c)
- [S49] C. E. Shannon, "Communication in the Presence of Noise," *Proc. IRE* 37(1), 1949. (c)
- [CT] T. Cover, J. Thomas, *Elements of Information Theory*, 2nd ed., Wiley 2006 (source coding theorem, Kraft–McMillan). (c)

---

## 1. Discrete model

**[ASSUME] A1 (discrete states).** Each realized state is a finite bit string, \(S_j\in\{0,1\}^{n_j}\). For audio and video this is already the case: a decoded frame is a finite array of quantized samples. "Perfect fidelity" means bit-exact equality with the captured digital record (see §8).

**[ASSUME] A2 (deterministic processor).** A fixed, pinned, deterministic function \(P\) and transition payloads \(\delta_j\in\{0,1\}^*\) give
\[S_{j+1}=P(S_j,\delta_j),\qquad j=0,\ldots,m-1.\]
Two special forms are useful:
(i) a raw delta, \(P(S,\delta)=S\oplus\delta\) or a tile-replacement list;
(ii) model plus residual, \(P(S,\delta)=\Pi_M(S)\star r\) with pinned predictor \(\Pi_M\) and an invertible correction \(\star\), meaning that for fixed \(S\) the map \(r\mapsto\Pi_M(S)\star r\) is injective.

**[ASSUME] A3 (unambiguous encoding).** \(\langle\cdot\rangle\) is an injective, length-prefixed encoding of tuples.

**Receipts.** For a hash \(H:\{0,1\}^*\to\{0,1\}^\lambda\) and domain tags \(\tau_0\ne\tau\):
\[R_0=H\langle\tau_0,\,0,\,S_0\rangle,\qquad R_{j+1}=H\langle\tau,\,j{+}1,\,R_j,\,\delta_j,\,S_{j+1}\rangle.\]
(Binding \(H(\delta_j)\) and a Merkle root of \(S_{j+1}\) in place of the raw values gives the same results. Collisions then also count collisions of the inner hash or tree.)

**Link to RS §2 [INTERP].** \(\gamma=(S_0,T_0,C_0,S_1,\ldots,S_m)\) with \(T_j:=(P,\delta_j)\). The cost \(C_j\) is carried as accounting metadata inside \(\delta_j\) or the receipt, so it is bound by the same hash. \(\Gamma_A\) is the set of histories consistent with A2 and the admissibility matrix (RS §3).

---

## 2. Lemma G2: deterministic replay is bit-exact [NEW, elementary]

**Statement.** Under A1–A3, the inputs \((S_0,\delta_0,\ldots,\delta_{m-1})\) determine every \(S_j\) and every \(R_j\) uniquely. Any two executions of the procedure on the same inputs produce identical \(S_j\) and \(R_j\) for all \(j\).

**Proof (induction on \(j\)).**
1. *Base case.* \(S_0\) is given. \(R_0=H\langle\tau_0,0,S_0\rangle\) is a function of given data, so it is unique.
2. *Inductive step.* Assume \(S_j\) and \(R_j\) are uniquely determined. \(S_{j+1}=P(S_j,\delta_j)\) is a value of a function (A2) at determined arguments, so it is unique. \(R_{j+1}=H\langle\tau,j{+}1,R_j,\delta_j,S_{j+1}\rangle\) is a function of determined arguments, so it is unique.
3. By induction this holds for all \(j\le m\). ∎

**Remark.** This is a stronger, state-level version of TT-PC-004 (TT-N), which asserts preservation only of the *outcome class* under identical inputs. The assumption that carries the weight is A2: the processor must be bit-deterministic, with the same floating-point behaviour, codec build and so on. The clock-video run (PAT-003 issue #16: 422 receipts regenerated, terminal SHA-256 matched) is one empirical instance.

---

## 3. Lemma G3: terminal-receipt match implies chain equality, except with collision probability [STD reduction, written out NEW]

**[ASSUME] A4 (collision resistance).** For every efficient procedure \(\mathcal B\), \(\Pr[\mathcal B \text{ outputs } x\ne x' \text{ with } H(x)=H(x')]\le\epsilon_{\mathrm{coll}}\). This is a computational assumption about the chosen \(H\) (e.g. SHA-256). It is not a theorem.

**Statement.** Let \((S_0,\delta)\) and \((S'_0,\delta')\) be two input sequences of lengths \(m\) and \(m'\) with terminal receipts \(R_m=R'_{m'}\). If \((S_0,\delta,m)\ne(S'_0,\delta',m')\), a collision of \(H\) can be computed from the two sequences in \(O(m)\) hash evaluations. Therefore any procedure that produces such a pair succeeds with probability at most \(\epsilon_{\mathrm{coll}}\).

**Proof.**
1. Write \(x_j\) for the encoded input of \(R_j\), so \(R_j=H(x_j)\), and likewise \(x'_j\).
2. *Case \(m\ne m'\).* The index field differs, so \(x_m\ne x'_{m'}\) by A3, while \(H(x_m)=H(x'_{m'})\). This is a collision.
3. *Case \(m=m'\).* Let \(j^*\) be the largest index with \(x_{j^*}\ne x'_{j^*}\). It exists because the sequences differ and every \(S_j,\delta_j,S_0\) appears in some \(x_j\).
   - If \(j^*=m\): \(H(x_m)=R_m=R'_m=H(x'_m)\). This is a collision.
   - If \(j^*<m\): \(x_{j^*+1}=x'_{j^*+1}\), and both contain \(R_{j^*}\) and \(R'_{j^*}\) in the same field (A3), so \(R_{j^*}=R'_{j^*}\), i.e. \(H(x_{j^*})=H(x'_{j^*})\) with \(x_{j^*}\ne x'_{j^*}\). This is a collision.
   - *Tag separation.* \(j^*=0\) compares two genesis encodings with tag \(\tau_0\). Mixed-tag comparisons cannot arise because the index fixes the tag.
4. Finding \(j^*\) takes one backward scan. ∎

This is the standard hash-chain/Merkle–Damgård argument ([M79], [D89]/[M89]). Its use for tamper-evident ordered records follows [HS91]. A *trusted* terminal receipt (received out of band or anchored) is required. A receipt that arrives with the payload over the same untrusted channel proves nothing.

---

## 4. Lemma G4: receipts alone do not determine content [STD counting, NEW framing]

**Statement.** Let \(X\subseteq\{0,1\}^n\) be the admissible content set of a frame and \(g_H=H|_X\). If \(|X|>2^\lambda\), then \(g_H\) is not injective, and some hash value has at least \(\lceil |X|/2^\lambda\rceil\) preimages. For a history, let \(\mathcal R\) be the set of receipt perspectives (any number \(q\) of receipts). If \(|\Gamma_A|>2^{\lambda q}\), then \(G_{\mathcal R}\) is not injective on \(\Gamma_A\), so in RS §7 terms \(\mathcal R\) alone is not resolving.

**Proof.** The image of \(G_{\mathcal R}\) has at most \(2^{\lambda q}\) values. By the pigeonhole principle, \(|\Gamma_A|\) histories mapped into fewer values force two histories to share an image. ∎

**Consequences.**
- *Verification is not transport.* Receipts verify a candidate history (G3), but the content-bearing perspectives (genesis and transition payloads, or model plus residuals) must be transmitted or stored.
- *Exception (search).* If \(|\Gamma_A|\) is small enough to enumerate, e.g. one unknown pixel with known prior state, then \(G_{\mathcal R}\) can be *computationally* resolving by exhaustive test against the receipts. The cost is \(\Theta(|\Gamma_A|)\) hash evaluations. Note that RS §7 injectivity is a non-constructive property: it does not by itself give an efficient decoder.

---

## 5. Theorem candidate G8: minimum resolving perspective set for a receipt chain [NEW, candidate]

**Setting (instantiating RS §§6–8).** The perspectives \(\mathcal E\) are:
- \(g_{S_0}\), the genesis content;
- \(g_{\delta_j}\), the payload of step \(j\) (one perspective per step);
- \(g_{R_m}\), the trusted terminal receipt;
- \(g_{R_j}\) for \(0\le j<m\), intermediate receipts;
- \(g_M\), the pinned model or processor identity, \(P\).

Let \(V_j\) be the set of admissible values of \(\delta_j\) given \(\Gamma_A\). Call step \(j\) **trivial** if \(|V_j|=1\), e.g. a region declared frozen, or a zero residual forced by the model.

**Two notions [INTERP; this distinction is the key addition to RS]:**
- *Resolving* (RS §7): \(G_I\) is injective on \(\Gamma_A\). This assumes perspectives report true values.
- *Verified-resolving:* perspectives other than a trusted anchor may arrive over an untrusted channel. The set must be resolving, and any substituted values must be rejected except with probability \(\le\epsilon_{\mathrm{coll}}\).

**Claim 5.1 (sufficiency).** \(I_0=\{g_{S_0}\}\cup\{g_{\delta_j}: j \text{ non-trivial}\}\) (with \(P\) pinned) is resolving. \(I_0\cup\{g_{R_m}\}\) is verified-resolving under A4.
*Proof.*
1. The trivial \(\delta_j\) are fixed by \(\Gamma_A\).
2. \(G_{I_0}\) therefore fixes \((S_0,\delta)\), and by G2 it fixes \(\gamma\). So it is injective.
3. For verified-resolving: any substituted \((S'_0,\delta')\) that differs and still matches the trusted \(R_m\) yields a collision (G3).
∎

**Claim 5.2 (redundancy of intermediate receipts).** For every \(j<m\), \(g_{R_j}=\phi_j\circ G_{I_0}\) for a deterministic function \(\phi_j\) (G2). Hence \(G_{I\cup\{g_{R_j}\}}\) is injective iff \(G_I\) is, whenever \(I\supseteq I_0\). Equivalently, in hitting-set form (RS §8), any pair \(\gamma\ne\gamma'\) whose distinguishing set contains \(g_{R_j}\) also has a distinguishing set meeting \(I_0\). Intermediate receipts are regenerable and add no resolving power. Their value lies in localization (G7) and in checkpointing, not in identifiability.
*Proof.* If \(G_{I_0}(\gamma)=G_{I_0}(\gamma')\), then \(\gamma=\gamma'\) by 5.1, so \(g_{R_j}\) agrees. Contrapositive: \(g_{R_j}(\gamma)\ne g_{R_j}(\gamma')\Rightarrow G_{I_0}(\gamma)\ne G_{I_0}(\gamma')\). ∎

**Claim 5.3 (necessity, information-theoretic).** Let \(j\) be non-trivial. Then \(I_0\setminus\{g_{\delta_j}\}\) together with any set of receipt perspectives is not resolving in the *information-theoretic* sense when \(|V_j|>2^{\lambda q}\) (G4 applied to the single unknown \(\delta_j\)). If instead \(|V_j|\le\) a feasible search budget, receipts can stand in for \(g_{\delta_j}\) computationally (G4 exception).
*Proof.* Fix all other perspectives. The candidates differ only in \(\delta_j\in V_j\) and its downstream consequences. Apply the pigeonhole argument of G4 to the \(q\) receipt values. ∎
Also, without any receipt, two histories that differ only in \(\delta_j\) agree on every other payload and on the genesis, so \(D_{\gamma,\gamma'}=\{g_{\delta_j}\}\cup\{\text{receipts at or after } j\}\). The hitting-set condition therefore forces \(g_{\delta_j}\) or a downstream receipt, and only the former is content-bearing.

**Claim 5.4 (threshold).** Under the per-step perspective granularity and A2–A4, with every non-trivial \(|V_j|\) beyond search range:
\[k^*_\Gamma=1+\#\{j:|V_j|>1\},\qquad k^*_{\text{verified}}=k^*_\Gamma+1\ (\text{trusted }R_m).\]
The pinned model \(g_M\) is a precondition, not a counted perspective; if it is counted, add 1. Fragments without content payloads (receipts only, or genesis plus receipts) are not resolving by 5.3.
*Status:* candidate. The counting depends on the granularity chosen for perspectives. With one aggregated "payload stream" perspective, \(k^*=2\) or \(3\). The value is structural (RS §6), not absolute.

**Claim 5.5 (frozen regions and subtree reuse) [STD + NEW].** Split \(S_j\) into \(N\) tiles under a Merkle tree [M79]. Let \(c_j\) be the number of changed tiles. Then \(\delta_j\) needs only the \(c_j\) changed tiles plus their indices (or an \(N\)-bit change map). The new root is computed with \(O(c_j\log N)\) hash evaluations, reusing unchanged subtree hashes. Unchanged tiles contribute trivial sub-perspectives (\(|V|=1\) once declared frozen), so by 5.4 they drop out of \(k^*\). This matches STCM-PC-003 (non-matching nodes are not activated, STCM-N §Hash-scoped activation) and the governance cost partition of STCM-PC-005 [INTERP].

**Model-plus-residual variant.** Replace \(g_{\delta_j}\) by \(g_{r_j}\) under A2(ii). Claims 5.1–5.4 carry over unchanged because the correction map is injective in \(r\) for fixed \(S\).

**Relation to AE-RS [INTERP].** AE's \(|\mathcal R(Y)/\equiv_M|=1\) is the same singleton condition with a materiality quotient. For bit-exact transfer, \(\equiv_M\) is equality. AE's continuous rank condition \(\operatorname{rank}J_H=d\) has no direct analogue here: the discrete analogue is injectivity itself (RS §7).

---

## 6. G5: payload size lower bound [STD]

**Statement.** Let the residual sequence \(r=(r_0,\ldots,r_{m-1})\) be a random variable given the receiver's side information \(Z=(S_0,M)\). Any uniquely decodable binary code for \(r\) that may depend on \(Z\) has expected length \(\ge H(r\mid Z)\) bits ([S48]; Kraft–McMillan, [CT]). Codes within one bit per block of this bound exist, e.g. arithmetic or Huffman coding under the true conditional law.

**Total transfer cost [NEW accounting].** The total is about \(|S_0|+H(r\mid Z)+\lambda\) bits. The \(\lambda\) is the trusted terminal receipt, plus any chosen checkpoints. Receipts add \(O(\lambda)\) per checkpoint, not per pixel.

**Better models.** A better model lowers \(H(r\mid Z)\) toward the information the model cannot predict.

**Chaotic systems [INTERP; not derived].** For chaotic dynamics (e.g. the double pendulum) prediction error grows over time. Residual entropy per frame is then expected to stay high unless predictions are re-anchored often. Quantifying this, e.g. through Kolmogorov–Sinai entropy, is open and is not claimed here.

**Prior-art caution [INTERP].** Lossless predictive coding is well established. Novelty, if any, must lie in the binding of the receipt chain, the perspective-threshold structure and the cross-node transfer, not in compression alone.

---

## 7. G7: continuity lemma (missing, forked, stale links) [NEW, discrete; generalizes STCM-L fixtures]

**Setting.** A verifier holds a set \(\mathcal Q\) of claimed receipt records \((j,R_j,\text{pred}=R_{j-1})\) and a trusted head \((m,R_m)\).

**Statement (under A4).**
1. *Missing link.* If, walking back from \(R_m\) by predecessor references, some referenced \(R_{j-1}\) is absent from \(\mathcal Q\) (and from regenerable data), the gap at index \(j-1\) is detected and localized.
2. *Fork.* If two distinct records claim the same predecessor and the same index, at most one lies on the path to the trusted \(R_m\) unless a collision exists. The fork is detected and the off-path branch is identified.
3. *Stale or out-of-sequence binding.* A record claiming index \(j\) whose predecessor's index is not \(j-1\), or whose predecessor is not the current head when appended, violates the index field bound in the hash. It is detected (cf. STCM-L verdicts: missing prior, hash mismatch, stale, superseded, competing chains).
4. *Limit.* Without a trusted head index \(m\), truncation of the tail (dropping \(R_{m'}\ldots R_m\)) is undetectable. Trusted anchoring of the head is necessary.

**Proof sketch.**
1. Every \(R_j\) commits to \((j,R_{j-1})\) (A3).
2. The backward walk from a trusted \(R_m\) is unique except with collision probability (G3).
3. Any record not on that walk either fails linkage (cases 1 and 3) or shares a predecessor with an on-path record (case 2).
4. Case 4: an untrusted shorter chain is internally consistent.
∎

---

## 8. G9: mode generality via sampling and quantization [STD + ASSUME]

**[STD] Sampling theorem [S49].** A signal band-limited to \(B\) Hz is exactly determined by samples at rate \(f_s>2B\).

**[ASSUME] A5 (band limitation).** Physical signals are only approximately band-limited. An anti-aliasing filter is part of the capture boundary.

**[ASSUME] A6 (quantization boundary).** Quantization to \(b\) bits is lossy with respect to the continuous physical field. Therefore "perfect (bit-exact) fidelity" is claimed for the captured digital record \(S_j\), and fidelity to the physical field is bounded by the capture parameters.

Once captured, every mode is an instance of §1 (A1). §§2–7 then apply without change.

**Mode variables (what fixes \(n_j\), \(m\) and the model class) [INTERP]:**

| Mode | Discretization variables | Natural "state" \(S_j\) | Typical model / residual |
|---|---|---|---|
| Optical / video | resolution, frame rate, bit depth, colour channels, colour space | frame | motion or inter-frame prediction |
| Acoustic / audio | sample rate, bit depth, channels | block of samples | linear prediction |
| RF / radio | carrier, bandwidth, I/Q sample rate, ADC bits | I/Q block | demodulated symbols plus channel estimate |
| Wired electrical | symbol rate, levels or encoding | symbol block | line code |
| Vibration / seismic | axes, sample rate, dynamic range | multi-axis block | physical model (modal) |
| Other (thermal, pressure, chemical sensors) | sample rate, resolution, sensor count | sensor vector | process model |

Audio and video records are already discrete (frames and quantized samples), so A5 and A6 apply only at original capture, not to re-transfer of an existing file. The clock webm (sha256 `069d9a26…eb8b`) is such a record.

---

## 9. Status summary

| Item | Status | Rests on |
|---|---|---|
| G2 bit-exact replay | NEW, complete elementary induction | A1–A3 (A2 determinism is the practical risk) |
| G3 terminal match ⇒ equality | STD reduction, written out | A3, A4, trusted \(R_m\) |
| G4 hashes don't carry content | STD counting | none beyond the sizes |
| G8 minimum resolving set (5.1–5.5) | NEW candidate; proofs written out | G2–G4, A4; result depends on perspective granularity; injectivity ≠ efficient decoding |
| G5 size bound | STD (Shannon) + NEW accounting; chaotic part is interpretation only | probabilistic model of residuals |
| G7 continuity | NEW discrete lemma; proof sketch | A3, A4, trusted head |
| G9 mode generality | STD + explicit assumptions A5, A6 | capture boundary |

**Open items.**
- Formalize the "verified-resolving" notion inside RS (an exclusionary \(O^-\) perspective in RS §4 terms).
- Decide the perspective granularity for the patent.
- Quantify chaotic residual growth.
- Have a practitioner check the (c) citations.
- Run the comms experiment.
