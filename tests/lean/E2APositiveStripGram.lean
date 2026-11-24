import Mathlib.Analysis.Calculus.Deriv.Slope
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Analysis.SpecialFunctions.ImproperIntegrals
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Sinc
import Mathlib.MeasureTheory.Integral.DominatedConvergence
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Module
import Mathlib.Tactic.Ring

namespace E2APositiveStrip

open Filter MeasureTheory Set
open scoped Topology

noncomputable def weight (α x : ℝ) : ℝ :=
  Real.exp (-(2 * α) * |x|) / (1 + x ^ 2)

noncomputable def mass (α : ℝ) : ℝ :=
  ∫ x : ℝ, weight α x

noncomputable def moment2 (α : ℝ) : ℝ :=
  (∫ x : ℝ, x ^ 2 * weight α x) / mass α

noncomputable def correlation (α δ : ℝ) : ℝ :=
  (∫ x : ℝ, Real.cos (δ * x) * weight α x) / mass α

private theorem weight_pos (α x : ℝ) : 0 < weight α x := by
  unfold weight
  positivity

private theorem continuous_weight (α : ℝ) : Continuous (weight α) := by
  unfold weight
  exact (by fun_prop : Continuous (fun x : ℝ ↦ Real.exp (-(2 * α) * |x|))).div
    (by fun_prop) (fun _ ↦ by positivity)

private theorem envelope_integrable {α : ℝ} (hα : 0 < α) :
    Integrable (fun x : ℝ ↦ Real.exp (-(2 * α) * |x|)) := by
  rw [← integrableOn_univ, ← Iic_union_Ioi (a := (0 : ℝ)), integrableOn_union]
  constructor
  · apply (integrableOn_exp_mul_Iic (a := 2 * α) (by positivity) 0).congr_fun _ measurableSet_Iic
    intro x hx
    change Real.exp (2 * α * x) = Real.exp (-(2 * α) * |x|)
    rw [abs_of_nonpos (mem_Iic.mp hx)]
    congr 1
    ring
  · apply (integrableOn_exp_mul_Ioi (a := -(2 * α)) (by linarith) 0).congr_fun _ measurableSet_Ioi
    intro x hx
    change Real.exp (-(2 * α) * x) = Real.exp (-(2 * α) * |x|)
    rw [abs_of_nonneg (mem_Ioi.mp hx).le]

theorem weight_integrable {α : ℝ} (hα : 0 < α) : Integrable (weight α) := by
  refine (envelope_integrable hα).mono' (continuous_weight α).aestronglyMeasurable
    (ae_of_all _ fun x ↦ ?_)
  rw [Real.norm_eq_abs, abs_of_pos (weight_pos α x), weight]
  apply (div_le_iff₀ (by positivity)).2
  nlinarith [mul_nonneg (Real.exp_pos (-(2 * α) * |x|)).le (sq_nonneg x)]

theorem second_moment_integrable {α : ℝ} (hα : 0 < α) :
    Integrable (fun x : ℝ ↦ x ^ 2 * weight α x) := by
  have hc := (continuous_id.pow 2).mul (continuous_weight α)
  refine (envelope_integrable hα).mono' hc.aestronglyMeasurable (ae_of_all _ fun x ↦ ?_)
  rw [Real.norm_eq_abs, abs_of_nonneg (mul_nonneg (sq_nonneg x) (weight_pos α x).le),
    weight, ← mul_div_assoc]
  apply (div_le_iff₀ (by positivity)).2
  nlinarith [Real.exp_pos (-(2 * α) * |x|)]

theorem mass_pos {α : ℝ} (hα : 0 < α) : 0 < mass α :=
  integral_pos_of_integrable_nonneg_nonzero (x := (0 : ℝ))
    (continuous_weight α) (weight_integrable hα) (fun x ↦ (weight_pos α x).le)
    (weight_pos α 0).ne'

