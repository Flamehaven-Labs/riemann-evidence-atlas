import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Module
import Mathlib.Tactic.Ring

namespace E2ATwoZeroBlock

open Filter Set
open scoped Topology

noncomputable def denominator (δ : ℝ) : ℝ :=
  Real.sqrt (Real.exp (2 * δ) - 1)

noncomputable def offDiagonal (δ : ℝ) (a b : ℂ) : ℂ :=
  (b - a) / (denominator δ : ℂ)

private theorem two_mul_le_exp_sub_one (δ : ℝ) :
    2 * δ ≤ Real.exp (2 * δ) - 1 := by
  linarith [Real.add_one_le_exp (2 * δ)]

private theorem denominator_pos {δ : ℝ} (hδ : 0 < δ) : 0 < denominator δ :=
  Real.sqrt_pos.2 (lt_of_lt_of_le (by positivity) (two_mul_le_exp_sub_one δ))

/-- The displayed action on the two orthonormal vectors specifies both matrix columns. -/
theorem orthonormal_block {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A : H →ₗ[ℂ] H) {u v : H} {a b : ℂ} {δ : ℝ} (hδ : 0 < δ)
    (hu : inner ℂ u u = 1) (hv : inner ℂ v v = 1)
    (huv : inner ℂ u v = (Real.exp (-δ) : ℂ))
    (hAu : A u = a • u) (hAv : A v = b • v) :
    ∃ e : H, inner ℂ u e = 0 ∧ inner ℂ e e = 1 ∧
      v = (Real.exp (-δ) : ℂ) • (u + (denominator δ : ℂ) • e) ∧
      A u = a • u ∧ A e = offDiagonal δ a b • u + b • e := by
  let r : ℂ := (Real.exp δ : ℂ)
  let ρ : ℂ := (Real.exp (-δ) : ℂ)
  let D : ℂ := (denominator δ : ℂ)
  let w : H := r • v - u
  have hrρ : r * ρ = 1 := by
    change (Real.exp δ : ℂ) * (Real.exp (-δ) : ℂ) = 1
    rw [← Complex.ofReal_mul, ← Real.exp_add, add_neg_cancel, Real.exp_zero, Complex.ofReal_one]
  have hrρ' : ρ * r = 1 := by simpa [mul_comm] using hrρ
  have hD : D ≠ 0 := Complex.ofReal_ne_zero.mpr (denominator_pos hδ).ne'
  have hDstar : (starRingEnd ℂ) D = D := Complex.conj_ofReal _
  have hrstar : (starRingEnd ℂ) r = r := Complex.conj_ofReal _
  change inner ℂ u v = ρ at huv
  have hvu : inner ℂ v u = ρ := by
    rw [← inner_conj_symm, huv]
    exact Complex.conj_ofReal _
  have huw : inner ℂ u w = 0 := by
    change inner ℂ u (r • v - u) = 0
    rw [inner_sub_right, inner_smul_right, huv, hu, hrρ, sub_self]
  have hwv : inner ℂ v w = r - ρ := by
    change inner ℂ v (r • v - u) = r - ρ
    rw [inner_sub_right, inner_smul_right, hv, hvu, mul_one]
  have hDsq : D ^ 2 = r ^ 2 - 1 := by
    change ((denominator δ : ℝ) : ℂ) ^ 2 = (Real.exp δ : ℂ) ^ 2 - 1
    rw [← Complex.ofReal_pow, ← Complex.ofReal_pow, ← Complex.ofReal_one, ← Complex.ofReal_sub]
    congr 1
    rw [denominator, Real.sq_sqrt ((by positivity : 0 ≤ 2 * δ).trans
      (two_mul_le_exp_sub_one δ)), pow_two, ← Real.exp_add]
    congr 2
    ring
  have hww : inner ℂ w w = D ^ 2 := by
    change inner ℂ (r • v - u) w = D ^ 2
    rw [inner_sub_left, inner_smul_left, hwv, huw, hrstar, hDsq]
    linear_combination -hrρ
  refine ⟨D⁻¹ • w, ?_, ?_, ?_, hAu, ?_⟩
  · rw [inner_smul_right, huw, mul_zero]
  · rw [inner_smul_left, inner_smul_right, map_inv₀, hDstar, hww]
    field_simp [hD]
  · change v = ρ • (u + D • (D⁻¹ • (r • v - u)))
    rw [smul_smul, mul_inv_cancel₀ hD, one_smul, add_sub_cancel, smul_smul, hrρ', one_smul]
  · change A (D⁻¹ • (r • v - u)) = ((b - a) / D) • u + b • D⁻¹ • (r • v - u)
    simp only [map_smul, map_sub, hAu, hAv, smul_sub, smul_smul, div_eq_mul_inv]
    module

theorem off_diagonal_norm_le {δ K : ℝ} (hδ : 0 < δ) (hK : 0 ≤ K) {a b : ℂ}
    (hdiff : ‖b - a‖ ≤ K * δ) :
    ‖offDiagonal δ a b‖ ≤ K * Real.sqrt (δ / 2) := by
  have hD := denominator_pos hδ
  have hr : Real.sqrt (2 * δ) ≤ denominator δ :=
    Real.sqrt_le_sqrt (two_mul_le_exp_sub_one δ)
  have hproduct : Real.sqrt (δ / 2) * Real.sqrt (2 * δ) = δ := by
    rw [← Real.sqrt_mul (by positivity), show (δ / 2) * (2 * δ) = δ ^ 2 by ring,
      Real.sqrt_sq hδ.le]
  rw [offDiagonal, norm_div, Complex.norm_real, Real.norm_eq_abs, abs_of_pos hD]
  apply (div_le_iff₀ hD).2
  calc
    ‖b - a‖ ≤ K * δ := hdiff
    _ = (K * Real.sqrt (δ / 2)) * Real.sqrt (2 * δ) := by rw [mul_assoc, hproduct]
    _ ≤ (K * Real.sqrt (δ / 2)) * denominator δ := by gcongr

theorem off_diagonal_tendsto_zero (a b : ℝ → ℂ) {K : ℝ} (hK : 0 ≤ K)
    (hdiff : ∀ δ > 0, ‖b δ - a δ‖ ≤ K * δ) :
    Tendsto (fun δ ↦ offDiagonal δ (a δ) (b δ)) (𝓝[>] (0 : ℝ)) (𝓝 0) := by
  apply squeeze_zero_norm'
  · filter_upwards [self_mem_nhdsWithin] with δ hδ
    exact off_diagonal_norm_le hδ hK (hdiff δ hδ)
  · have h : Continuous (fun δ : ℝ ↦ K * Real.sqrt (δ / 2)) := by fun_prop
    have ht : Tendsto (fun δ : ℝ ↦ K * Real.sqrt (δ / 2)) (𝓝[>] (0 : ℝ))
        (𝓝 (K * Real.sqrt ((0 : ℝ) / 2))) :=
      h.continuousAt.tendsto.mono_left nhdsWithin_le_nhds
    simpa only [zero_div, Real.sqrt_zero, mul_zero] using ht

/-- Constant eigenvalues 0 and 1 across the two columns leave a diverging entry. -/
theorem fixed_jump_diverges :
    Tendsto (fun δ ↦ ‖offDiagonal δ 0 1‖) (𝓝[>] (0 : ℝ)) atTop := by
  have hc : Continuous denominator := by unfold denominator; fun_prop
  have hz : denominator 0 = 0 := by simp [denominator]
  have hD : Tendsto denominator (𝓝[>] (0 : ℝ)) (𝓝[>] (0 : ℝ)) := by
    apply tendsto_nhdsWithin_iff.2
    constructor
    · have ht : Tendsto denominator (𝓝[>] (0 : ℝ)) (𝓝 (denominator 0)) :=
        hc.continuousAt.tendsto.mono_left nhdsWithin_le_nhds
      simpa only [hz] using ht
    · filter_upwards [self_mem_nhdsWithin] with δ hδ
      exact denominator_pos hδ
  apply (tendsto_inv_nhdsGT_zero.comp hD).congr'
  filter_upwards [self_mem_nhdsWithin] with δ hδ
  simp [offDiagonal, Complex.norm_real, abs_of_pos (denominator_pos hδ), one_div]

end E2ATwoZeroBlock

#print axioms E2ATwoZeroBlock.orthonormal_block
#print axioms E2ATwoZeroBlock.off_diagonal_norm_le
#print axioms E2ATwoZeroBlock.off_diagonal_tendsto_zero
#print axioms E2ATwoZeroBlock.fixed_jump_diverges
