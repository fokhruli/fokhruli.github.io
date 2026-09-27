# JEPA Atlas — compiled technical review

Review snapshot: 2026-09-26

Technical briefs for the 19 papers added in the September review, not the complete awesome-JEPA catalog.

18 records have selected method/result sections checked; one is abstract-only. These are author-reported results, not independent replications. Schematic equations use normalized notation. Curator experiments are proposals, not paper claims. Publication acceptance is not inferred.

# CGM-JEPA

CGM-JEPA: Learning Consistent Continuous Glucose Monitor Representations via Predictive Self-Supervised Pretraining

arXiv:2605.00933 · v1 · sections_checked · checked 2026-09-26

Primary source: https://arxiv.org/html/2605.00933v1
Source locators: Method; Tables 1–2

## Problem
Learn useful glucose representations with scarce metabolic labels.

## Intuition
Hide part of a glucose trace and predict its representation. A second view describes the distribution of glucose values, rather than their order.

## Mechanism
CGM-JEPA predicts masked temporal embeddings; X-CGM-JEPA adds Glucodensity cross-view prediction. Evaluation freezes the encoder and fits a logistic classifier.

## Objective / pipeline
context glucose → predicted masked latent ≈ target latent; X-CGM adds cross-view alignment (schematic).

## Training
Unlabeled CGM pretraining; labels used for downstream probes, not pretraining.

## Deployment
CGM encoder plus fitted classifier; not an insulin policy.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### Home CGM: beta-cell dysfunction
AUROC: 0.946 0–1; comparator PCA: 0.925.

Protocol: Subject-level 2-fold CV repeated 20 times; small cohorts (N=27/17 in the study).

Uncertainty: Reported ±0.063 versus ±0.069; repeats share subjects.



Evidence: https://arxiv.org/html/2605.00933v1 — Table 1

### Home CGM: insulin resistance
AUROC: 0.857 0–1; comparator GluFormer: 0.889.

Protocol: Same paper, endpoint-specific comparison.

Uncertainty: Reported ±0.112 versus ±0.103.



Evidence: https://arxiv.org/html/2605.00933v1 — Table 2

## Limitations
- Small-cohort phenotyping; no dosing or closed-loop safety experiment.
- X-CGM does not win every metric or endpoint.

## Next experiment — curator proposal
For a new CGM study, split by subject before windowing; compare temporal-only versus temporal-plus-distribution embeddings with identical probes.

## Concepts
latent, temporal, grounding

---

# GlucoFM

GlucoFM: A Dual-Stream Foundation Model for Continuous Glucose Monitoring

arXiv:2605.30865 · v1 · sections_checked · checked 2026-09-26

Primary source: https://arxiv.org/html/2605.30865v1
Source locators: Section 3; Eq. 5; Tables 2–3

## Problem
Keep slow glucose state and short-lived events in the same representation.

## Intuition
A daily baseline and a brief excursion tell different stories. Two streams try to retain both instead of averaging away the excursion.

## Mechanism
Dual-stream latent modeling combines masked contextual reconstruction and temporal-dynamics constraints. The online encoder is retained; the EMA target branch is discarded.

## Objective / pipeline
L = L_masked-context + L_temporal-dynamics (Eq. 5; both weights 1).

## Training
477 subjects, 109,066 hours; compact 3-layer Transformers; 0.72M trainable parameters.

## Deployment
Frozen 24-hour-window embeddings with a supervised downstream probe.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### 14 cohort–endpoint evaluations
Average ROC-AUC: 66.7 percent; comparator CGM-JEPA, retrained on same corpus: 62.4.

Protocol: 10 repetitions of 5-fold subject-grouped CV; four downstream cohorts.

Uncertainty: Not extracted; do not infer significance.

MantisV2 scores 64.7; heterogeneous pretraining is a separate comparison.

Evidence: https://arxiv.org/html/2605.30865v1 — Table 3

## Limitations
- Not best on every endpoint; device/sampling shifts remain.
- Metabolic classification does not establish safe insulin control.

## Next experiment — curator proposal
Probe slow-state and event streams separately. Test whether meal/exercise-related information survives compression, without labeling an observational association causal.

## Concepts
latent, temporal

---

# TD-JEPA

TD-JEPA: Latent-predictive Representations for Zero-Shot Reinforcement Learning

arXiv:2510.00739 · v1 · sections_checked · checked 2026-09-26