theorem moment2_pos {α : ℝ} (hα : 0 < α) : 0 < moment2 α := by
  apply div_pos _ (mass_pos hα)
  apply integral_pos_of_integrable_nonneg_nonzero (x := (1 : ℝ))
    ((continuous_id.pow 2).mul (continuous_weight α)) (second_moment_integrable hα)
    (fun x ↦ mul_nonneg (sq_nonneg x) (weight_pos α x).le)
  simpa using (weight_pos α 1).ne'

private theorem mul_sinc (y : ℝ) : y * Real.sinc y = Real.sin y := by
  by_cases hy : y = 0
  · simp [hy]
  · rw [Real.sinc_of_ne_zero hy]
    field_simp

/-- This form removes the apparent singularity of the cosine deficit at zero. -/
private theorem deficit_eq {δ : ℝ} (hδ : δ ≠ 0) (x : ℝ) :
    (1 - Real.cos (δ * x)) / δ ^ 2 = x ^ 2 / 2 * Real.sinc (δ * x / 2) ^ 2 := by
  have hc : Real.cos (δ * x) = 1 - 2 * Real.sin (δ * x / 2) ^ 2 := by
    simpa only [show 2 * (δ * x / 2) = δ * x by ring] using
      Real.cos_two_mul_eq_one_sub (δ * x / 2)
  rw [hc, ← mul_sinc (δ * x / 2)]
  field_simp
  ring

private theorem cosine_integrable {α : ℝ} (hα : 0 < α) (δ : ℝ) :
    Integrable (fun x : ℝ ↦ Real.cos (δ * x) * weight α x) := by
  have hc : Continuous (fun x : ℝ ↦ Real.cos (δ * x) * weight α x) :=
    (Real.continuous_cos.comp (by fun_prop)).mul (continuous_weight α)
  refine (weight_integrable hα).mono' hc.aestronglyMeasurable (ae_of_all _ fun x ↦ ?_)
  rw [norm_mul, Real.norm_eq_abs, Real.norm_eq_abs, abs_of_pos (weight_pos α x)]
  simpa using mul_le_mul_of_nonneg_right (Real.abs_cos_le_one (δ * x)) (weight_pos α x).le

theorem correlation_deficit_limit {α : ℝ} (hα : 0 < α) :
    Tendsto (fun δ : ℝ ↦ (1 - correlation α δ) / δ ^ 2) (𝓝[>] 0)
      (𝓝 (moment2 α / 2)) := by
  let q (x : ℝ) : ℝ := x ^ 2 * weight α x / 2
  let F (δ x : ℝ) : ℝ := q x * Real.sinc (δ * x / 2) ^ 2
  have hq : Integrable q := (second_moment_integrable hα).div_const 2
  have hcq : Continuous q := ((continuous_id.pow 2).mul (continuous_weight α)).div_const 2
  have hq_nonneg (x : ℝ) : 0 ≤ q x :=
    div_nonneg (mul_nonneg (sq_nonneg x) (weight_pos α x).le) (by positivity)
  have hF : Tendsto (fun δ : ℝ ↦ ∫ x : ℝ, F δ x) (𝓝[>] 0) (𝓝 (∫ x : ℝ, q x)) := by
    apply tendsto_integral_filter_of_dominated_convergence q
    · apply Eventually.of_forall
      intro δ
      have hcs : Continuous (fun x : ℝ ↦ Real.sinc (δ * x / 2)) := by fun_prop
      have hc : Continuous (F δ) := hcq.mul (hcs.pow 2)
      exact hc.aestronglyMeasurable
    · apply Eventually.of_forall
      intro δ
      apply ae_of_all
      intro x
      have hs : Real.sinc (δ * x / 2) ^ 2 ≤ 1 := by
        simpa using (sq_le_sq).2 (by simpa using Real.abs_sinc_le_one (δ * x / 2) :
          |Real.sinc (δ * x / 2)| ≤ |(1 : ℝ)|)
      change ‖q x * Real.sinc (δ * x / 2) ^ 2‖ ≤ q x
      rw [Real.norm_eq_abs, abs_of_nonneg (mul_nonneg (hq_nonneg x) (sq_nonneg _))]
      simpa using mul_le_mul_of_nonneg_left hs (hq_nonneg x)
    · exact hq
    · apply ae_of_all
      intro x
      have hc : Continuous (fun δ : ℝ ↦ F δ x) := by unfold F; fun_prop
      have ht : Tendsto (fun δ : ℝ ↦ F δ x) (𝓝[>] 0) (𝓝 (F 0 x)) :=
        hc.continuousAt.tendsto.mono_left nhdsWithin_le_nhds
      simpa [F] using ht
  have ht := hF.div_const (mass α)
  have htarget : (∫ x : ℝ, q x) / mass α = moment2 α / 2 := by
    change (∫ x : ℝ, (x ^ 2 * weight α x) / 2) / mass α = moment2 α / 2
    rw [integral_div, moment2]
    ring
  rw [htarget] at ht
  apply ht.congr'
  filter_upwards [self_mem_nhdsWithin] with δ (hδ : 0 < δ)
  have hpoint (x : ℝ) :
      F δ x = (weight α x - Real.cos (δ * x) * weight α x) / δ ^ 2 := by
    have h := deficit_eq hδ.ne' x
    calc
      F δ x = ((1 - Real.cos (δ * x)) / δ ^ 2) * weight α x := by rw [h]; unfold F q; ring
      _ = _ := by ring
  simp_rw [hpoint]
  rw [integral_div, integral_sub (weight_integrable hα) (cosine_integrable hα δ), correlation]
  change (mass α - _) / δ ^ 2 / mass α = _
  field_simp [(mass_pos hα).ne', hδ.ne']

