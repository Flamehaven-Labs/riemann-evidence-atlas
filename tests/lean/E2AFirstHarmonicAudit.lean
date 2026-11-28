import Mathlib.Analysis.InnerProductSpace.Projection.Basic
import Mathlib.Tactic.Abel
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-! Check the sign convention, nested lower bound, and exact budget inequalities.
The enclosure of the Arb output in the rational input intervals is an external check. -/

namespace E2AFirstHarmonicAudit

open scoped InnerProductSpace

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-- Mathlib conjugates the first slot of the inner product. -/
theorem signed_polarization (x y : H) (c z : ℂ) (r : ℝ)
    (hz : (r : ℂ) * star z = c) :
    2 * (c * ⟪y, x⟫_ℂ).re =
      (r / 2) * (‖x + z • y‖ ^ 2 - ‖x - z • y‖ ^ 2) := by
  have hsym : RCLike.re ⟪x, z • y⟫_ℂ = RCLike.re ⟪z • y, x⟫_ℂ := by
    rw [← inner_conj_symm]
    rfl
  rw [norm_add_sq (𝕜 := ℂ), norm_sub_sq (𝕜 := ℂ), hsym, inner_smul_left, ← hz,
    mul_assoc]
  change 2 * ((r : ℂ) * (star z * ⟪y, x⟫_ℂ)).re =
    (r / 2) * ((‖x‖ ^ 2 + 2 * (star z * ⟪y, x⟫_ℂ).re + ‖z • y‖ ^ 2) -
      (‖x‖ ^ 2 - 2 * (star z * ⟪y, x⟫_ℂ).re + ‖z • y‖ ^ 2))
  rw [Complex.mul_re]
  simp only [Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero]
  ring

theorem nested_residual_lower (N M P : Submodule ℂ H)
    [N.HasOrthogonalProjection] [M.HasOrthogonalProjection] [P.HasOrthogonalProjection]
    (hNM : N ≤ M) (hMP : M ≤ P) (x : H) :
    ‖M.starProjection x - N.starProjection x‖ ^ 2 ≤
      ‖P.starProjection x - N.starProjection x‖ ^ 2 := by
  have hM : M.starProjection x - N.starProjection x ∈ M :=
    M.sub_mem (M.starProjection_apply_mem x) (hNM (N.starProjection_apply_mem x))
  have hOrth :
      ⟪P.starProjection x - M.starProjection x, M.starProjection x - N.starProjection x⟫_ℂ
        = 0 := by
    have hd : P.starProjection x - M.starProjection x =
        (x - M.starProjection x) - (x - P.starProjection x) := by abel
    rw [hd, inner_sub_left,
      M.starProjection_inner_eq_zero _ _ hM, P.starProjection_inner_eq_zero _ _ (hMP hM),
      sub_zero]
  have heq : P.starProjection x - N.starProjection x =
      (P.starProjection x - M.starProjection x) +
      (M.starProjection x - N.starProjection x) := by abel
  have hs := norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero _ _ hOrth
  rw [heq]
  simp only [pow_two]
  rw [hs]
  linarith [mul_self_nonneg ‖P.starProjection x - M.starProjection x‖]

theorem signed_interval (lp lm up um xp xm : ℝ)
    (hp₁ : lp ≤ xp) (hp₂ : xp ≤ up) (hm₁ : lm ≤ xm) (hm₂ : xm ≤ um) :
    lp - um ≤ xp - xm ∧ xp - xm ≤ up - lm :=
  ⟨sub_le_sub hp₁ hm₂, sub_le_sub hp₂ hm₁⟩

theorem first_pair_misses_budget (b : ℚ) (hb : (65.23789 : ℚ) < b) :
    86 * (0.7551450173 : ℚ) < b := by
  have h : 86 * (0.7551450173 : ℚ) < 65.23789 := by norm_num
  exact h.trans hb

theorem constant_rounding_budget :
    (0.03062 : ℚ) + 0.12657 + 0.10425 + 0.18896 = 0.4504 ∧
    (0.4503 : ℚ) + 0.7551450173 = 1.2054450173 ∧ (0.4503 : ℚ) < 0.4504 := by
  norm_num

#print axioms signed_polarization
#print axioms nested_residual_lower
#print axioms signed_interval
#print axioms first_pair_misses_budget
#print axioms constant_rounding_budget

end E2AFirstHarmonicAudit