Primary source: https://arxiv.org/html/2510.00739v1
Source locators: Eq. 9; Algorithm 1; Table 1

## Problem
Learn task-adaptable control representations before rewards are specified.

## Intuition
Instead of predicting only the next state, summarize what a policy will encounter over many future steps. Later, task weights select useful behavior.

## Mechanism
Temporal-difference learning builds policy-conditioned multi-step latent predictions from reward-free offline transitions; the practical method uses symmetric objectives and orthonormality regularization.

## Objective / pipeline
T(φ(s),a,z) ≈ stopgrad[ψ(s′) + γ T(φ(s′),a′,z)], a′ ~ π_z (normalized Eq. 9).

## Training
Offline state/action/next-state transitions; target networks and task-conditioned policies.

## Deployment
Infer a task representation and use its policy without task-specific policy retraining.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### DMC_RGB task average
Return: 628.8 reward units; comparator BYOL-γ*: 582.4.

Protocol: Paper-matched visual-control evaluation; not a success rate.

Uncertainty: Reported standard errors: 5.5 versus 9.8.



Evidence: https://arxiv.org/html/2510.00739v1 — Table 1

## Limitations
- Idealized theoretical assumptions and learned feature/task coverage matter.
- Not an arbitrary-reward or safety guarantee.

## Next experiment — curator proposal
Hold the offline dataset fixed; test unseen reward functions and identify which lie outside the representation’s task span.

## Concepts
latent, action, decision

## Curation audit
This arXiv ID is the zero-shot-RL TD-JEPA. The similarly named baseline in D-JEPA is a different work; no identity or citation edge is inferred.

---

# XP-JEPA

XP-JEPA: Cross-Predictive Physics Grounding for Forecastable Latent Dynamics

arXiv:2608.24044 · v1 · sections_checked · checked 2026-09-26

Primary source: https://arxiv.org/html/2608.24044v1
Source locators: Section 3; Eq. 1; Section 4; Appendix C

## Problem
An easy-to-predict latent space may still miss physical distinctions needed for control.

## Intuition
Two scenes can look alike but react differently to the same action. Training-time physical trajectories provide a second account of what really changes.

## Mechanism
Separate visual/physical encoders share an action-conditioned predictor. Each branch predicts both future modalities; per-branch regularization discourages collapse.

## Objective / pipeline
L ≈ Σ_{m,n∈{vision,state}} ||g(z_t^m,a_t) − z_{t+1}^n||² + β(Ω_vision + Ω_state) (Eq. 1, abbreviated).

## Training
Paired visual observations, actions and privileged physical trajectories.

## Deployment
Discard the physical branch; visual-only latent planning.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### Six evaluation subfamilies
Mean control success: 78.2 percent; comparator Visual-only model: 53.6.

Protocol: Matched data/planner; three seeds.

Uncertainty: Not extracted; do not infer significance.



Evidence: https://arxiv.org/html/2608.24044v1 — Section 4; Figures 4–5

### Frozen-encoder fresh-predictor test
Rollout drift: 0.104 paper-defined drift; comparator Visual-only encoder: 0.361.

Protocol: Original predictor removed and an identical fresh predictor fitted.

Uncertainty: Not extracted; do not infer significance.



Evidence: https://arxiv.org/html/2608.24044v1 — Section 4; Appendix C

## Limitations
- Physical-state decodability alone does not imply forecastability.
- Visual robotics results are not physiological-control validation.

## Next experiment — curator proposal
Compare privileged-state regression against cross-prediction; then freeze both encoders and refit the same predictor to separate representation gains from co-adaptation.

## Concepts
latent, grounding, action, rollout

## Curation audit
Earlier curation called this JEPA-x. The inspected v1 article uses XP-JEPA; the arXiv ID is unchanged.

---

# Delta-JEPA

Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding

arXiv:2606.31232 · v1 · sections_checked · checked 2026-09-26

Primary source: https://arxiv.org/html/2606.31232v1
Source locators: Method; Eq. 7; Table 1

## Problem
Latent predictions can be insensitive to the action that caused a transition.

## Intuition
Make the change between two embeddings reveal which action occurred. This discourages a representation that ignores the control input.

## Mechanism
An auxiliary decoder reconstructs actions from consecutive latent differences alongside forward latent prediction.

## Objective / pipeline
L = L_prediction + λ L_action; â_t = decoder(z_{t+1} − z_t) (Eq. 7, schematic decoder).

