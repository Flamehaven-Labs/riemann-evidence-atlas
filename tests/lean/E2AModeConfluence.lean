import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import E2APositiveStripGram

namespace E2AModeConfluence

open Filter MeasureTheory Set
open scoped Topology
open E2APositiveStrip

/-- The mode at frequency `t`, in the probability normalization `weight α / mass α`. -/
noncomputable def mode (t x : ℝ) : ℂ := Complex.exp (Complex.I * ((t * x : ℝ) : ℂ))

noncomputable def modeJet (t x : ℝ) : ℂ := (Complex.I * (x : ℂ)) * mode t x

noncomputable def dividedMode (t δ x : ℝ) : ℂ :=
  ((δ : ℂ)⁻¹) * (mode (t + δ) x - mode t x)

private theorem norm_mode (t x : ℝ) : ‖mode t x‖ = 1 :=
  Complex.norm_exp_I_mul_ofReal (t * x)

private theorem norm_modeJet (t x : ℝ) : ‖modeJet t x‖ = |x| := by
  simp [modeJet, norm_mode]

private theorem norm_dividedMode_le (t δ x : ℝ) : ‖dividedMode t δ x‖ ≤ |x| := by
  by_cases hδ : δ = 0
  · simp [hδ, dividedMode]
  have hm : mode (t + δ) x - mode t x = (mode δ x - 1) * mode t x := by
    unfold mode
    rw [add_mul, Complex.ofReal_add, mul_add, Complex.exp_add]
    ring
  have he : ‖mode δ x - 1‖ ≤ |δ| * |x| := by
    simpa [mode, Real.norm_eq_abs, abs_mul] using
      (Real.norm_exp_I_mul_ofReal_sub_one_le (x := δ * x))
  rw [dividedMode, norm_mul, norm_inv, Complex.norm_real, Real.norm_eq_abs, hm, norm_mul,
    norm_mode, mul_one]
  rw [inv_mul_eq_div, div_le_iff₀ (abs_pos.mpr hδ), mul_comm]
  exact he

theorem divided_mode_pointwise (t x : ℝ) :
    Tendsto (fun δ : ℝ ↦ dividedMode t δ x) (𝓝[>] 0) (𝓝 (modeJet t x)) := by
  have hx : HasDerivAt (fun s : ℝ ↦ Complex.I * (x : ℂ) * (s : ℂ))
      (Complex.I * (x : ℂ)) t := by
    simpa using (Complex.ofRealCLM.hasFDerivAt.hasDerivAt (x := t)).const_mul
      (Complex.I * (x : ℂ))
  have hd : HasDerivAt (fun s : ℝ ↦ mode s x) (modeJet t x) t := by
    convert hx.cexp using 1
    · ext s
      unfold mode
      push_cast
      ring_nf
    · unfold modeJet mode
      push_cast
      ring_nf
  simpa [dividedMode, slope, Algebra.smul_def, add_comm] using hd.tendsto_slope_zero_right

/-- The integral is the squared L² error for the normalized positive-strip measure. -/
noncomputable def squaredError (α : ℝ) (f g : ℝ → ℂ) : ℝ :=
  (∫ x : ℝ, ‖f x - g x‖ ^ 2 * weight α x) / mass α

theorem mode_jet_squared_norm (α t : ℝ) :
    squaredError α (modeJet t) 0 = moment2 α := by
  simp [squaredError, moment2, norm_modeJet, sq_abs]

