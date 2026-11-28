import Mathlib.Analysis.Calculus.ParametricIntegral
import Mathlib.Analysis.Calculus.Deriv.Shift
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.InnerProductSpace.l2Space
import Mathlib.MeasureTheory.Measure.Lebesgue.Integral
import Mathlib.Topology.Algebra.InfiniteSum.Real
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Module

namespace E2AFixedCharacterTrace

open Filter Set MeasureTheory
open scoped Topology InnerProductSpace

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The Bochner average of a continuous-linear action, evaluated on a vector. -/
noncomputable def kernelAverage (U : ℝ → H →L[ℂ] H) (k : ℝ → ℂ) (x : H) : H :=
  ∫ t : ℝ, k t • U t x

/-- The forward group action on an average shifts the kernel backwards. -/
theorem translate_kernel_average (U : ℝ → H →L[ℂ] H)
    (hgroup : ∀ h t, U (h + t) = (U h).comp (U t)) (k : ℝ → ℂ) (x : H)
    (hint : Integrable (fun t ↦ k t • U t x)) (h : ℝ) :
    U h (kernelAverage U k x) = ∫ t : ℝ, k (t - h) • U t x := by
  unfold kernelAverage
  rw [← (U h).integral_comp_comm hint]
  simp_rw [map_smul, ← ContinuousLinearMap.comp_apply, ← hgroup, add_comm h]
  simpa only [add_sub_cancel_right] using
    (integral_add_right_eq_self (fun t : ℝ ↦ k (t - h) • U t x) h)