## Training
Action-labeled transitions; joint encoder/predictor/action-decoder optimization.

## Deployment
Use the learned action-conditioned world model for planning.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### PushT
Control success: 89.07 percent; comparator LeWM: 84.53.

Protocol: Paper’s visual continuous-control evaluation.

Uncertainty: Reported ±1.90 versus ±1.50; uncertainty convention not extracted.



Evidence: https://arxiv.org/html/2606.31232v1 — Table 1

### OGB-Cube
Control success: 79.27 percent; comparator LeWM: 64.13.

Protocol: Same evaluation table.

Uncertainty: Reported ±1.81 versus ±1.89; uncertainty convention not extracted.



Evidence: https://arxiv.org/html/2606.31232v1 — Table 1

## Limitations
- Four visual tasks; one-step action recovery need not capture delayed effects.
- Action-sensitive features need not contain every exogenous task-relevant variable.

## Next experiment — curator proposal
Use matched transitions to test action recovery at several lags. Separately test retention of exogenous variables needed for the reward.

## Concepts
latent, action

---

# D-JEPA

D-JEPA: A Decision-Aligned Latent World Model

arXiv:2609.24749 · v1 · sections_checked · checked 2026-09-26

Primary source: https://arxiv.org/html/2609.24749v1
Source locators: Section 3; Eqs. 1–2; Tables 1–2

## Problem
Accurate-looking future embeddings may rank candidate actions incorrectly.

## Intuition
A planner needs the best candidate, not just a plausible forecast. Outcome feedback can teach a small correction to the ranking.

## Mechanism
Bounded, permutation-equivariant corrections use goal-relative candidate descriptors and executed-outcome supervision. Successful candidates receive probability mass while trust/locality terms constrain corrections.

## Objective / pipeline
L ≈ −log Σ_{i:success} softmax(−s/T)_i + λ_local L_local + λ_trust mean(δ²) (Eq. 2).

## Training
Candidate futures plus realized outcome labels; not reward-free pretraining.

## Deployment
Calibrate candidate scores before selecting an action.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### PushT matched candidate pool
Success: 87.89 percent; comparator JEPA-WM: 85.16.

Protocol: 256 evaluation cases; LeWM also scores 83.59.

Uncertainty: Not extracted; do not infer significance.



Evidence: https://arxiv.org/html/2609.24749v1 — Table 1

### Physical PiPER evaluation
Success: 81 percent; comparator Native policy: 64.

Protocol: 100 cases in this separate evaluation.

Uncertainty: Not extracted; do not infer significance.



Evidence: https://arxiv.org/html/2609.24749v1 — Table 2

## Limitations
- Empirical ranking improvements are not safety certificates.
- Different from denoising D-JEPA (2410.03755).

## Next experiment — curator proposal
Construct a fixed candidate pool; measure realized regret and ranking correlation, not only latent MSE. Hold the candidate generator constant.

## Concepts
decision, action, latent

## Curation audit
Denoising D-JEPA and decision-aligned D-JEPA are separate papers. The TD-JEPA baseline named in this paper is not automatically the zero-shot-RL TD-JEPA in this atlas.

---

# Exogenous-feature study

Predictive Objectives Discard Exogenous Control-Relevant Features: A Controlled Mechanistic Study

arXiv:2606.30068 · v1 · sections_checked · checked 2026-09-26

Primary source: https://arxiv.org/html/2606.30068v1
Source locators: Main controlled study; Figure 4; Appendix Table 4

## Problem
Predictability or controllability may select the wrong information for a future task.

## Intuition
A variable can matter to your decision even when your action cannot change it. “Useful for prediction” and “useful for control” are different tests.

## Mechanism
Controlled experiments cross controllability with task relevance, holding architecture/data comparable across predictive and task-grounded objectives.

## Objective / pipeline
Diagnostic: probe each controllability × relevance quadrant; vary reward supervision rather than assuming predictive loss is sufficient.

## Training
Synthetic controlled environments; reward-free versus partially reward-grounded objectives.

## Deployment
An analysis/diagnostic, not a deployable controller.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### QuadrantEnv exogenous task-relevant probe
Probe accuracy: 0.77 0–1; comparator 1% reward-grounded condition: 0.72.

Protocol: 2% versus 1% reward grounding; diagnostic threshold 0.75.

Uncertainty: Not extracted; do not infer significance.