end E2APositiveStrip

namespace E2ARealGramBlock

open Filter Set
open scoped Topology

noncomputable def gramDen (ρ : ℝ) : ℝ := Real.sqrt (1 - ρ ^ 2)

noncomputable def gramEntry (ρ : ℝ) (a b : ℂ) : ℂ :=
  (ρ : ℂ) * (b - a) / (gramDen ρ : ℂ)

theorem real_gram_block {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A : H →ₗ[ℂ] H) {u v : H} {a b : ℂ} {ρ : ℝ} (hρ : |ρ| < 1)
    (hu : inner ℂ u u = 1) (hv : inner ℂ v v = 1) (huv : inner ℂ u v = (ρ : ℂ))
    (hAu : A u = a • u) (hAv : A v = b • v) :
    ∃ e : H, inner ℂ u e = 0 ∧ inner ℂ e e = 1 ∧
      v = (ρ : ℂ) • u + (gramDen ρ : ℂ) • e ∧
      A u = a • u ∧ A e = gramEntry ρ a b • u + b • e := by
  let r : ℂ := ρ
  let D : ℂ := gramDen ρ
  let w : H := v - r • u
  have hpos : 0 < 1 - ρ ^ 2 := by
    have hs : ρ ^ 2 < (1 : ℝ) ^ 2 := (sq_lt_sq).2 (by simpa using hρ)
    nlinarith
  have hD : D ≠ 0 := Complex.ofReal_ne_zero.mpr (Real.sqrt_pos.2 hpos).ne'
  have hstarD : (starRingEnd ℂ) D = D := Complex.conj_ofReal _
  have hstarr : (starRingEnd ℂ) r = r := Complex.conj_ofReal _
  change inner ℂ u v = r at huv
  have hvu : inner ℂ v u = r := by
    rw [← inner_conj_symm, huv, hstarr]
  have huw : inner ℂ u w = 0 := by
    change inner ℂ u (v - r • u) = 0
    rw [inner_sub_right, huv, inner_smul_right, hu, mul_one, sub_self]
  have hvw : inner ℂ v w = 1 - r ^ 2 := by
    change inner ℂ v (v - r • u) = 1 - r ^ 2
    rw [inner_sub_right, hv, inner_smul_right, hvu, pow_two]
  have hww : inner ℂ w w = D ^ 2 := by
    change inner ℂ (v - r • u) w = ((gramDen ρ : ℝ) : ℂ) ^ 2
    rw [inner_sub_left, hvw, inner_smul_left, huw, mul_zero, sub_zero]
    simpa only [r, gramDen, Complex.ofReal_sub, Complex.ofReal_one, Complex.ofReal_pow] using
      congrArg Complex.ofReal (Real.sq_sqrt hpos.le).symm
  refine ⟨D⁻¹ • w, ?_, ?_, ?_, hAu, ?_⟩
  · rw [inner_smul_right, huw, mul_zero]
  · rw [inner_smul_left, inner_smul_right, map_inv₀, hstarD, hww]
    field_simp [hD]
  · change v = r • u + D • (D⁻¹ • (v - r • u))
    rw [smul_smul, mul_inv_cancel₀ hD, one_smul, add_sub_cancel]
  · change A (D⁻¹ • (v - r • u)) = (r * (b - a) / D) • u + b • D⁻¹ • (v - r • u)
    simp only [map_smul, map_sub, hAu, hAv, smul_sub, smul_smul, div_eq_mul_inv]
    module

