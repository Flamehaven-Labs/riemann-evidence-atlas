import Mathlib.Analysis.Normed.Operator.Basic
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Linarith

namespace E2ABiorthogonalGap

private theorem kernel_pos {δ : ℝ} (hδ : 0 < δ) :
    0 < 2 * (1 - Real.exp (-δ)) := by
  have h : Real.exp (-δ) < 1 := by
    rw [← Real.exp_zero]
    exact Real.exp_lt_exp.mpr (neg_neg_of_pos hδ)
  linarith

theorem inverse_sqrt_gap_le {δ : ℝ} (hδ : 0 < δ) :
    1 / Real.sqrt (2 * δ) ≤ 1 / Real.sqrt (2 * (1 - Real.exp (-δ))) := by
  apply one_div_le_one_div_of_le (Real.sqrt_pos.2 (kernel_pos hδ))
  apply Real.sqrt_le_sqrt
  linarith [Real.add_one_le_exp (-δ)]

/-- The normalized distance formula is an analytic input for the chosen dual norm. -/
theorem biorthogonal_product_lower {E : Type*} [SeminormedAddCommGroup E]
    [NormedSpace ℂ E] {ηt ηu : E →L[ℂ] ℂ} {ψ : E} {δ : ℝ}
    (hδ : 0 < δ) (ht : ηt ψ = 1) (hu : ηu ψ = 0)
    (hdistance : ‖ηt - ηu‖ = ‖ηt‖ * Real.sqrt (2 * (1 - Real.exp (-δ)))) :
    1 / Real.sqrt (2 * (1 - Real.exp (-δ))) ≤ ‖ηt‖ * ‖ψ‖ := by
  have hop := (ηt - ηu).le_opNorm ψ
  have hvalue : ‖(ηt - ηu) ψ‖ = 1 := by simp [ht, hu]
  rw [hvalue, hdistance] at hop
  apply (div_le_iff₀ (Real.sqrt_pos.2 (kernel_pos hδ))).2
  simpa only [mul_assoc, mul_left_comm, mul_comm] using hop

/-- A fixed pairwise product cap would force positive separation of the ordinates. -/
theorem gap_lower_of_uniform_cap {δ C : ℝ} (hδ : 0 < δ) (hC : 0 < C)
    (hcap : 1 / Real.sqrt (2 * (1 - Real.exp (-δ))) ≤ C) :
    1 / (2 * C ^ 2) ≤ δ := by
  have hp : 0 < 2 * δ := by linarith
  have h := (div_le_iff₀ (Real.sqrt_pos.2 hp)).1 ((inverse_sqrt_gap_le hδ).trans hcap)
  have hs : (1 : ℝ) ^ 2 ≤ (C * Real.sqrt (2 * δ)) ^ 2 := by
    simpa only [pow_two] using mul_self_le_mul_self (by norm_num : (0 : ℝ) ≤ 1) h
  rw [mul_pow, Real.sq_sqrt hp.le] at hs
  apply (div_le_iff₀ (by positivity : (0 : ℝ) < 2 * C ^ 2)).2
  nlinarith only [hs]

/-- The hypotheses refer only to chosen pairs and their positive gaps. -/
theorem no_uniform_cap_of_close_pairs {ι : Type*} (gap product : ι → ℝ)
    (hgap : ∀ i, 0 < gap i) (hsmall : ∀ ε > 0, ∃ i, gap i < ε)
    (hlower : ∀ i, 1 / Real.sqrt (2 * (1 - Real.exp (-gap i))) ≤ product i) :
    ¬ ∃ C : ℝ, ∀ i, product i ≤ C := by
  rintro ⟨C, hC⟩
  let B := max C 1
  have hB : 0 < B := zero_lt_one.trans_le (le_max_right C 1)
  obtain ⟨i, hi⟩ := hsmall (1 / (2 * B ^ 2)) (by positivity)
  have hcap := (hlower i).trans ((hC i).trans (le_max_left C 1))
  exact (not_lt_of_ge (gap_lower_of_uniform_cap (hgap i) hB hcap)) hi

end E2ABiorthogonalGap

#print axioms E2ABiorthogonalGap.inverse_sqrt_gap_le
#print axioms E2ABiorthogonalGap.biorthogonal_product_lower
#print axioms E2ABiorthogonalGap.gap_lower_of_uniform_cap
#print axioms E2ABiorthogonalGap.no_uniform_cap_of_close_pairs