Reward-free conditions are near chance in the studied setup.

Evidence: https://arxiv.org/html/2606.30068v1 — Figure 4; Appendix Table 4

## Limitations
- Deliberately narrow mechanistic construction, not a universal JEPA theorem.
- Reward grounding is not shown to solve all feature-selection failures.

## Next experiment — curator proposal
Create a controlled driver-blindness test: vary whether a driver is predictable, controllable and reward-relevant independently. Evaluate each factor with a probe.

## Concepts
exogenous, action, decision

---

# Semigroup-JEPA

Semigroup-JEPA: Latent Dynamics Consistency for Zero-Shot Physics Generalization

arXiv:2609.10464 · v1 · sections_checked · checked 2026-09-26

Primary source: https://arxiv.org/html/2609.10464v1
Source locators: Method; Appendix C; Figure 5

## Problem
One-step accuracy may not survive recursive rollout under changed physics.

## Intuition
An error becomes the next input. Training through several predicted steps exposes that feedback rather than hiding it with the true next state.

## Mechanism
Gravity-conditioned encoder/predictor training uses recursive latent rollout and SIGReg. Fresh-predictor tests distinguish representation gains from the original predictor.

## Objective / pipeline
L ≈ Σ_{k=1..K} γ^(k−1)||ẑ_{t+k} − z_{t+k}||² + λ SIGReg(z); K=5, γ=0.95.

## Training
Narrow gravity distributions; history H=20; GRU/SSM variants.

## Deployment
Supplied gravity remains an input. Control uses separately trained diffusion policies on frozen features.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### 2D square: fresh GRU on frozen encoders
Mean rollout error: 1.376 paper-defined error; comparator Transformer-trained encoder: 1.555.

Protocol: Same newly fitted GRU; GRU-trained encoder versus Transformer-trained encoder.

Uncertainty: Not extracted; do not infer significance.



Evidence: https://arxiv.org/html/2609.10464v1 — Figure 5(a); Section 4

## Limitations
- Unknown physical parameters are not inferred.
- Theory uses linear features; nonlinear/contact behavior has additional caveats.

## Next experiment — curator proposal
Report teacher-forced and free-rollout error separately, then replace the predictor. Test supplied-parameter errors before claiming adaptation.

## Concepts
grounding, rollout, latent

---

# RD-JEPA

RD-JEPA: Predictive latent pretraining for few-trajectory transfer across reaction–diffusion equations

arXiv:2609.29403 · v1 · sections_checked · checked 2026-09-26

Primary source: https://arxiv.org/html/2609.29403v1
Source locators: Unseen-reaction-law experiment; Table 1

## Problem
Forecast a new reaction law using very few target trajectories.

## Intuition
Learn common dynamical features from related systems, then spend the small adaptation budget on the unfamiliar system instead of learning everything again.

## Mechanism
Predictive-latent pretraining transfers to supervised full-field forecasting; three held-out reaction families are excluded from pretraining.

## Objective / pipeline
Source predictive-latent pretraining → target-system adaptation → field forecasts (pipeline, not a transcribed loss).

## Training
Five source equation families; unseen-system adaptation with 1, 5 or 10 trajectories.

## Deployment
Adapted forecaster receives observed fields and the forecast horizon.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### Held-out Lambda–Omega; one support trajectory
Relative L2 field error: 12.24 table units ×10⁻²; comparator RieszNO: 19.2.

Protocol: Horizon average h=1…5; same 300 test trajectories; three paired support selections.

Uncertainty: Sample SD 2.58 versus 4.72.

Multiply table values by 0.01 for the unscaled relative error.

Evidence: https://arxiv.org/html/2609.29403v1 — Table 1

## Limitations
- Related PDE families and finite horizons, not universal physics transfer.
- Only three paired support selections; no formal hypothesis test reported.

## Next experiment — curator proposal
Separate source-system reuse from genuinely held-out dynamics. Use identical support trajectories and a strong non-JEPA pretrained baseline.

## Concepts
latent, grounding, temporal

---

# Phys-JEPA

Phys-JEPA: Physics-Informed Latent World Models for Multivariate Time-Series Forecasting

arXiv:2606.16076 · v1 · sections_checked · checked 2026-09-26

Primary source: https://arxiv.org/html/2606.16076v1
Source locators: Eqs. 6–12; Tables 2–5; compact robustness check Table 8

