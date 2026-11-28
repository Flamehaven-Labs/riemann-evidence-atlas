import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.InnerProductSpace.ProdL2
import Mathlib.Topology.Algebra.Module.ContinuousLinearMap.Quotient
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.ImproperIntegrals
import Mathlib.MeasureTheory.Measure.Lebesgue.Integral
import Mathlib.Tactic.Ring

namespace E2AAdelicQuotient

open scoped InnerProductSpace BigOperators

section Quotient

variable {𝕜 H : Type*} [NontriviallyNormedField 𝕜]
  [NormedAddCommGroup H] [NormedSpace 𝕜 H]

/-- A bounded operator induces an operator on a quotient when it preserves the denominator. -/
noncomputable def quotientOperator (W : Submodule 𝕜 H) (T : H →L[𝕜] H)
    (hW : ∀ x ∈ W, T x ∈ W) : (H ⧸ W) →L[𝕜] (H ⧸ W) :=
  W.liftQL (W.mkQL.comp T) fun x hx ↦ (Submodule.Quotient.mk_eq_zero W).mpr (hW x hx)

theorem quotientOperator_mk (W : Submodule 𝕜 H) (T : H →L[𝕜] H)
    (hW : ∀ x ∈ W, T x ∈ W) (x : H) :
    quotientOperator W T hW (Submodule.Quotient.mk x) = Submodule.Quotient.mk (T x) :=
  rfl

theorem norm_quotientOperator_le (W : Submodule 𝕜 H) (T : H →L[𝕜] H)
    (hW : ∀ x ∈ W, T x ∈ W) :
    ‖quotientOperator W T hW‖ ≤ ‖T‖ := by
  apply ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg _)
  intro q
  refine le_of_forall_pos_le_add fun ε hε ↦ ?_
  let η := ε / (‖T‖ + 1)
  have hT : 0 ≤ ‖T‖ := norm_nonneg _
  have hden : 0 < ‖T‖ + 1 := by linarith
  have hη : 0 < η := div_pos hε hden
  obtain ⟨x, hx, hnorm⟩ := Submodule.Quotient.norm_mk_lt q hη
  have hbudget : ‖T‖ * η ≤ ε := by
    have he : (‖T‖ + 1) * η = ε := by
      dsimp [η]
      field_simp
    nlinarith [hη.le]
  calc
    ‖quotientOperator W T hW q‖ = ‖(Submodule.Quotient.mk (T x) : H ⧸ W)‖ := by
      rw [← hx, quotientOperator_mk]
    _ ≤ ‖T x‖ := Submodule.Quotient.norm_mk_le W _
    _ ≤ ‖T‖ * ‖x‖ := T.le_opNorm _
    _ ≤ ‖T‖ * (‖q‖ + η) := mul_le_mul_of_nonneg_left hnorm.le hT
    _ ≤ ‖T‖ * ‖q‖ + ε := by rw [mul_add]; linarith

private def descendFunctional (W : Submodule 𝕜 H) (L : H →L[𝕜] 𝕜)
    (hL : ∀ x ∈ W, L x = 0) : (H ⧸ W) →L[𝕜] 𝕜 :=
  W.liftQL L fun x hx ↦ LinearMap.mem_ker.mpr (hL x hx)

/-- Pullback of a quotient functional is the descent of its ambient pullback. -/
theorem quotient_functional_pullback (W : Submodule 𝕜 H) (T : H →L[𝕜] H)
    (hW : ∀ x ∈ W, T x ∈ W) (L : H →L[𝕜] 𝕜) (hL : ∀ x ∈ W, L x = 0) :
    (descendFunctional W L hL).comp (quotientOperator W T hW) =
      descendFunctional W (L.comp T) (fun x hx ↦ hL _ (hW x hx)) := by
  ext q
  obtain ⟨x, rfl⟩ := W.mkQ_surjective q
  rfl

end Quotient

section Hilbert

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
  (W : Submodule ℂ H) [W.HasOrthogonalProjection]

