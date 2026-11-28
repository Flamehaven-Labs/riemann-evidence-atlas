import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import E2AModeConfluence

namespace E2AMellinTranslation

open Filter MeasureTheory Set E2APositiveStrip E2AModeConfluence
open scoped Topology

/-- The plus sign in the translation fixes the sign of the multiplier. -/
noncomputable def translateIntegral (k f : ℝ → ℂ) (x : ℝ) : ℂ :=
  ∫ y : ℝ, k y * f (x + y)

noncomputable def multiplier (k : ℝ → ℂ) (t : ℝ) : ℂ :=
  ∫ y : ℝ, k y * mode t y

noncomputable def multiplierJet (k : ℝ → ℂ) (t : ℝ) : ℂ :=
  ∫ y : ℝ, k y * modeJet t y

private theorem mode_add (t x y : ℝ) : mode t (x + y) = mode t x * mode t y := by
  unfold mode
  rw [mul_add, Complex.ofReal_add, mul_add, Complex.exp_add]

private theorem mode_norm (t x : ℝ) : ‖mode t x‖ = 1 :=
  Complex.norm_exp_I_mul_ofReal (t * x)

private theorem modeJet_norm (t x : ℝ) : ‖modeJet t x‖ = |x| := by
  simp [modeJet, mode_norm]

private theorem mode_continuous (t : ℝ) : Continuous (mode t) :=
  Complex.continuous_exp.comp (by fun_prop)

private theorem modeJet_continuous (t : ℝ) : Continuous (modeJet t) := by
  unfold modeJet
  exact (continuous_const.mul Complex.continuous_ofReal).mul (mode_continuous t)

private theorem hasDerivAt_mode (t x : ℝ) :
    HasDerivAt (fun s : ℝ ↦ mode s x) (modeJet t x) t := by
  have hx : HasDerivAt (fun s : ℝ ↦ Complex.I * (x : ℂ) * (s : ℂ))
      (Complex.I * (x : ℂ)) t := by
    simpa using (Complex.ofRealCLM.hasFDerivAt.hasDerivAt (x := t)).const_mul
      (Complex.I * (x : ℂ))
  convert hx.cexp using 1
  · ext s
    unfold mode
    push_cast
    ring_nf
  · unfold modeJet mode
    push_cast
    ring_nf

private theorem integrable_kernel_mode {k : ℝ → ℂ} (hk : Integrable k) (t : ℝ) :
    Integrable (fun y ↦ k y * mode t y) := by
  exact hk.norm.mono' (hk.aestronglyMeasurable.mul (mode_continuous t).aestronglyMeasurable)
    (ae_of_all _ fun y ↦ by rw [norm_mul, mode_norm, mul_one])

private theorem integrable_kernel_jet {k : ℝ → ℂ} (hk : Integrable k)
    (h1 : Integrable (fun y ↦ ‖k y‖ * |y|)) (t : ℝ) :
    Integrable (fun y ↦ k y * modeJet t y) := by
  exact h1.mono' (hk.aestronglyMeasurable.mul (modeJet_continuous t).aestronglyMeasurable)
    (ae_of_all _ fun y ↦ by rw [norm_mul, modeJet_norm])

private theorem divided_norm_le (t δ y : ℝ) : ‖dividedMode t δ y‖ ≤ |y| := by
  by_cases hδ : δ = 0
  · simp [dividedMode, hδ]
  have hmode : mode (t + δ) y - mode t y = (mode δ y - 1) * mode t y := by
    unfold mode
    rw [add_mul, Complex.ofReal_add, mul_add, Complex.exp_add]
    ring
  have hdiff : ‖mode δ y - 1‖ ≤ |δ| * |y| := by
    simpa [mode, Real.norm_eq_abs, abs_mul] using
      (Real.norm_exp_I_mul_ofReal_sub_one_le (x := δ * y))
  rw [dividedMode, norm_mul, norm_inv, Complex.norm_real, Real.norm_eq_abs,
    hmode, norm_mul, mode_norm, mul_one, inv_mul_eq_div, div_le_iff₀ (abs_pos.mpr hδ),
    mul_comm]
  exact hdiff