## Problem
Keep known physical descriptors and their changes meaningful in a learned forecaster.

## Intuition
Give part of the embedding a job you can inspect; let the remaining part model what those descriptors do not explain.

## Mechanism
Splits physical/residual latents; combines decoded forecasting, latent prediction, physical-state consistency and physical-change consistency.

## Objective / pipeline
L = L_forecast + αL_JEPA + βL_reg + λ_sL_state + λ_dL_dynamics (Eq. 12).

## Training
Observed sequences and selected physical descriptors; moment regularization on residual features.

## Deployment
Encode a history, forecast latents, decode the future sequence.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### Jena; H=24
MSE: 0.12273 normalized MSE; comparator Supervised forecast-only baseline: 0.12482.

Protocol: L=96; main single-seed setting; aggregate over variables.

Uncertainty: Not extracted; do not infer significance.



Evidence: https://arxiv.org/html/2606.16076v1 — Tables 2–3

### Traffic; H=192
MSE: 0.773873 normalized MSE; comparator Supervised forecast-only baseline: 0.800784.

Protocol: L=96; main single-seed setting; aggregate over variables.

Uncertainty: Not extracted; do not infer significance.



Evidence: https://arxiv.org/html/2606.16076v1 — Table 5

## Limitations
- Main tables are single-seed; compact two-seed checks do not reproduce the full model’s Traffic advantage.
- Hybrid supervision; short-horizon Electricity is worse than the supervised baseline.

## Next experiment — curator proposal
Ablate state consistency and change consistency separately. Compare actual physical measurements with engineered descriptive statistics.

## Concepts
grounding, latent, temporal

## Curation audit
Its Eq. 11 labels a mean/covariance moment penalty SIGReg. Do not assume this is identical to a characteristic-function SIGReg implementation merely because the name matches.

---

# Eidos

EIDOS: Latent-Space Predictive Learning for Time Series Foundation Models

arXiv:2602.14024 · v1 · sections_checked · checked 2026-09-26

Primary source: https://arxiv.org/html/2602.14024v1
Source locators: Method; Table 1

## Problem
Combine useful latent predictability with accurate observable forecasts.

## Intuition
A compact latent space still needs an anchor to what will be measured. Test whether representation alignment adds anything beyond the forecast loss.

## Mechanism
Causal Transformer learning combines latent alignment, observation grounding and direct forecasting supervision.

## Objective / pipeline
L = L_forecast + λ_align L_latent + λ_ground L_observation (schematic decomposition).

## Training
Historical and future time-series observations; hybrid objectives.

## Deployment
Time-series forecasting, not latent-space action search.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### GIFT-Eval overall
CRPS: 0.547 benchmark aggregate; comparator No latent/grounding terms: 0.5597.

Protocol: Same-paper objective ablation; latent-only variant is 0.5570.

Uncertainty: Not extracted; do not infer significance.



Evidence: https://arxiv.org/html/2602.14024v1 — Table 1

### GIFT-Eval overall
MASE: 0.7569 benchmark aggregate; comparator No latent/grounding terms: 0.7678.

Protocol: Latent-only also 0.7678: alignment alone is not the full gain.

Uncertainty: Not extracted; do not infer significance.



Evidence: https://arxiv.org/html/2602.14024v1 — Table 1

## Limitations
- Hybrid supervision must be preserved in fair comparisons.
- Aggregate gains do not prove every dataset or horizon improves.

## Next experiment — curator proposal
Use a 2×2 ablation of latent alignment and observation grounding at fixed capacity, data and training budget.

## Concepts
latent, temporal, grounding

---

# LeNEPA

LeNEPA: No-Augmentation Next-Latent Prediction for Time-Series Representation Learning

arXiv:2607.00958 · v1 · sections_checked · checked 2026-09-26

Primary source: https://arxiv.org/html/2607.00958v1
Source locators: Method; Tables 3–4

## Problem
Reuse a time-series pretraining recipe without hand-designed augmentations.

## Intuition
Predict the next latent token and prevent the whole space collapsing. Then check whether the same recipe works on a different signal family.

## Mechanism
Causal next-latent prediction with SIGReg; no EMA or stop-gradient. Separate pretraining runs reuse one fixed recipe.

## Objective / pipeline
L ≈ next-latent cosine prediction + λ SIGReg(z) (schematic).

## Training
20,000 updates; five-seed PTB-XL/Diag comparison.