/-- Smoothing on the generator domain. The measurable integrands and an
integrable neighborhood envelope are explicit in the statement. -/
theorem kernel_average_orbit_hasDerivAt (U : ℝ → H →L[ℂ] H)
    (hgroup : ∀ h t, U (h + t) = (U h).comp (U t)) (k k' : ℝ → ℂ) (x : H)
    (hk : ∀ r, HasDerivAt k (k' r) r)
    (hint : Integrable (fun t ↦ k t • U t x))
    {s : Set ℝ} (hs : s ∈ 𝓝 (0 : ℝ)) {bound : ℝ → ℝ}
    (hmeas : ∀ᶠ h in 𝓝 (0 : ℝ), AEStronglyMeasurable (fun t ↦ k (t - h) • U t x) volume)
    (hdmeas : AEStronglyMeasurable (fun t ↦ (-k' t) • U t x) volume)
    (hbound : ∀ᵐ t ∂volume, ∀ h ∈ s, ‖k' (t - h) • U t x‖ ≤ bound t)
    (hbound_int : Integrable bound) :
    HasDerivAt (fun h : ℝ ↦ U h (kernelAverage U k x)) (-kernelAverage U k' x) 0 := by
  let F (h t : ℝ) : H := k (t - h) • U t x
  let F' (h t : ℝ) : H := (-k' (t - h)) • U t x
  have hdiff : ∀ᵐ t ∂volume, ∀ h ∈ s, HasDerivAt (F · t) (F' h t) h := by
    apply ae_of_all
    intro t h _
    exact ((hk (t - h)).comp_const_sub t h).smul_const (U t x)
  have h := hasDerivAt_integral_of_dominated_loc_of_deriv_le
    (F := F) (F' := F') (bound := bound) hs hmeas
    (by simpa only [F, sub_zero] using hint)
    (by simpa only [F', sub_zero] using hdmeas)
    (hbound.mono fun t ht h hs' ↦ by simpa only [F', neg_smul, norm_neg] using ht h hs')
    hbound_int hdiff
  simpa only [F, F', sub_zero, neg_smul, integral_neg, kernelAverage,
    ← translate_kernel_average U hgroup k x hint] using h.2

omit [CompleteSpace H] in
/-- Applying the inverse on two generator-domain vectors yields the factorization. -/
theorem twice_resolvent_factorization
    (U : ℝ → H →L[ℂ] H) (R : H →L[ℂ] H) (b : ℂ)
    (hinv : ∀ {a d : H}, HasDerivAt (fun t : ℝ ↦ U t a) d 0 → R (b • a - d) = a)
    (v₀ v₁ v₂ : H) (h₀ : HasDerivAt (fun t : ℝ ↦ U t v₀) (-v₁) 0)
    (h₁ : HasDerivAt (fun t : ℝ ↦ U t v₁) (-v₂) 0) :
    R (R ((b ^ 2) • v₀ + (2 * b) • v₁ + v₂)) = v₀ := by
  have r₀ : R (b • v₀ + v₁) = v₀ := by simpa only [sub_neg_eq_add] using hinv h₀
  have r₁ : R (b • v₁ + v₂) = v₁ := by simpa only [sub_neg_eq_add] using hinv h₁
  have heq : (b ^ 2) • v₀ + (2 * b) • v₁ + v₂ =
      b • (b • v₀ + v₁) + (b • v₁ + v₂) := by
    simp only [smul_add, smul_smul, pow_two, two_mul, add_smul]
    abel
  rw [heq, map_add, map_smul, r₀, r₁, r₀]

variable {ι : Type*}

/-- Parseval applied to rows and columns transfers the square-summability to the adjoint. -/
theorem summable_adjoint_columns (e : HilbertBasis ι ℂ H) (R : H →L[ℂ] H)
    (hR : Summable (fun i ↦ ‖R (e i)‖ ^ 2)) :
    Summable (fun i ↦ ‖R.adjoint (e i)‖ ^ 2) := by
  have parseval (x : H) : HasSum (fun i ↦ ‖inner ℂ (e i) x‖ ^ 2) (‖x‖ ^ 2) := by
    have h := lp.hasSum_norm (by norm_num : 0 < (2 : ENNReal).toReal) (e.repr x)
    rw [LinearIsometryEquiv.norm_map] at h
    simpa only [ENNReal.toReal_ofNat, Real.rpow_two,
      HilbertBasis.repr_apply_apply] using h
  let M (p : ι × ι) := ‖inner ℂ (e p.2) (R (e p.1))‖ ^ 2
  have rows (i : ι) : HasSum (fun j ↦ M (i, j)) (‖R (e i)‖ ^ 2) := parseval (R (e i))
  have cols (j : ι) : HasSum (fun i ↦ M (i, j)) (‖R.adjoint (e j)‖ ^ 2) := by
    apply (parseval (R.adjoint (e j))).congr_fun
    intro i
    change ‖inner ℂ (e j) (R (e i))‖ ^ 2 = ‖inner ℂ (e i) (R.adjoint (e j))‖ ^ 2
    rw [R.adjoint_inner_right, norm_inner_symm (𝕜 := ℂ) (e j) (R (e i))]
  have hM (p : ι × ι) : 0 ≤ M p := sq_nonneg _
  have h : Summable M := (summable_prod_of_nonneg (f := M) hM).mpr
    ⟨fun i ↦ (rows i).summable, hR.congr fun i ↦ (rows i).tsum_eq.symm⟩
  have h' : Summable (fun p : ι × ι ↦ M (p.2, p.1)) :=
    (Equiv.prodComm ι ι).summable_iff.mpr h
  exact ((summable_prod_of_nonneg (fun p : ι × ι ↦ hM (p.2, p.1))).mp h').2.congr
    fun j ↦ (cols j).tsum_eq

/-- The rank-one norms are summable, and the sum in operator norm is R composed twice with D. -/
theorem resolvent_rank_one_expansion (e : HilbertBasis ι ℂ H) (R D : H →L[ℂ] H)
    (hR : Summable (fun i ↦ ‖R (e i)‖ ^ 2)) :
    let term (i : ι) := InnerProductSpace.rankOne ℂ (R (e i)) (D.adjoint (R.adjoint (e i)))
    (Summable (fun i ↦ ‖term i‖)) ∧ HasSum term (R.comp (R.comp D)) := by
  let term (i : ι) := InnerProductSpace.rankOne ℂ (R (e i)) (D.adjoint (R.adjoint (e i)))
  change Summable (fun i ↦ ‖term i‖) ∧ HasSum term (R.comp (R.comp D))
  have hstar := summable_adjoint_columns e R hR
  have hprod : Summable (fun i ↦ ‖R (e i)‖ * ‖R.adjoint (e i)‖) := by
    apply Summable.of_nonneg_of_le (fun _ ↦ by positivity) _ (hR.add hstar)
    intro i
    nlinarith [sq_nonneg (‖R (e i)‖ - ‖R.adjoint (e i)‖), sq_nonneg ‖R (e i)‖,
      sq_nonneg ‖R.adjoint (e i)‖]
  have hnorm : Summable (fun i ↦ ‖term i‖) := by
    refine Summable.of_nonneg_of_le (fun _ ↦ norm_nonneg _) (fun i ↦ ?_)
      (hprod.mul_right ‖D.adjoint‖)
    simp only [term, InnerProductSpace.norm_rankOne]
    rw [mul_right_comm ‖R (e i)‖ ‖R.adjoint (e i)‖ ‖D.adjoint‖, mul_assoc]
    exact mul_le_mul_of_nonneg_left (D.adjoint.le_opNorm _) (norm_nonneg _)
  have hs : Summable term := hnorm.of_norm_bounded fun _ ↦ le_rfl
  refine ⟨hnorm, ?_⟩
  have hpoint (x : H) :
      HasSum (fun i ↦ term i x) (R (R (D x))) := by
    apply ((e.hasSum_repr (R (D x))).mapL R).congr_fun
    intro i
    simp only [term, InnerProductSpace.rankOne_apply, D.adjoint_inner_left, R.adjoint_inner_left,
      map_smul, e.repr_apply_apply]
  have hsum : (∑' i, term i) = R.comp (R.comp D) := by
    ext x
    exact ((hs.hasSum.mapL (ContinuousLinearMap.apply ℂ H x))).unique (hpoint x)
  exact hsum ▸ hs.hasSum

/-- The diagonal of the averaged action is the Mellin integral on an invariant flag. -/
theorem kernel_average_diagonal (U : ℝ → H →L[ℂ] H) (k : ℝ → ℂ) (e : H) (v : ℝ → H)
    (z : ℂ) (he : ‖e‖ = 1)
    (hu : ∀ t, U t e = Complex.exp (z * (t : ℂ)) • e + v t)
    (hv : ∀ t, inner ℂ e (v t) = 0)
    (hint : Integrable (fun t ↦ k t • U t e)) :
    inner ℂ e (kernelAverage U k e) = ∫ t : ℝ, k t * Complex.exp (z * (t : ℂ)) := by
  change innerSL ℂ e (∫ t : ℝ, k t • U t e) = _
  rw [← (innerSL ℂ e).integral_comp_comm hint]
  congr 1
  funext t
  change inner ℂ e (k t • U t e) = _
  have hunit : inner ℂ e e = 1 := by
    rw [inner_self_eq_norm_sq_to_K, he]
    norm_num
  rw [hu t, inner_smul_right, inner_add_right, hv t, add_zero, inner_smul_right, hunit, mul_one]

/-- Absolute convergence of the diagonal under the squared-resolvent factorization. -/
theorem summable_resolvent_diagonal (e : HilbertBasis ι ℂ H) (R D : H →L[ℂ] H)
    (hR : Summable (fun i ↦ ‖R (e i)‖ ^ 2)) :
    Summable (fun i ↦ ‖inner ℂ (e i) (R (R (D (e i))))‖) := by
  have hstar := summable_adjoint_columns e R hR
  have hSstar : Summable (fun i ↦ ‖(R.comp D).adjoint (e i)‖ ^ 2) := by
    refine Summable.of_nonneg_of_le (fun _ ↦ sq_nonneg _) (fun i ↦ ?_)
      (hstar.mul_left (‖D.adjoint‖ ^ 2))
    rw [ContinuousLinearMap.adjoint_comp, ContinuousLinearMap.comp_apply, ← mul_pow]
    exact pow_le_pow_left₀ (norm_nonneg _) (D.adjoint.le_opNorm _) 2
  have hS := summable_adjoint_columns e (R.comp D).adjoint hSstar
  simp only [ContinuousLinearMap.adjoint_adjoint, ContinuousLinearMap.comp_apply] at hS
  refine Summable.of_nonneg_of_le (fun _ ↦ norm_nonneg _) (fun i ↦ ?_) (hstar.add hS)
  rw [← R.adjoint_inner_left]
  calc
    _ ≤ ‖R.adjoint (e i)‖ * ‖R (D (e i))‖ := norm_inner_le_norm _ _
    _ ≤ ‖R.adjoint (e i)‖ ^ 2 + ‖R (D (e i))‖ ^ 2 := by
      nlinarith [sq_nonneg (‖R.adjoint (e i)‖ - ‖R (D (e i))‖),
        sq_nonneg ‖R.adjoint (e i)‖, sq_nonneg ‖R (D (e i))‖]

/-- Combine the Mellin calculation with the factorization to certify absolute
summability of the fixed-character spectral diagonal. -/
theorem summable_mellin_diagonal (e : HilbertBasis ι ℂ H) (R D : H →L[ℂ] H)
    (hR : Summable (fun i ↦ ‖R (e i)‖ ^ 2))
    (U : ℝ → H →L[ℂ] H) (k : ℝ → ℂ) (z : ι → ℂ) (v : ι → ℝ → H)
    (hu : ∀ i t, U t (e i) = Complex.exp (z i * (t : ℂ)) • e i + v i t)
    (hv : ∀ i t, inner ℂ (e i) (v i t) = 0)
    (hi : ∀ i, Integrable (fun t ↦ k t • U t (e i)))
    (hfact : ∀ i, kernelAverage U k (e i) = R (R (D (e i)))) :
    Summable (fun i ↦ ‖∫ t : ℝ, k t * Complex.exp (z i * (t : ℂ))‖) := by
  apply (summable_resolvent_diagonal e R D hR).congr
  intro i
  rw [← hfact i, kernel_average_diagonal U k (e i) (v i) (z i)
    (e.orthonormal.norm_eq_one i) (hu i) (hv i) (hi i)]

end E2AFixedCharacterTrace

#print axioms E2AFixedCharacterTrace.translate_kernel_average
#print axioms E2AFixedCharacterTrace.kernel_average_orbit_hasDerivAt
#print axioms E2AFixedCharacterTrace.twice_resolvent_factorization
#print axioms E2AFixedCharacterTrace.summable_adjoint_columns
#print axioms E2AFixedCharacterTrace.resolvent_rank_one_expansion
#print axioms E2AFixedCharacterTrace.kernel_average_diagonal
#print axioms E2AFixedCharacterTrace.summable_resolvent_diagonal
#print axioms E2AFixedCharacterTrace.summable_mellin_diagonal