private theorem integrable_kernel_divided {k : ℝ → ℂ} (hk : Integrable k)
    (h1 : Integrable (fun y ↦ ‖k y‖ * |y|)) (t δ : ℝ) :
    Integrable (fun y ↦ k y * dividedMode t δ y) := by
  have hc : Continuous (dividedMode t δ) :=
    continuous_const.mul ((mode_continuous (t + δ)).sub (mode_continuous t))
  refine h1.mono' (hk.aestronglyMeasurable.mul hc.aestronglyMeasurable) (ae_of_all _ fun y ↦ ?_)
  rw [norm_mul]
  exact mul_le_mul_of_nonneg_left (divided_norm_le t δ y) (norm_nonneg _)

theorem multiplier_hasDerivAt {k : ℝ → ℂ} (hk : Integrable k)
    (h1 : Integrable (fun y ↦ ‖k y‖ * |y|)) (t : ℝ) :
    HasDerivAt (multiplier k) (multiplierJet k t) t := by
  apply hasDerivAt_iff_tendsto_slope_zero.mpr
  have hd : Tendsto (fun δ : ℝ ↦ ∫ y : ℝ, k y * dividedMode t δ y) (𝓝[≠] 0)
      (𝓝 (multiplierJet k t)) := by
    refine tendsto_integral_filter_of_dominated_convergence
      (F := fun δ y ↦ k y * dividedMode t δ y) (f := fun y ↦ k y * modeJet t y)
      (fun y ↦ ‖k y‖ * |y|) ?_ ?_ h1 ?_
    · exact Eventually.of_forall fun δ ↦ (integrable_kernel_divided hk h1 t δ).aestronglyMeasurable
    · exact Eventually.of_forall fun δ ↦ ae_of_all _ fun y ↦ by
        rw [norm_mul]
        exact mul_le_mul_of_nonneg_left (divided_norm_le t δ y) (norm_nonneg _)
    · exact ae_of_all _ fun y ↦ by
        have h : Tendsto (fun δ : ℝ ↦ dividedMode t δ y) (𝓝[≠] 0) (𝓝 (modeJet t y)) := by
          simpa [dividedMode, Algebra.smul_def] using (hasDerivAt_mode t y).tendsto_slope_zero
        exact h.const_mul (k y)
  apply hd.congr'
  apply Eventually.of_forall
  intro δ
  simp_rw [dividedMode, show ∀ y, k y * ((δ : ℂ)⁻¹ * (mode (t + δ) y - mode t y)) =
    (δ : ℂ)⁻¹ * (k y * mode (t + δ) y - k y * mode t y) from fun y ↦ by ring]
  rw [integral_const_mul, integral_sub (integrable_kernel_mode hk _) (integrable_kernel_mode hk _)]
  simp [multiplier, Algebra.smul_def]

theorem translate_mode (k : ℝ → ℂ) (t x : ℝ) :
    translateIntegral k (mode t) x = multiplier k t * mode t x := by
  unfold translateIntegral multiplier
  simp_rw [mode_add, show ∀ y, k y * (mode t x * mode t y) =
    (k y * mode t y) * mode t x from fun y ↦ by ring]
  rw [integral_mul_const]

theorem translate_jet {k : ℝ → ℂ} (hk : Integrable k)
    (h1 : Integrable (fun y ↦ ‖k y‖ * |y|)) (t x : ℝ) :
    translateIntegral k (modeJet t) x =
      multiplier k t * modeJet t x + multiplierJet k t * mode t x := by
  unfold translateIntegral multiplier multiplierJet
  have eq (y : ℝ) : k y * modeJet t (x + y) =
      (k y * mode t y) * modeJet t x + (k y * modeJet t y) * mode t x := by
    unfold modeJet
    rw [mode_add, Complex.ofReal_add]
    ring
  simp_rw [eq]
  rw [integral_add ((integrable_kernel_mode hk t).mul_const _)
    ((integrable_kernel_jet hk h1 t).mul_const _), integral_mul_const, integral_mul_const]