private theorem weighted_l2_of_dominated {α : ℝ} (hα : 0 < α)
    {f : ℝ → ℝ → ℂ} {g : ℝ → ℂ} {K : ℝ}
    (hf : ∀ δ, Continuous (f δ)) (hg : Continuous g)
    (hpoint : ∀ x, Tendsto (fun δ ↦ f δ x) (𝓝[>] 0) (𝓝 (g x)))
    (hbound : ∀ᶠ δ in 𝓝[>] (0 : ℝ), ∀ x, ‖f δ x - g x‖ ≤ K * (|x| + 1)) :
    Tendsto (fun δ ↦ squaredError α (f δ) g) (𝓝[>] 0) (𝓝 0) := by
  let F (δ x : ℝ) := ‖f δ x - g x‖ ^ 2 * weight α x
  have hw : Continuous (weight α) := by
    unfold weight
    exact (by fun_prop : Continuous (fun x : ℝ ↦ Real.exp (-(2 * α) * |x|))).div
      (by fun_prop) (fun _ ↦ by positivity)
  let bound (x : ℝ) := (2 * K ^ 2) * (x ^ 2 * weight α x + weight α x)
  have h : Tendsto (fun δ : ℝ ↦ ∫ x : ℝ, F δ x) (𝓝[>] 0)
      (𝓝 (∫ _ : ℝ, (0 : ℝ))) := by
    refine tendsto_integral_filter_of_dominated_convergence
      (F := F) (f := fun _ ↦ (0 : ℝ)) bound ?_ ?_ ?_ ?_
    · exact Eventually.of_forall fun δ ↦ ((((hf δ).sub hg).norm.pow 2).mul hw).aestronglyMeasurable
    · filter_upwards [hbound] with δ hδ
      apply ae_of_all
      intro x
      have hw0 : 0 ≤ weight α x := by unfold weight; positivity
      have hb : (|x| + 1) ^ 2 ≤ 2 * (x ^ 2 + 1) := by
        nlinarith [sq_nonneg (|x| - 1), sq_abs x]
      rw [Real.norm_eq_abs, abs_of_nonneg (mul_nonneg (sq_nonneg _) hw0)]
      calc
        _ ≤ (K * (|x| + 1)) ^ 2 * weight α x :=
          mul_le_mul_of_nonneg_right (pow_le_pow_left₀ (norm_nonneg _) (hδ x) 2) hw0
        _ ≤ bound x := by
          rw [mul_pow]
          unfold bound
          calc
            _ ≤ (K ^ 2 * (2 * (x ^ 2 + 1))) * weight α x :=
              mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_left hb (sq_nonneg _)) hw0
            _ = _ := by ring
    · exact ((second_moment_integrable hα).add (weight_integrable hα)).const_mul _
    · apply ae_of_all
      intro x
      have h0 := (hpoint x).sub (tendsto_const_nhds (x := g x))
      simpa [F] using ((h0.norm.pow 2).mul_const (weight α x))
  simpa [squaredError, F] using h.div_const (mass α)

private theorem continuous_mode (s : ℝ) : Continuous (mode s) := by
  unfold mode
  exact Complex.continuous_exp.comp (by fun_prop)

private theorem continuous_jet (t : ℝ) : Continuous (modeJet t) := by
  unfold modeJet
  exact (continuous_const.mul Complex.continuous_ofReal).mul (continuous_mode t)

private theorem continuous_divided_mode (t δ : ℝ) : Continuous (dividedMode t δ) :=
  continuous_const.mul ((continuous_mode (t + δ)).sub (continuous_mode t))

private theorem norm_divided_sub_jet (t δ x : ℝ) :
    ‖dividedMode t δ x - modeJet t x‖ ≤ 2 * |x| := by
  calc
    _ ≤ ‖dividedMode t δ x‖ + ‖modeJet t x‖ := norm_sub_le _ _
    _ ≤ |x| + |x| := add_le_add (norm_dividedMode_le t δ x) (norm_modeJet t x).le
    _ = _ := by ring

theorem divided_mode_weighted_l2 {α : ℝ} (hα : 0 < α) (t : ℝ) :
    Tendsto (fun δ : ℝ ↦ squaredError α (dividedMode t δ) (modeJet t))
      (𝓝[>] 0) (𝓝 0) := by
  apply weighted_l2_of_dominated hα (continuous_divided_mode t) (continuous_jet t)
    (divided_mode_pointwise t) (K := 2)
  exact Eventually.of_forall fun δ x ↦ (norm_divided_sub_jet t δ x).trans (by linarith)

/-- The second Gram vector of the normalized pair for a nonzero Gram denominator. -/
noncomputable def gramMode (α t δ x : ℝ) : ℂ :=
  (mode (t + δ) x - (correlation α δ : ℂ) * mode t x) /
    (E2ARealGramBlock.gramDen (correlation α δ) : ℂ)