## Deployment
Frozen representation probes; recipe transfer is not shared-checkpoint zero-shot transfer.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### Diag classification
AUROC: 0.92 0–1; comparator JEPA CLS: 0.88.

Protocol: Median across five seeds; fixed L4 LeNEPA readout versus best-layer JEPA.

Uncertainty: Seed SD 0.001 versus 0.013.



Evidence: https://arxiv.org/html/2607.00958v1 — Table 3

### UCR-128
Mean accuracy: 77.65 percent; comparator Mantis: 78.81.

Protocol: CauKer pretraining; frozen embeddings plus Random Forest; best LeNEPA checkpoint.

Uncertainty: Not extracted; do not infer significance.



Evidence: https://arxiv.org/html/2607.00958v1 — Table 4

## Limitations
- Readout selection differs in the reported table.
- Not a claim of superiority to optimally retuned baselines; UCR score is below Mantis.

## Next experiment — curator proposal
Pre-register the readout layer and checkpoint rule. Separate recipe robustness from frozen-checkpoint transfer.

## Concepts
latent, collapse, temporal

---

# Distributed JEPA

Distributed JEPA: A Self-Supervised Framework for Energy Forecasting

arXiv:2609.17029 · v1 · abstract_only · checked 2026-09-26

Primary source: https://arxiv.org/abs/2609.17029v1
Source locators: Abstract

## Problem
Transfer energy forecasting representations between heterogeneous assets.

## Intuition
Try to share temporal structure without requiring every solar installation or building to have identical data.

## Mechanism
Masked temporal embedding prediction with covariance and temporal-variance regularization; evaluates asset transfer and degraded data.

## Objective / pipeline
Masked latent prediction + covariance/temporal-variance regularization; exact loss not extracted.

## Training
Heterogeneous energy time series; full training protocol not checked.

## Deployment
Asset-level forecasting; deployment inputs not fully extracted.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### Unseen photovoltaic assets
R² range: 0.73–0.88 0–1; comparator Transformer: < 0.45.

Protocol: Abstract reports improvement on 9/10 assets; horizons, splits and seeds not extracted.

Uncertainty: Not extracted; do not infer significance.



Evidence: https://arxiv.org/abs/2609.17029v1 — Abstract

## Limitations
- Abstract-only record: numerical range is author-reported, not table-audited.
- Not a comprehensive forecasting leaderboard.

## Next experiment — curator proposal
Before reuse, extract the test-asset split, missingness process, horizons and scaling rules; compare per asset, not only the aggregate.

## Concepts
latent, collapse, temporal

---

# FF-JEPA

FF-JEPA: Long-Horizon Planning in World Models with Latent Planners

arXiv:2606.09311 · v1 · sections_checked · checked 2026-09-26

Primary source: https://arxiv.org/html/2606.09311v1
Source locators: Method; Table I

## Problem
Long-horizon search needs useful intermediate targets without a supplied goal image.

## Intuition
First propose where to go next in latent space; then use a short-horizon action planner to get there.

## Mechanism
An action-free latent subgoal planner complements an action-conditioned forward model. Diffusion and deterministic planners are studied; action search uses CEM.

## Objective / pipeline
G(history) → subgoal; CEM minimizes predicted distance to that subgoal (planning schematic).

## Training
Behavior trajectories for world-model and latent-planner learning.

## Deployment
Learned subgoals plus receding-horizon search; no explicit goal image.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### PushT long initialization t=75
Success: 91.8 percent; comparator LeWM: 3.52.

Protocol: 256 evaluation episodes under the paper’s long-initialization protocol.

Uncertainty: Not extracted; do not infer significance.



Evidence: https://arxiv.org/html/2606.09311v1 — Table I

### PushT short initialization
Success: 96.09 percent; comparator LeWM: 94.53.

Protocol: Same paper; far smaller short-horizon gap.

Uncertainty: Not extracted; do not infer significance.



Evidence: https://arxiv.org/html/2606.09311v1 — Table I

## Limitations
- Preliminary single-environment evidence.
- Some external baselines in the table use different protocols.

## Next experiment — curator proposal
Compare learned subgoals to random, expert and interpolated subgoals under equal environment interaction and action-search budgets.

## Concepts
rollout, decision, latent

## Curation audit
The random-initialization success differs between Table I (82.42) and prose (82.25). It is excluded from the numerical records pending reconciliation.

---

# SkyJEPA