theorem translate_divided_mode {k : ℝ → ℂ} (hk : Integrable k) (t δ x : ℝ) :
    translateIntegral k (dividedMode t δ) x =
      multiplier k (t + δ) * dividedMode t δ x +
      ((δ : ℂ)⁻¹ * (multiplier k (t + δ) - multiplier k t)) * mode t x := by
  unfold translateIntegral dividedMode
  have eq (y : ℝ) : k y * ((δ : ℂ)⁻¹ * (mode (t + δ) (x + y) - mode t (x + y))) =
      (δ : ℂ)⁻¹ * (k y * mode (t + δ) (x + y) - k y * mode t (x + y)) := by ring
  simp_rw [eq]
  rw [integral_const_mul, integral_sub]
  · change (δ : ℂ)⁻¹ * (translateIntegral k (mode (t + δ)) x -
      translateIntegral k (mode t) x) = _
    rw [translate_mode, translate_mode]
    ring
  all_goals
    simp_rw [mode_add, show ∀ a y : ℝ, k y * (mode a x * mode a y) =
      (k y * mode a y) * mode a x from fun a y ↦ by ring]
    exact (integrable_kernel_mode hk _).mul_const _

/-- The forward integral carries the divided differences to the same L² limit
as its explicit action on the derivative mode. -/
theorem translate_divided_weighted_l2 {α : ℝ} (hα : 0 < α) {k : ℝ → ℂ}
    (hk : Integrable k) (h1 : Integrable (fun y ↦ ‖k y‖ * |y|)) (t : ℝ) :
    Tendsto (fun δ ↦ squaredError α (translateIntegral k (dividedMode t δ))
      (translateIntegral k (modeJet t))) (𝓝[>] 0) (𝓝 0) := by
  let m := multiplier k
  let m' := multiplierJet k t
  let a (δ : ℝ) := m (t + δ)
  let b (δ : ℝ) := (δ : ℂ)⁻¹ * (m (t + δ) - m t)
  let f (δ x : ℝ) := a δ * dividedMode t δ x + b δ * mode t x
  let g (x : ℝ) := m t * modeJet t x + m' * mode t x
  let F (δ x : ℝ) := ‖f δ x - g x‖ ^ 2 * weight α x
  let C := ‖m t‖ + ‖m'‖ + 1
  let bound (x : ℝ) := (8 * C ^ 2) * (x ^ 2 * weight α x + weight α x)
  have hmt := multiplier_hasDerivAt hk h1 t
  have hp : Tendsto (fun δ ↦ (a δ, b δ)) (𝓝[>] 0) (𝓝 (m t, m')) :=
    divided_block_entry_limit hmt
  have ha : Tendsto a (𝓝[>] 0) (𝓝 (m t)) := continuous_fst.continuousAt.tendsto.comp hp
  have hb : Tendsto b (𝓝[>] 0) (𝓝 m') := continuous_snd.continuousAt.tendsto.comp hp
  have ha' : ∀ᶠ δ in 𝓝[>] (0 : ℝ), ‖a δ‖ < C :=
    ha.norm.eventually (eventually_lt_nhds (by dsimp [C]; linarith [norm_nonneg m']))
  have hb' : ∀ᶠ δ in 𝓝[>] (0 : ℝ), ‖b δ‖ < C :=
    hb.norm.eventually (eventually_lt_nhds (by dsimp [C]; linarith [norm_nonneg (m t)]))
  have hw : Continuous (weight α) := by
    unfold weight
    exact (by fun_prop : Continuous (fun x : ℝ ↦ Real.exp (-(2 * α) * |x|))).div
      (by fun_prop) (fun _ ↦ by positivity)
  have h : Tendsto (fun δ : ℝ ↦ ∫ x : ℝ, F δ x) (𝓝[>] 0)
      (𝓝 (∫ _ : ℝ, (0 : ℝ))) := by
    refine tendsto_integral_filter_of_dominated_convergence
      (F := F) (f := fun _ ↦ (0 : ℝ)) bound ?_ ?_ ?_ ?_
    · exact Eventually.of_forall fun δ ↦ by
        have hq : Continuous (dividedMode t δ) :=
          continuous_const.mul ((mode_continuous (t + δ)).sub (mode_continuous t))
        have hf : Continuous (f δ) :=
          (continuous_const.mul hq).add (continuous_const.mul (mode_continuous t))
        have hg : Continuous g :=
          (continuous_const.mul (modeJet_continuous t)).add (continuous_const.mul (mode_continuous t))
        exact (((hf.sub hg).norm.pow 2).mul hw).aestronglyMeasurable
    · filter_upwards [ha', hb'] with δ hδa hδb
      apply ae_of_all
      intro x
      have hf : ‖f δ x‖ ≤ C * |x| + C := by
        calc
          _ ≤ ‖a δ * dividedMode t δ x‖ + ‖b δ * mode t x‖ := norm_add_le _ _
          _ ≤ _ := by
            rw [norm_mul, norm_mul, mode_norm, mul_one]
            exact add_le_add
              (mul_le_mul hδa.le (divided_norm_le t δ x) (norm_nonneg _) (by positivity)) hδb.le
      have hg : ‖g x‖ ≤ C * |x| + C := by
        calc
          _ ≤ ‖m t * modeJet t x‖ + ‖m' * mode t x‖ := norm_add_le _ _
          _ ≤ _ := by
            rw [norm_mul, norm_mul, mode_norm, modeJet_norm, mul_one]
            exact add_le_add (mul_le_mul_of_nonneg_right (by dsimp [C]; linarith [norm_nonneg m']) (abs_nonneg x))
              (by dsimp [C]; linarith [norm_nonneg (m t)])
      have hdiff : ‖f δ x - g x‖ ≤ 2 * C * (|x| + 1) :=
        (norm_sub_le _ _).trans ((add_le_add hf hg).trans (by ring_nf; exact le_rfl))
      have hw0 : 0 ≤ weight α x := by unfold weight; positivity
      have hsq : (|x| + 1) ^ 2 ≤ 2 * (x ^ 2 + 1) := by
        nlinarith [sq_nonneg (|x| - 1), sq_abs x]
      rw [Real.norm_eq_abs, abs_of_nonneg (mul_nonneg (sq_nonneg _) hw0)]
      calc
        _ ≤ (2 * C * (|x| + 1)) ^ 2 * weight α x :=
          mul_le_mul_of_nonneg_right (pow_le_pow_left₀ (norm_nonneg _) hdiff 2) hw0
        _ ≤ bound x := by
          rw [mul_pow]
          unfold bound
          calc
            _ ≤ ((2 * C) ^ 2 * (2 * (x ^ 2 + 1))) * weight α x :=
              mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_left hsq (sq_nonneg _)) hw0
            _ = _ := by ring
    · exact ((second_moment_integrable hα).add (weight_integrable hα)).const_mul _
    · apply ae_of_all
      intro x
      have hfg : Tendsto (fun δ ↦ f δ x) (𝓝[>] 0) (𝓝 (g x)) :=
        (ha.mul (divided_mode_pointwise t x)).add (hb.mul_const (mode t x))
      have h0 := hfg.sub (tendsto_const_nhds (x := g x))
      simpa [F] using ((h0.norm.pow 2).mul_const (weight α x))
  have h' : Tendsto (fun δ ↦ squaredError α (f δ) g) (𝓝[>] 0) (𝓝 0) := by
    simpa [squaredError, F] using h.div_const (mass α)
  apply h'.congr'
  exact Eventually.of_forall fun δ ↦ by
    have hq : translateIntegral k (dividedMode t δ) = f δ :=
      funext (translate_divided_mode hk t δ)
    have hj : translateIntegral k (modeJet t) = g :=
      funext (translate_jet hk h1 t)
    change squaredError α (f δ) g = squaredError α (translateIntegral k (dividedMode t δ))
      (translateIntegral k (modeJet t))
    rw [hq, hj]

/-- A single translation changes the weight by at most this factor.
Taking square roots gives the weighted L² shift bound. -/
theorem weight_translate_le {α : ℝ} (hα : 0 ≤ α) (x y : ℝ) :
    weight α x ≤ Real.exp ((2 * α + 1) * |y|) * weight α (x + y) := by
  let F (z : ℝ) := Real.log (1 + z ^ 2)
  have hF (z : ℝ) : HasDerivAt F (2 * z / (1 + z ^ 2)) z := by
    have hp : HasDerivAt (fun z : ℝ ↦ 1 + z ^ 2) (2 * z) z := by
      simpa [mul_comm] using ((hasDerivAt_id z).pow 2).const_add 1
    have hlog := (Real.hasDerivAt_log (by positivity : 1 + z ^ 2 ≠ 0)).comp z hp
    simpa [F, Function.comp_def, div_eq_mul_inv, mul_comm] using hlog
  have hD (z : ℝ) : ‖deriv F z‖ ≤ 1 := by
    rw [(hF z).deriv, Real.norm_eq_abs, abs_div, abs_of_pos (by positivity : 0 < 1 + z ^ 2),
      abs_mul, abs_of_nonneg (by norm_num : (0 : ℝ) ≤ 2)]
    apply (div_le_iff₀ (by positivity)).2
    nlinarith [sq_nonneg (|z| - 1), sq_abs z]
  have hDiff := (convex_univ : Convex ℝ (univ : Set ℝ)).norm_image_sub_le_of_norm_deriv_le
    (fun z _ ↦ (hF z).differentiableAt) (fun z _ ↦ hD z) (mem_univ x) (mem_univ (x + y))
  have hLog : F (x + y) - F x ≤ |y| := by
    have h := (le_abs_self (F (x + y) - F x)).trans (by simpa [Real.norm_eq_abs] using hDiff)
    exact h
  have hp (z : ℝ) : 0 < 1 + z ^ 2 := by positivity
  have hPoly : 1 + (x + y) ^ 2 ≤ Real.exp |y| * (1 + x ^ 2) := by
    have h := Real.exp_le_exp.mpr hLog
    rw [Real.exp_sub] at h
    unfold F at h
    rwa [Real.exp_log (hp _), Real.exp_log (hp _), div_le_iff₀ (hp _)] at h
  have habs : |x + y| ≤ |x| + |y| := abs_add_le x y
  have hNum : Real.exp (-(2 * α) * |x|) ≤
      Real.exp (2 * α * |y|) * Real.exp (-(2 * α) * |x + y|) := by
    rw [← Real.exp_add, Real.exp_le_exp]
    nlinarith [mul_le_mul_of_nonneg_left habs (show 0 ≤ 2 * α by positivity)]
  unfold weight
  rw [← mul_div_assoc]
  apply (div_le_div_iff₀ (hp _) (hp _)).mpr
  calc
    _ ≤ (Real.exp (2 * α * |y|) * Real.exp (-(2 * α) * |x + y|)) *
          (Real.exp |y| * (1 + x ^ 2)) :=
      mul_le_mul hNum hPoly (hp _).le (by positivity)
    _ = _ := by
      rw [show (2 * α + 1) * |y| = 2 * α * |y| + |y| by ring, Real.exp_add]
      ring

/-- Squared weighted translation norm bound for any function with integrable
weighted squared norm. -/
theorem translate_weighted_l2_le {α : ℝ} (hα : 0 < α) {f : ℝ → ℂ}
    (hf : Integrable (fun x ↦ ‖f x‖ ^ 2 * weight α x)) (y : ℝ) :
    squaredError α (fun x ↦ f (x + y)) 0 ≤
      Real.exp ((2 * α + 1) * |y|) * squaredError α f 0 := by
  let E := Real.exp ((2 * α + 1) * |y|)
  let g (x : ℝ) := ‖f x‖ ^ 2 * weight α x
  have hi : Integrable (fun x ↦ E * g (x + y)) := (hf.comp_add_right y).const_mul E
  have hmono : (∫ x : ℝ, ‖f (x + y)‖ ^ 2 * weight α x) ≤
      ∫ x : ℝ, E * g (x + y) := by
    refine integral_mono_of_nonneg (ae_of_all _ fun x ↦ mul_nonneg (sq_nonneg _) ?_) hi
      (ae_of_all _ fun x ↦ ?_)
    · unfold weight
      positivity
    · have h := mul_le_mul_of_nonneg_left (weight_translate_le hα.le x y)
          (sq_nonneg ‖f (x + y)‖)
      simpa [g, E, mul_left_comm] using h
  rw [integral_const_mul, integral_add_right_eq_self g y] at hmono
  apply (div_le_div_iff_of_pos_right (mass_pos hα)).2
    at hmono
  simpa [squaredError, E, g, mul_div_assoc] using hmono

end E2AMellinTranslation

#print axioms E2AMellinTranslation.multiplier_hasDerivAt
#print axioms E2AMellinTranslation.translate_mode
#print axioms E2AMellinTranslation.translate_jet
#print axioms E2AMellinTranslation.translate_divided_mode
#print axioms E2AMellinTranslation.translate_divided_weighted_l2
#print axioms E2AMellinTranslation.weight_translate_le
#print axioms E2AMellinTranslation.translate_weighted_l2_le