theorem gram_mode_weighted_l2 {α : ℝ} (hα : 0 < α) (t : ℝ) :
    Tendsto
      (fun δ : ℝ ↦ squaredError α (gramMode α t δ)
        (fun x ↦ modeJet t x / (Real.sqrt (moment2 α) : ℂ)))
      (𝓝[>] 0) (𝓝 0) := by
  let ρ := correlation α
  let D (δ : ℝ) := E2ARealGramBlock.gramDen (ρ δ)
  let d := Real.sqrt (moment2 α)
  have hd : 0 < d := Real.sqrt_pos.2 (moment2_pos hα)
  have hDen : Tendsto (fun δ ↦ D δ / δ) (𝓝[>] 0) (𝓝 d) :=
    strip_denominator_limit hα
  have hBase : Tendsto (fun δ : ℝ ↦ δ) (𝓝[>] 0) (𝓝 0) := nhdsWithin_le_nhds
  have hρ := correlation_deficit_limit hα
  have hNum : Tendsto (fun δ ↦ (1 - ρ δ) / δ) (𝓝[>] 0) (𝓝 0) := by
    have h := hρ.mul hBase
    simp only [mul_zero] at h
    apply h.congr'
    filter_upwards [self_mem_nhdsWithin] with δ (hδ : 0 < δ)
    change (1 - ρ δ) / δ ^ 2 * δ = (1 - ρ δ) / δ
    field_simp
  let a (δ : ℝ) := (D δ / δ)⁻¹
  let b (δ : ℝ) := ((1 - ρ δ) / δ) / (D δ / δ)
  have ha : Tendsto a (𝓝[>] 0) (𝓝 d⁻¹) := hDen.inv₀ hd.ne'
  have hb : Tendsto b (𝓝[>] 0) (𝓝 0) := by
    simpa only [b, Pi.div_def, zero_div] using hNum.div hDen hd.ne'
  let f (δ x : ℝ) := (a δ : ℂ) * dividedMode t δ x + (b δ : ℂ) * mode t x
  have hEq : ∀ᶠ δ in 𝓝[>] (0 : ℝ), f δ = gramMode α t δ := by
    filter_upwards [self_mem_nhdsWithin, hDen.eventually (eventually_gt_nhds hd)] with
      δ (hδ : 0 < δ) (hD : 0 < D δ / δ)
    have hD0 : D δ ≠ 0 := fun h ↦ by simp [h] at hD
    funext x
    simp only [f, a, b, dividedMode, Complex.ofReal_inv, Complex.ofReal_sub,
      Complex.ofReal_one, Complex.ofReal_div]
    change _ = (mode (t + δ) x - (ρ δ : ℂ) * mode t x) / (D δ : ℂ)
    field_simp [Complex.ofReal_ne_zero.mpr hδ.ne', Complex.ofReal_ne_zero.mpr hD0]
    ring
  have hg (x : ℝ) : Tendsto (fun δ ↦ f δ x) (𝓝[>] 0)
      (𝓝 (modeJet t x / (d : ℂ))) := by
    have ha' := Complex.continuous_ofReal.continuousAt.tendsto.comp ha
    have hb' := Complex.continuous_ofReal.continuousAt.tendsto.comp hb
    simpa [f, div_eq_mul_inv, mul_comm] using
      (ha'.mul (divided_mode_pointwise t x)).add (hb'.mul_const (mode t x))
  have hfa : ∀ᶠ δ in 𝓝[>] (0 : ℝ), |a δ| < d⁻¹ + 1 :=
    ha.abs.eventually (eventually_lt_nhds (by rw [abs_of_pos (inv_pos.2 hd)]; linarith))
  have hfb : ∀ᶠ δ in 𝓝[>] (0 : ℝ), |b δ| < 1 :=
    hb.abs.eventually (eventually_lt_nhds (by norm_num))
  have h := weighted_l2_of_dominated hα
    (f := f) (g := fun x ↦ modeJet t x / (d : ℂ)) (K := 2 * d⁻¹ + 2)
    (fun δ ↦ (continuous_const.mul (continuous_divided_mode t δ)).add
      (continuous_const.mul (continuous_mode t)))
    ((continuous_jet t).div_const _) hg
    (by
      filter_upwards [hfa, hfb] with δ hδa hδb
      intro x
      have hsum : ‖f δ x‖ ≤ ‖(a δ : ℂ) * dividedMode t δ x‖ +
          ‖(b δ : ℂ) * mode t x‖ := norm_add_le _ _
      calc
        _ ≤ ‖(a δ : ℂ) * dividedMode t δ x‖ + ‖(b δ : ℂ) * mode t x‖ +
            ‖modeJet t x / (d : ℂ)‖ := (norm_sub_le _ _).trans (add_le_add hsum le_rfl)
        _ ≤ (d⁻¹ + 1) * |x| + 1 + |x| / d := by
          simp only [norm_mul, norm_div, Complex.norm_real, Real.norm_eq_abs, norm_mode,
            norm_modeJet, mul_one, abs_of_pos hd]
          exact add_le_add
            (add_le_add (mul_le_mul hδa.le (norm_dividedMode_le t δ x)
              (norm_nonneg _) (by positivity)) hδb.le) le_rfl
        _ ≤ (2 * d⁻¹ + 2) * (|x| + 1) := by
          rw [div_eq_mul_inv]
          nlinarith [abs_nonneg x, (inv_pos.2 hd).le])
  exact h.congr' (hEq.mono fun δ hδ ↦ by rw [hδ])

/-- An exact identity in the basis formed by a mode and its divided difference. -/
theorem divided_block {H : Type*} [AddCommGroup H] [Module ℂ H]
    (A : H →ₗ[ℂ] H) {u v : H} {a b : ℂ} (δ : ℝ)
    (hu : A u = a • u) (hv : A v = b • v) :
    A ((δ : ℂ)⁻¹ • (v - u)) =
      ((δ : ℂ)⁻¹ * (b - a)) • u + b • ((δ : ℂ)⁻¹ • (v - u)) := by
  simp only [map_smul, map_sub, hu, hv, smul_sub, smul_smul]
  module

/-- The divided-difference basis gives an upper triangular limit with entry `m'`. -/
theorem divided_block_entry_limit {m : ℝ → ℂ} {t : ℝ} {m' : ℂ}
    (hm : HasDerivAt m m' t) :
    Tendsto (fun δ : ℝ ↦ (m (t + δ), (δ : ℂ)⁻¹ * (m (t + δ) - m t)))
      (𝓝[>] 0) (𝓝 (m t, m')) := by
  have hs : Tendsto (fun δ : ℝ ↦ (δ : ℂ)⁻¹ * (m (t + δ) - m t))
      (𝓝[>] 0) (𝓝 m') := by
    simpa [slope, Algebra.smul_def, add_comm] using hm.tendsto_slope_zero_right
  have h0 : Tendsto (fun δ : ℝ ↦ δ) (𝓝[>] 0) (𝓝 0) := nhdsWithin_le_nhds
  have ht : Tendsto (fun δ : ℝ ↦ t + δ) (𝓝[>] 0) (𝓝 t) := by
    simpa using (tendsto_const_nhds (x := t)).add h0
  exact (hm.continuousAt.tendsto.comp ht).prodMk_nhds hs

private def nilpotentPart (m' : ℂ) (z : ℂ × ℂ) : ℂ × ℂ := (m' * z.2, 0)

/-- Subtracting the limiting eigenvalue leaves a square-zero map, nonzero exactly
when the multiplier derivative is nonzero. -/
theorem limiting_block_nilpotent (m' : ℂ) :
    (∀ z, nilpotentPart m' (nilpotentPart m' z) = 0) ∧
    (nilpotentPart m' ≠ 0 ↔ m' ≠ 0) := by
  constructor
  · intro z
    simp [nilpotentPart]
  · constructor
    · intro h hzero
      exact h (by ext z <;> simp [nilpotentPart, hzero])
    · intro h hzero
      have hz := congrFun hzero (0, 1)
      exact h (by simpa [nilpotentPart] using congrArg Prod.fst hz)

end E2AModeConfluence

#print axioms E2AModeConfluence.divided_mode_pointwise
#print axioms E2AModeConfluence.mode_jet_squared_norm
#print axioms E2AModeConfluence.divided_mode_weighted_l2
#print axioms E2AModeConfluence.gram_mode_weighted_l2
#print axioms E2AModeConfluence.divided_block
#print axioms E2AModeConfluence.divided_block_entry_limit
#print axioms E2AModeConfluence.limiting_block_nilpotent