theorem adjoint_preserves_annihilator_iff [CompleteSpace H] (T : H →L[ℂ] H) :
    (∀ x ∈ W, T x ∈ W) ↔ (∀ y ∈ Wᗮ, T.adjoint y ∈ Wᗮ) := by
  constructor
  · intro h y hy
    apply (W.mem_orthogonal _).mpr
    intro x hx
    rw [T.adjoint_inner_right]
    exact Submodule.inner_right_of_mem_orthogonal (h x hx) hy
  · intro h x hx
    have hmem : T x ∈ Wᗮᗮ := by
      apply (Wᗮ.mem_orthogonal' _).mpr
      intro y hy
      rw [← T.adjoint_inner_right]
      exact Submodule.inner_right_of_mem_orthogonal hx (h y hy)
    rwa [W.orthogonal_orthogonal] at hmem

private theorem quotientEquivOrthogonal_projection (x : H) :
    W.quotientEquivOrthogonal (Submodule.Quotient.mk x) = Wᗮ.orthogonalProjectionOnto x := by
  have hmem := W.sub_starProjection_mem_orthogonal x
  have heq : (Submodule.Quotient.mk x : H ⧸ W) =
      Submodule.Quotient.mk (x - W.starProjection x) := by
    apply (Submodule.Quotient.eq W).mpr
    simp
  rw [heq, W.quotientEquivOrthogonal_mk _ hmem, W.orthogonalProjectionOnto_orthogonal]

/-- The induced operator, carried to the orthogonal complement by the quotient isometry. -/
theorem quotient_operator_eq_compression (T : H →L[ℂ] H) (hW : ∀ x ∈ W, T x ∈ W)
    (v : Wᗮ) :
    W.quotientEquivOrthogonal (quotientOperator W T hW (W.quotientEquivOrthogonal.symm v)) =
      Wᗮ.orthogonalProjectionOnto (T v) := by
  rw [W.quotientEquivOrthogonal_symm_eq_mk _ v.2, quotientOperator_mk,
    quotientEquivOrthogonal_projection]

theorem norm_orthogonal_compression_le (T : H →L[ℂ] H) :
    ‖W.starProjection.comp (T.comp W.starProjection)‖ ≤ ‖T‖ := by
  apply ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg _)
  intro x
  change ‖W.starProjection (T (W.starProjection x))‖ ≤ ‖T‖ * ‖x‖
  exact (W.norm_starProjection_apply_le _).trans <|
    (T.le_opNorm _).trans <| mul_le_mul_of_nonneg_left
      (W.norm_starProjection_apply_le _) (norm_nonneg _)

end Hilbert

/-- It suffices to check invariance on generators of a closed span. -/
theorem closed_span_invariant {H : Type*} [NormedAddCommGroup H] [NormedSpace ℂ H]
    (T : H →L[ℂ] H) (s : Set H) (hs : ∀ x ∈ s, T x ∈ Submodule.span ℂ s) :
    ∀ x ∈ (Submodule.span ℂ s).topologicalClosure,
      T x ∈ (Submodule.span ℂ s).topologicalClosure := by
  have hinv : Submodule.span ℂ s ∈ Module.End.invtSubmodule T.toLinearMap := by
    rw [Module.End.mem_invtSubmodule_iff_map_le, Submodule.map_span]
    exact Submodule.span_le.mpr fun _ ⟨x, hx, he⟩ ↦ he ▸ hs x hx
  have hcl := Submodule.topologicalClosure_mem_invtSubmodule hinv
  rw [Module.End.mem_invtSubmodule_iff_forall_mem_of_mem] at hcl
  exact hcl

/-- The reciprocal of the manuscript's radial norm weight, in centered log coordinates, at s=2. -/
theorem radial_dual_weight_eq (α x : ℝ) (hα : 0 ≤ α) :
    (max (Real.exp (-(2 * α) * x)) (Real.exp ((2 * α) * x)) * (1 + x ^ 2))⁻¹ =
      Real.exp (-(2 * α) * |x|) / (1 + x ^ 2) := by
  have hmax : max (Real.exp (-(2 * α) * x)) (Real.exp ((2 * α) * x)) =
      Real.exp ((2 * α) * |x|) := by
    rcases le_total x 0 with hx | hx
    · rw [abs_of_nonpos hx, max_eq_left]
      · congr 1
        ring
      · rw [Real.exp_le_exp]
        nlinarith [mul_nonpos_of_nonneg_of_nonpos hα hx]
    · rw [abs_of_nonneg hx, max_eq_right]
      rw [Real.exp_le_exp]
      nlinarith [mul_nonneg hα hx]
  rw [hmax, mul_inv_rev, ← Real.exp_neg]
  rw [show -((2 * α) * |x|) = -(2 * α) * |x| by ring, div_eq_mul_inv, mul_comm]