private theorem gap_tendsto_zero :
    Tendsto (fun δ : ℝ ↦ δ) (𝓝[>] 0) (𝓝 0) :=
  tendsto_id.mono_left nhdsWithin_le_nhds

private theorem gram_tendsto_one {ρ : ℝ → ℝ} {M : ℝ}
    (h : Tendsto (fun δ ↦ (1 - ρ δ) / δ ^ 2) (𝓝[>] 0) (𝓝 (M / 2))) :
    Tendsto ρ (𝓝[>] 0) (𝓝 1) := by
  have hz := h.mul (gap_tendsto_zero.pow 2)
  have hdeficit : Tendsto (fun δ ↦ 1 - ρ δ) (𝓝[>] 0) (𝓝 0) := by
    simp only [zero_pow (by decide : (2 : ℕ) ≠ 0), mul_zero] at hz
    apply hz.congr'
    filter_upwards [self_mem_nhdsWithin] with δ (hδ : 0 < δ)
    exact div_mul_cancel₀ _ (pow_ne_zero _ hδ.ne')
  have h1 := (tendsto_const_nhds (x := (1 : ℝ))).sub hdeficit
  simpa only [sub_zero, sub_sub_cancel] using h1

private theorem gram_eventually_between {ρ : ℝ → ℝ} {M : ℝ} (hM : 0 < M)
    (h : Tendsto (fun δ ↦ (1 - ρ δ) / δ ^ 2) (𝓝[>] 0) (𝓝 (M / 2))) :
    ∀ᶠ δ in 𝓝[>] 0, 0 < ρ δ ∧ ρ δ < 1 := by
  filter_upwards [(gram_tendsto_one h).eventually (eventually_gt_nhds zero_lt_one),
    h.eventually (eventually_gt_nhds (half_pos hM)), self_mem_nhdsWithin] with δ hpos hquot (hδ : 0 < δ)
  have hp : 0 < (1 - ρ δ) / δ ^ 2 := hquot
  have hn : 0 < 1 - ρ δ := (div_pos_iff_of_pos_right (pow_pos hδ _)).1 hp
  exact ⟨hpos, sub_pos.mp hn⟩

theorem gram_den_scaled_limit {ρ : ℝ → ℝ} {M : ℝ} (hM : 0 < M)
    (h : Tendsto (fun δ ↦ (1 - ρ δ) / δ ^ 2) (𝓝[>] 0) (𝓝 (M / 2))) :
    Tendsto (fun δ ↦ gramDen (ρ δ) / δ) (𝓝[>] 0) (𝓝 (Real.sqrt M)) := by
  have hsum := (tendsto_const_nhds (x := (1 : ℝ))).add (gram_tendsto_one h)
  have hprod := h.mul hsum
  rw [show M / 2 * (1 + 1) = M by ring] at hprod
  apply (Real.continuous_sqrt.continuousAt.tendsto.comp hprod).congr'
  filter_upwards [gram_eventually_between hM h, self_mem_nhdsWithin] with δ hρ (hδ : 0 < δ)
  change Real.sqrt (((1 - ρ δ) / δ ^ 2) * (1 + ρ δ)) = gramDen (ρ δ) / δ
  rw [show (1 - ρ δ) / δ ^ 2 * (1 + ρ δ) = (1 - ρ δ ^ 2) / δ ^ 2 by ring,
    Real.sqrt_div' _ (sq_nonneg δ), Real.sqrt_sq hδ.le, gramDen]

theorem gram_lipschitz_bounded {ρ : ℝ → ℝ} {M K : ℝ} (hM : 0 < M) (hK : 0 ≤ K)
    (h : Tendsto (fun δ ↦ (1 - ρ δ) / δ ^ 2) (𝓝[>] 0) (𝓝 (M / 2)))
    {a b : ℝ → ℂ} (hdiff : ∀ᶠ δ in 𝓝[>] 0, ‖b δ - a δ‖ ≤ K * δ) :
    ∀ᶠ δ in 𝓝[>] 0, ‖gramEntry (ρ δ) (a δ) (b δ)‖ ≤ 2 * K / Real.sqrt M := by
  have hs := Real.sqrt_pos.2 hM
  have hhalf : Real.sqrt M / 2 < Real.sqrt M := by linarith
  filter_upwards [gram_eventually_between hM h, self_mem_nhdsWithin, hdiff,
    (gram_den_scaled_limit hM h).eventually (eventually_gt_nhds hhalf)] with δ hρ (hδ : 0 < δ) hb hden
  have hsmall : Real.sqrt M / 2 * δ < gramDen (ρ δ) := (lt_div_iff₀ hδ).1 hden
  have hbig : 0 < gramDen (ρ δ) := (by positivity : 0 < Real.sqrt M / 2 * δ).trans hsmall
  rw [gramEntry, norm_div, norm_mul, Complex.norm_real, Complex.norm_real, Real.norm_eq_abs,
    Real.norm_eq_abs, abs_of_pos hρ.1, abs_of_pos hbig]
  apply (div_le_iff₀ hbig).2
  calc
    ρ δ * ‖b δ - a δ‖ ≤ 1 * ‖b δ - a δ‖ :=
      mul_le_mul_of_nonneg_right hρ.2.le (norm_nonneg _)
    _ ≤ K * δ := by simpa using hb
    _ = (2 * K / Real.sqrt M) * (Real.sqrt M / 2 * δ) := by field_simp
    _ ≤ _ := mul_le_mul_of_nonneg_left hsmall.le (by positivity)

theorem gram_derivative_limit {ρ : ℝ → ℝ} {M : ℝ} (hM : 0 < M)
    (h : Tendsto (fun δ ↦ (1 - ρ δ) / δ ^ 2) (𝓝[>] 0) (𝓝 (M / 2)))
    {m : ℝ → ℂ} {t : ℝ} {m' : ℂ} (hm : HasDerivAt m m' t) :
    Tendsto (fun δ ↦ gramEntry (ρ δ) (m t) (m (t + δ))) (𝓝[>] 0)
      (𝓝 (m' / (Real.sqrt M : ℂ))) := by
  have hs := Real.sqrt_pos.2 hM
  have hquot : Tendsto (fun δ : ℝ ↦ (m (t + δ) - m t) / (δ : ℂ)) (𝓝[>] 0) (𝓝 m') := by
    refine hm.tendsto_slope_zero_right.congr fun δ ↦ ?_
    simp [Algebra.smul_def, div_eq_mul_inv, mul_comm]
  have hρ : Tendsto (fun δ ↦ (ρ δ : ℂ)) (𝓝[>] 0) (𝓝 1) := by
    simpa only [Complex.ofReal_one, Function.comp_def] using
      (Complex.continuous_ofReal.continuousAt.tendsto.comp (gram_tendsto_one h))
  have hD := Complex.continuous_ofReal.continuousAt.tendsto.comp (gram_den_scaled_limit hM h)
  have ht := (hρ.mul hquot).div hD (Complex.ofReal_ne_zero.mpr hs.ne')
  simp only [one_mul] at ht
  apply ht.congr'
  filter_upwards [self_mem_nhdsWithin, gram_eventually_between hM h] with δ (hδ : 0 < δ) hr
  change (ρ δ : ℂ) * ((m (t + δ) - m t) / (δ : ℂ)) /
    ((gramDen (ρ δ) / δ : ℝ) : ℂ) = gramEntry (ρ δ) (m t) (m (t + δ))
  have hDn : gramDen (ρ δ) ≠ 0 := by
    apply (Real.sqrt_pos.2 _).ne'
    have hp := mul_pos (sub_pos.mpr hr.2) (by linarith [hr.1] : 0 < 1 + ρ δ)
    nlinarith
  rw [Complex.ofReal_div, gramEntry]
  field_simp [Complex.ofReal_ne_zero.mpr hδ.ne', Complex.ofReal_ne_zero.mpr hDn]

theorem gram_fixed_jump_diverges {ρ : ℝ → ℝ} {M : ℝ} (hM : 0 < M)
    (h : Tendsto (fun δ ↦ (1 - ρ δ) / δ ^ 2) (𝓝[>] 0) (𝓝 (M / 2))) :
    Tendsto (fun δ ↦ ‖gramEntry (ρ δ) 0 1‖) (𝓝[>] 0) atTop := by
  have hD := (gram_den_scaled_limit hM h).mul gap_tendsto_zero
  have hzero : Tendsto (fun δ ↦ gramDen (ρ δ)) (𝓝[>] 0) (𝓝 0) := by
    rw [mul_zero] at hD
    apply hD.congr'
    filter_upwards [self_mem_nhdsWithin] with δ (hδ : 0 < δ)
    exact div_mul_cancel₀ _ hδ.ne'
  have hpos : ∀ᶠ δ in 𝓝[>] 0, 0 < ρ δ ∧ 0 < gramDen (ρ δ) := by
    filter_upwards [gram_eventually_between hM h] with δ hr
    refine ⟨hr.1, Real.sqrt_pos.2 ?_⟩
    have hp := mul_pos (sub_pos.mpr hr.2) (by linarith [hr.1] : 0 < 1 + ρ δ)
    nlinarith
  have hratio : Tendsto (fun δ ↦ gramDen (ρ δ) / ρ δ) (𝓝[>] 0) (𝓝[>] 0) := by
    apply tendsto_nhdsWithin_iff.2
    refine ⟨?_, ?_⟩
    · simpa only [Pi.div_def, zero_div] using hzero.div (gram_tendsto_one h) one_ne_zero
    · exact hpos.mono (fun _ hp ↦ div_pos hp.2 hp.1)
  apply (tendsto_inv_nhdsGT_zero.comp hratio).congr'
  filter_upwards [hpos] with δ hp
  simp [gramEntry, Complex.norm_real, Real.norm_eq_abs, abs_of_pos hp.1,
    abs_of_pos hp.2, inv_div]

end E2ARealGramBlock

namespace E2APositiveStrip

open Filter Set E2ARealGramBlock
open scoped Topology

theorem correlation_deficit_bounds {α : ℝ} (hα : 0 < α) :
    ∀ᶠ δ in 𝓝[>] 0, (moment2 α / 4) * δ ^ 2 ≤ 1 - correlation α δ ∧
      1 - correlation α δ ≤ (3 * moment2 α / 4) * δ ^ 2 := by
  have hp := moment2_pos hα
  have hlo : moment2 α / 4 < moment2 α / 2 := by linarith
  have hhi : moment2 α / 2 < 3 * moment2 α / 4 := by linarith
  have ht := correlation_deficit_limit hα
  filter_upwards [ht.eventually (eventually_gt_nhds hlo),
    ht.eventually (eventually_lt_nhds hhi), self_mem_nhdsWithin] with δ hl hh (hδ : 0 < δ)
  exact ⟨(le_div_iff₀ (pow_pos hδ 2)).1 hl.le, (div_le_iff₀ (pow_pos hδ 2)).1 hh.le⟩

theorem strip_denominator_limit {α : ℝ} (hα : 0 < α) :
    Tendsto (fun δ ↦ gramDen (correlation α δ) / δ) (𝓝[>] 0)
      (𝓝 (Real.sqrt (moment2 α))) :=
  gram_den_scaled_limit (moment2_pos hα) (correlation_deficit_limit hα)

theorem strip_lipschitz_bounded {α K : ℝ} (hα : 0 < α) (hK : 0 ≤ K)
    {a b : ℝ → ℂ} (hdiff : ∀ᶠ δ in 𝓝[>] 0, ‖b δ - a δ‖ ≤ K * δ) :
    ∀ᶠ δ in 𝓝[>] 0, ‖gramEntry (correlation α δ) (a δ) (b δ)‖ ≤
      2 * K / Real.sqrt (moment2 α) :=
  gram_lipschitz_bounded (moment2_pos hα) hK (correlation_deficit_limit hα) hdiff

theorem strip_derivative_limit {α : ℝ} (hα : 0 < α)
    {m : ℝ → ℂ} {t : ℝ} {m' : ℂ} (hm : HasDerivAt m m' t) :
    Tendsto (fun δ ↦ gramEntry (correlation α δ) (m t) (m (t + δ))) (𝓝[>] 0)
      (𝓝 (m' / (Real.sqrt (moment2 α) : ℂ))) :=
  gram_derivative_limit (moment2_pos hα) (correlation_deficit_limit hα) hm

theorem strip_linear_multiplier_nonzero_limit {α : ℝ} (hα : 0 < α) :
    Tendsto (fun δ : ℝ ↦ gramEntry (correlation α δ) 0 (δ : ℂ)) (𝓝[>] 0)
      (𝓝 (1 / (Real.sqrt (moment2 α) : ℂ))) ∧
      (1 / (Real.sqrt (moment2 α) : ℂ)) ≠ 0 := by
  have hne := Complex.ofReal_ne_zero.mpr (Real.sqrt_pos.2 (moment2_pos hα)).ne'
  refine ⟨?_, one_div_ne_zero hne⟩
  have hρ : Tendsto (fun δ ↦ (correlation α δ : ℂ)) (𝓝[>] 0) (𝓝 1) := by
    simpa only [Complex.ofReal_one, Function.comp_def] using
      (Complex.continuous_ofReal.continuousAt.tendsto.comp
        (gram_tendsto_one (correlation_deficit_limit hα)))
  have hD := Complex.continuous_ofReal.continuousAt.tendsto.comp (strip_denominator_limit hα)
  apply (hρ.div hD hne).congr
  intro δ
  change (correlation α δ : ℂ) / ((gramDen (correlation α δ) / δ : ℝ) : ℂ) =
    gramEntry (correlation α δ) 0 (δ : ℂ)
  rw [Complex.ofReal_div, div_div_eq_mul_div, gramEntry, sub_zero]

theorem strip_fixed_jump_diverges {α : ℝ} (hα : 0 < α) :
    Tendsto (fun δ ↦ ‖gramEntry (correlation α δ) 0 1‖) (𝓝[>] 0) atTop :=
  gram_fixed_jump_diverges (moment2_pos hα) (correlation_deficit_limit hα)

end E2APositiveStrip

#print axioms E2APositiveStrip.weight_integrable
#print axioms E2APositiveStrip.second_moment_integrable
#print axioms E2APositiveStrip.mass_pos
#print axioms E2APositiveStrip.moment2_pos
#print axioms E2APositiveStrip.correlation_deficit_limit
#print axioms E2APositiveStrip.correlation_deficit_bounds
#print axioms E2ARealGramBlock.real_gram_block
#print axioms E2APositiveStrip.strip_denominator_limit
#print axioms E2APositiveStrip.strip_lipschitz_bounded
#print axioms E2APositiveStrip.strip_derivative_limit
#print axioms E2APositiveStrip.strip_linear_multiplier_nonzero_limit
#print axioms E2APositiveStrip.strip_fixed_jump_diverges