SkyJEPA: Learning Long-Horizon World Models for Zero-Shot Sim-to-Real Control of Quadrotors

arXiv:2606.23444 · v1 · sections_checked · checked 2026-09-26

Primary source: https://arxiv.org/html/2606.23444v1
Source locators: Section IV; Tables III–IV

## Problem
Control a real quadrotor using latent dynamics trained in simulation.

## Intuition
Imagine motion in a compressed space, then translate it back into physical states so a controller can evaluate trajectory costs.

## Mechanism
Encodes histories of estimated full states and motor actions, rolls latent dynamics forward, and uses a physics-inspired state prober inside MPPI.

## Objective / pipeline
state/action history → latent rollout → physical-state probe → MPPI cost (pipeline).

## Training
Domain-randomized simulation; state histories include pose, velocities and attitude.

## Deployment
Estimated full-state observations and action history; not vision-only control.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### Real flight: circular tracking
Position RMSE: 0.24 m; comparator MPPI (Pred+Phys): 0.36.

Protocol: Real closed-loop tracking in the paper’s flight setup.

Uncertainty: Not extracted; do not infer significance.



Evidence: https://arxiv.org/html/2606.23444v1 — Table IV

### Open-loop prober ablation
Position error: 1.43 m; comparator JEPA with generic prober: 5.56.

Protocol: Physics-inspired versus generic prober within JEPA.

Uncertainty: Not extracted; do not infer significance.



Evidence: https://arxiv.org/html/2606.23444v1 — Table III

## Limitations
- Platform-specific sim-to-real results, not formal robust-control guarantees.
- Separate prober improvements from representation improvements.

## Next experiment — curator proposal
Ablate the prober while keeping latent dynamics fixed; record latency, model error and closed-loop cost under the same disturbances.

## Concepts
rollout, grounding, action

---

# WA-JEPA

WA-JEPA: Rethinking the Video JEPA Paradigm for World-Action Modeling in Autonomous Driving

arXiv:2608.20974 · v1 · sections_checked · checked 2026-09-26

Primary source: https://arxiv.org/html/2608.20974v1
Source locators: Method; Table 1; Table 4; Appendix C

## Problem
Couple future-scene prediction and action generation without averaging away uncertain futures.

## Intuition
Generate possible latent futures jointly with actions, rather than forcing all plausible futures into one mean representation.

## Mechanism
Future-masked video pretraining followed by joint future/action modeling with conditional flow matching.

## Objective / pipeline
Past video → future latents and actions; conditional flow-matching objective (schematic, not deterministic latent regression).

## Training
nuPlan video pretraining; NAVSIM navtrain action/world training.

## Deployment
Multi-view video history with joint future–action generation.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### NAVSIM-v2 navtest
Corrected EPDMS: 91.7 score; comparator Discrete-WAM: 90.4.

Protocol: Different backbones; stochastic evaluations use 10 seeds.

Uncertainty: Not extracted; do not infer significance.

EPDMS* 88.0 is the pre-correction aggregation; do not mix columns.

Evidence: https://arxiv.org/html/2608.20974v1 — Table 1; Appendix C

## Limitations
- Driving-specific evaluation and substantial compute.
- Stochastic predictions are not automatically calibrated risk estimates.

## Next experiment — curator proposal
At fixed inference budget compare deterministic regression with sampled latent futures; assess calibration and candidate diversity separately.

## Concepts
latent, stochastic, action

---

# JEPA-Anything

JEPA-Anything: Learning Predictive Models across Different Worlds

arXiv:2609.20800 · v1 · sections_checked · checked 2026-09-26

Primary source: https://arxiv.org/html/2609.20800v1
Source locators: Eqs. 3–10; Tables 1–3

## Problem
A single undifferentiated target can entangle different predictive factors.

## Intuition
Give several subspaces different parts of the prediction job; reconstruct a shared predicted state from their outputs.

## Mechanism
Learned projectors split a stopped-gradient target into K orthogonality-regularized factors. Factor predictors and state synthesis augment domain-specific base losses.

## Objective / pipeline
z_k = P_kᵀ stopgrad(z); L = L_base + L_factor-pred + regularizers (Eqs. 3–10, abbreviated).

## Training
Domain-specific tokenizers/backbones; EMA target encoder; factor projectors remain trainable.

## Deployment
Online features or synthesized future states feed task-specific readouts/planners.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### MuJoCo visual binding; DINOv3
Injective held-out-cell accuracy: 0.581 0–1; comparator Standard JEPA: 0.572.

