import Mathlib.Analysis.Complex.Basic
import Mathlib.MeasureTheory.Group.Integral
import Mathlib.Topology.Algebra.InfiniteSum.Real

namespace E2AGlobalTrace

open MeasureTheory MeasureTheory.Measure

/-- Translation invariance of the test kills a coefficient at any character
that is nontrivial on the translating element. This uses the positive Mellin sign. -/
theorem invariant_mellin_coefficient_eq_zero {G : Type*} [Group G] [MeasurableSpace G]
    [MeasurableMul G] (μ : Measure G) [IsMulLeftInvariant μ]
    (φ : G → ℂ) (χ : G →* ℂ) (u : G) (hφ : ∀ x, φ (u * x) = φ x)
    (hχ : χ u ≠ 1) : (∫ x, φ x * χ x ∂μ) = 0 := by
  have hinv := integral_mul_left_eq_self (μ := μ) (fun x ↦ φ x * χ x) u
  simp only [hφ, map_mul] at hinv
  have hpoint (x : G) : φ x * (χ u * χ x) = χ u * (φ x * χ x) :=
    (mul_left_comm (φ x) (χ u) (χ x))
  simp only [hpoint, integral_const_mul] at hinv
  have hzero : (χ u - 1) * (∫ x, φ x * χ x ∂μ) = 0 := by
    rw [sub_mul, one_mul, hinv, sub_self]
  exact (mul_eq_zero.mp hzero).resolve_left (sub_ne_zero.mpr hχ)

/-- A geometric shell count combined with faster geometric decay makes the
sum of the nonnegative character bounds finite. -/
theorem summable_character_shells {J : ℕ → Type*} [∀ n, Fintype (J n)]
    (cost : (Σ n, J n) → ℝ) {A B growth decay : ℝ}
    (hg : 0 ≤ growth) (hd : 0 ≤ decay) (hgap : growth * decay < 1)
    (hB : 0 ≤ B) (hpos : ∀ i, 0 ≤ cost i)
    (hcount : ∀ n, (Fintype.card (J n) : ℝ) ≤ A * growth ^ n)
    (hcost : ∀ i, cost i ≤ B * decay ^ i.1) : Summable cost := by
  refine (summable_sigma_of_nonneg hpos).mpr ⟨fun n ↦ (hasSum_fintype (fun j : J n ↦ cost ⟨n, j⟩)).summable, ?_⟩
  have hnorm : ‖growth * decay‖ < 1 := by rwa [Real.norm_of_nonneg (mul_nonneg hg hd)]
  have hgeo : Summable (fun n : ℕ ↦ (A * B) * (growth * decay) ^ n) :=
    (summable_geometric_of_norm_lt_one hnorm).mul_left (A * B)
  refine Summable.of_nonneg_of_le (fun n ↦ tsum_nonneg fun j ↦ hpos ⟨n, j⟩) ?_ hgeo
  intro n
  rw [tsum_fintype]
  calc
    _ ≤ ∑ _ : J n, B * decay ^ n := Finset.sum_le_sum fun j _ ↦ hcost ⟨n, j⟩
    _ = (Fintype.card (J n) : ℝ) * (B * decay ^ n) := by simp
    _ ≤ (A * growth ^ n) * (B * decay ^ n) :=
      mul_le_mul_of_nonneg_right (hcount n) (mul_nonneg hB (pow_nonneg hd _))
    _ = (A * B) * (growth * decay) ^ n := by rw [mul_pow]; ac_rfl

/-- A summable bound on the absolute diagonal sums justifies aggregating both
the character and zero-mode indices. -/
theorem summable_spectral_terms_of_trace_bounds {ι : Type*} {J : ι → Type*}
    (term : (Σ i, J i) → ℂ) (bound : ι → ℝ) (hbound : Summable bound)
    (hdiag : ∀ i, Summable (fun j : J i ↦ ‖term ⟨i, j⟩‖))
    (hle : ∀ i, (∑' j : J i, ‖term ⟨i, j⟩‖) ≤ bound i) :
    Summable (fun p ↦ ‖term p‖) := by
  refine (summable_sigma_of_nonneg (fun p ↦ norm_nonneg (term p))).mpr ⟨hdiag, ?_⟩
  exact Summable.of_nonneg_of_le (fun _ ↦ tsum_nonneg fun _ ↦ norm_nonneg _) hle hbound

end E2AGlobalTrace

#print axioms E2AGlobalTrace.invariant_mellin_coefficient_eq_zero
#print axioms E2AGlobalTrace.summable_character_shells
#print axioms E2AGlobalTrace.summable_spectral_terms_of_trace_bounds