/-- A translate of a polynomial-exponential mode is triangular in its polynomial degree. -/
theorem translate_polynomial_mode (z : ℂ) (n : ℕ) (x y : ℝ) :
    ((x + y : ℝ) : ℂ) ^ n * Complex.exp (z * ((x + y : ℝ) : ℂ)) =
      ∑ j ∈ Finset.range (n + 1),
        ((n.choose j : ℂ) * (y : ℂ) ^ (n - j) * Complex.exp (z * (y : ℂ))) *
        ((x : ℂ) ^ j * Complex.exp (z * (x : ℂ))) := by
  rw [Complex.ofReal_add, mul_add, Complex.exp_add, add_pow, Finset.sum_mul]
  refine Finset.sum_congr rfl fun j _ ↦ ?_
  ring

open MeasureTheory in
/-- Change of variables for the bilinear pairing. A backwards shift on the
first argument is a forwards shift on the second. -/
theorem radial_translation_pairing (f g : ℝ → ℂ) (y : ℝ) :
    (∫ x : ℝ, f (x - y) * g x) = ∫ x : ℝ, f x * g (x + y) := by
  calc
    _ = ∫ x : ℝ, f (x + y - y) * g (x + y) :=
      (integral_add_right_eq_self (fun x : ℝ ↦ f (x - y) * g x) y).symm
    _ = _ := by simp only [add_sub_cancel_right]

open MeasureTheory Set in
/-- The one-sided Laplace integral gives the resolvent coefficient on an exponential mode. -/
theorem laplace_translate_mode (b x : ℝ) (z : ℂ) (hb : z.re < b) :
    (∫ y : ℝ in Ioi 0, Complex.exp (-(b : ℂ) * (y : ℂ)) *
      Complex.exp (z * ((x + y : ℝ) : ℂ))) =
        ((b : ℂ) - z)⁻¹ * Complex.exp (z * (x : ℂ)) := by
  have h (y : ℝ) : Complex.exp (-(b : ℂ) * (y : ℂ)) *
      Complex.exp (z * ((x + y : ℝ) : ℂ)) =
        Complex.exp ((z - (b : ℂ)) * (y : ℂ)) * Complex.exp (z * (x : ℂ)) := by
    rw [← Complex.exp_add, ← Complex.exp_add, Complex.ofReal_add]
    congr 1
    ring
  have hneg : (z - (b : ℂ)).re < 0 := by simpa using sub_neg.mpr hb
  simp_rw [h]
  rw [integral_mul_const, integral_exp_mul_complex_Ioi hneg]
  simp only [Complex.ofReal_zero, mul_zero, Complex.exp_zero, neg_div, one_div]
  rw [show z - (b : ℂ) = -((b : ℂ) - z) by ring, inv_neg, neg_neg]

end E2AAdelicQuotient

#print axioms E2AAdelicQuotient.quotientOperator_mk
#print axioms E2AAdelicQuotient.norm_quotientOperator_le
#print axioms E2AAdelicQuotient.quotient_functional_pullback
#print axioms E2AAdelicQuotient.adjoint_preserves_annihilator_iff
#print axioms E2AAdelicQuotient.quotient_operator_eq_compression
#print axioms E2AAdelicQuotient.norm_orthogonal_compression_le
#print axioms E2AAdelicQuotient.closed_span_invariant
#print axioms E2AAdelicQuotient.radial_dual_weight_eq
#print axioms E2AAdelicQuotient.translate_polynomial_mode
#print axioms E2AAdelicQuotient.radial_translation_pairing
#print axioms E2AAdelicQuotient.laplace_translate_mode