Protocol: Same learned-grid readout and matched pretraining; ten seeds.

Uncertainty: Not extracted; do not infer significance.



Evidence: https://arxiv.org/html/2609.20800v1 — Tables 2–3

### Same experiment
Grid recovery: 0.659 0–1; comparator Standard JEPA: 0.645.

Protocol: Matched readout, not the supplied-grid setting.

Uncertainty: Not extracted; do not infer significance.



Evidence: https://arxiv.org/html/2609.20800v1 — Table 3

## Limitations
- Shared objective is not a single cross-domain pretrained model.
- Orthogonal factors do not automatically identify causal variables.

## Next experiment — curator proposal
Hold latent dimension and parameter count fixed; compare one predictor, multiple unconstrained heads and orthogonally regularized heads.

## Concepts
latent, factor, collapse

---

# Clin-JEPA intervention study

Intervention Granularity Matters: Coherent Treatment Bundles in Counterfactual Simulation with Clinical World Models

arXiv:2609.21906 · v1 · sections_checked · checked 2026-09-26

Primary source: https://arxiv.org/html/2609.21906v1
Source locators: Methods; Results

## Problem
Counterfactual edits may leave the support of clinically coherent treatment combinations.

## Intuition
Changing one setting while freezing all related settings can describe an implausible intervention. Compare coherent bundles instead.

## Mechanism
A frozen clinical world model compares isolated component edits with co-occurring ventilation-treatment bundles, including equal-edit-magnitude controls.

## Objective / pipeline
Compare Δz_next(bundle) against Δz_next(single edit), controlling perturbation magnitude (diagnostic, not a causal estimator).

## Training
MIMIC-IV patient trajectories; frozen Clin-JEPA used for the intervention audit.

## Deployment
Counterfactual latent-response analysis only; no treatment-policy deployment.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### Usable clinical intervention targets
Targets with bundle support: 1019 targets.

Protocol: 1,019 of 1,089 targets; next-hour analysis.

Uncertainty: Not extracted; do not infer significance.



Evidence: https://arxiv.org/html/2609.21906v1 — Results

### Equal-magnitude comparison
Quadratic bundle coefficient: 0.008 normalized latent-response model.

Protocol: Model-response association; 5,000 bootstrap resamples.

Uncertainty: 95% CI [0.005, 0.011].



Evidence: https://arxiv.org/html/2609.21906v1 — Results

## Limitations
- Predicted response is not an identified treatment effect.
- No clinical benefit or safe intervention policy established.

## Next experiment — curator proposal
For any action-conditioned model, define the valid joint intervention set before querying counterfactuals; flag extrapolated combinations.

## Concepts
decision, exogenous, latent

---

# VL-JEPA

VL-JEPA: Joint Embedding Predictive Architecture for Vision-language

arXiv:2512.10942 · v1 · sections_checked · checked 2026-09-26

Primary source: https://arxiv.org/html/2512.10942v1
Source locators: Model; Section 4.5; Figure 4

## Problem
Predict semantic answers without generating text tokens at every instant.

## Intuition
Update what the model means continuously; translate that meaning into words only when a readout is needed.

## Mechanism
Vision plus a text query predicts the target-text embedding. A separate lightweight decoder produces language selectively.

## Objective / pipeline
L = D(predicted text embedding, target text embedding); decode only on selected steps.

## Training
Embedding prediction pretraining followed by VQA supervised fine-tuning.

## Deployment
Embedding-based retrieval/classification; optional selective text decoding.

Equations use normalized notation; consult the primary source for exact definitions.

## Author-reported evidence

### Video-stream selective decoding
Decoding frequency: 0.35 Hz; comparator Uniform decoding: 1.

Protocol: Similar average CIDEr; approximately 2.85× fewer decoding operations.

Uncertainty: Not extracted; do not infer significance.

Operation count reduction, not an end-to-end latency speedup.

Evidence: https://arxiv.org/html/2512.10942v1 — Section 4.5; Figure 4

## Limitations
- 1.6B-parameter model; efficiency comparison depends on matched setup.
- Selection benchmark does not establish causally online event detection in every setting.

## Next experiment — curator proposal
Measure semantic update rate and decoder calls separately. Benchmark total latency and whether a causal trigger matches offline selection.

## Concepts
latent, decision
