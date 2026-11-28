import Mathlib.Analysis.Calculus.Deriv.Slope
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.ImproperIntegrals
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap
import Mathlib.Analysis.SpecificLimits.Normed
import Mathlib.Topology.Algebra.InfiniteSum.Real
import Mathlib.Tactic.Linarith

namespace E2AResolvent

open Filter Set
open scoped Topology InnerProductSpace BigOperators

/-- Derivative of a squared orbit norm at its common value with the exponential envelope. -/
theorem orbit_energy_le {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {u : ℝ → H} {x d : H} {ω : ℝ} (hu0 : u 0 = x) (hd : HasDerivAt u d 0)
    (hbound : ∀ᶠ y in 𝓝[>] (0 : ℝ), ‖u y‖ ^ 2 ≤ Real.exp (2 * ω * y) * ‖x‖ ^ 2) :
    (inner ℂ x d).re ≤ ω * ‖x‖ ^ 2 := by
  let : InnerProductSpace ℝ H := InnerProductSpace.rclikeToReal ℂ H
  have hlo : HasDerivAt (fun t : ℝ ↦ ‖u t‖ ^ 2) (2 * (inner ℂ x d).re) 0 := by
    simpa only [hu0, real_inner_eq_re_inner ℂ, RCLike.re_to_complex] using hd.norm_sq
  have hhi : HasDerivAt (fun t : ℝ ↦ Real.exp (2 * ω * t) * ‖x‖ ^ 2)
      (2 * ω * ‖x‖ ^ 2) 0 := by
    simpa using ((((hasDerivAt_id (0 : ℝ)).const_mul (2 * ω)).exp).mul_const (‖x‖ ^ 2))
  have hdiff : 2 * (inner ℂ x d).re ≤ 2 * ω * ‖x‖ ^ 2 := by
    apply le_of_tendsto_of_tendsto hlo.tendsto_slope_zero_right hhi.tendsto_slope_zero_right
    filter_upwards [hbound, self_mem_nhdsWithin] with t ht (hpos : 0 < t)
    simp only [zero_add, hu0, mul_zero, Real.exp_zero, one_mul, smul_eq_mul]
    exact mul_le_mul_of_nonneg_left (sub_le_sub_right ht _) (inv_nonneg.mpr hpos.le)
  linarith

/-- Dissipativity yields a columnwise energy estimate for the inverse equation. -/
theorem energy_of_inverse_equation {H : Type*} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] {b ω : ℝ} {x y d : H}
    (heq : x = (b : ℂ) • y - d)
    (hd : (inner ℂ y d).re ≤ ω * ‖y‖ ^ 2) :
    (b - ω) * ‖y‖ ^ 2 ≤ (inner ℂ y x).re := by
  rw [heq, inner_sub_right, inner_smul_right, inner_self_eq_norm_sq_to_K]
  change (b - ω) * ‖y‖ ^ 2 ≤ ((b : ℂ) * (‖y‖ : ℂ) ^ 2).re - (inner ℂ y d).re
  rw [← Complex.ofReal_pow, ← Complex.ofReal_mul, Complex.ofReal_re]
  linarith

/-- The previous flag contributes zero to the Gram–Schmidt diagonal. -/
theorem diagonal_of_orthogonal_error {H : Type*} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] {e v : H} {c : ℂ} (he : ‖e‖ = 1)
    (hv : inner ℂ v e = 0) :
    (inner ℂ (c • e + v) e).re = c.re := by
  rw [inner_add_left, hv, add_zero, inner_smul_left, inner_self_eq_norm_sq_to_K, he]
  simp

theorem real_part_inverse_le {b α : ℝ} {z : ℂ} (hz : |z.re| ≤ α) (hb : α + 1 ≤ b) :
    (((b : ℂ) - z)⁻¹).re ≤ (b + α) / (1 + z.im ^ 2) := by
  obtain ⟨hlo, hhi⟩ := abs_le.mp hz
  have h : 1 ≤ b - z.re := by linarith
  have hs : 1 ≤ (b - z.re) ^ 2 := by nlinarith [mul_nonneg (sub_nonneg.mpr h) (by linarith : 0 ≤ b - z.re + 1)]
  rw [Complex.inv_re, Complex.normSq_apply]
  simp only [Complex.sub_re, Complex.ofReal_re, Complex.sub_im, Complex.ofReal_im, zero_sub, ← sq]
  calc
    _ ≤ (b - z.re) / (1 + z.im ^ 2) :=
      div_le_div_of_nonneg_left (by linarith) (by positivity) (by linarith)
    _ ≤ _ := div_le_div_of_nonneg_right (by linarith) (by positivity)

/-- A sufficient count for summable inverse-square ordinates. The shell label
satisfies `2^k ≤ 1 + |t|` so that it also handles the shell near the origin. -/
theorem summable_ordinates_of_dyadic_count {J : ℕ → Type*} [∀ k, Fintype (J k)]
    {C : ℝ} (t : (Σ k, J k) → ℝ)
    (hshell : ∀ i, (2 : ℝ) ^ i.1 ≤ 1 + |t i|)
    (hcount : ∀ k, (Fintype.card (J k) : ℝ) ≤ C * 3 ^ k) :
    Summable (fun i ↦ (1 + (t i) ^ 2)⁻¹) := by
  refine (summable_sigma_of_nonneg (fun _ ↦ by positivity)).mpr ⟨fun _ ↦ (hasSum_fintype _).summable, ?_⟩
  have hgeo : Summable (fun k : ℕ ↦ (2 * C) * (3 / 4 : ℝ) ^ k) :=
    (summable_geometric_of_norm_lt_one (by norm_num : ‖(3 / 4 : ℝ)‖ < 1)).mul_left _
  refine Summable.of_nonneg_of_le (fun _ ↦ tsum_nonneg fun _ ↦ by positivity) ?_ hgeo
  intro k
  rw [tsum_fintype]
  have hi (i : J k) : (1 + (t ⟨k, i⟩) ^ 2)⁻¹ ≤ 2 / (4 : ℝ) ^ k := by
    have h := pow_le_pow_left₀ (by positivity : 0 ≤ (2 : ℝ) ^ k) (hshell ⟨k, i⟩) 2
    have hsq : ((2 : ℝ) ^ k) ^ 2 = (4 : ℝ) ^ k := by rw [← pow_mul, Nat.mul_comm k 2, pow_mul]; norm_num
    rw [hsq] at h
    have hr : (1 + |t ⟨k, i⟩|) ^ 2 ≤ 2 * (1 + (t ⟨k, i⟩) ^ 2) := by
      nlinarith [sq_nonneg (|t ⟨k, i⟩| - 1), sq_abs (t ⟨k, i⟩)]
    rw [← one_div]
    exact (div_le_div_iff₀ (by positivity) (by positivity)).2 (by linarith [h.trans hr])
  calc
    _ ≤ ∑ _ : J k, 2 / (4 : ℝ) ^ k := Finset.sum_le_sum fun i _ ↦ hi i
    _ = (Fintype.card (J k) : ℝ) * (2 / (4 : ℝ) ^ k) := by simp
    _ ≤ (C * 3 ^ k) * (2 / (4 : ℝ) ^ k) := mul_le_mul_of_nonneg_right (hcount k) (by positivity)
    _ = (2 * C) * (3 / 4 : ℝ) ^ k := by rw [div_pow]; ring

/-- The column estimate uses the actual right-hand norm envelope of each orbit
and an orthogonal splitting of the resolvent column. -/
theorem resolvent_column_le {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {b ω α : ℝ} {z : ℂ} (hb : α + 1 ≤ b) (hgap : ω < b) (hz : |z.re| ≤ α)
    (e y d v : H) (u : ℝ → H) (he : ‖e‖ = 1) (hv : inner ℂ v e = 0)
    (hdiag : y = ((b : ℂ) - z)⁻¹ • e + v) (hres : e = (b : ℂ) • y - d)
    (hu0 : u 0 = y) (hd : HasDerivAt u d 0)
    (hbound : ∀ᶠ t in 𝓝[>] (0 : ℝ), ‖u t‖ ^ 2 ≤ Real.exp (2 * ω * t) * ‖y‖ ^ 2) :
    ‖y‖ ^ 2 ≤ ((b + α) / (b - ω)) * (1 + z.im ^ 2)⁻¹ := by
  have hen := energy_of_inverse_equation hres (orbit_energy_le hu0 hd hbound)
  rw [show (inner ℂ y e).re = (((b : ℂ) - z)⁻¹).re by
    rw [hdiag]
    exact diagonal_of_orthogonal_error he hv] at hen
  have hs := hen.trans (real_part_inverse_le hz hb)
  have hg := sub_pos.mpr hgap
  calc
    ‖y‖ ^ 2 ≤ ((b + α) / (1 + z.im ^ 2)) / (b - ω) :=
      (le_div_iff₀ hg).2 (by simpa [mul_comm] using hs)
    _ = _ := by simp only [div_eq_mul_inv]; ring

/-- A resolvent whose columns arise from the orbit equation and invariant-flag
diagonal has a square-summable column family under the dyadic count. -/
theorem summable_resolvent_columns_of_dyadic_count {H : Type*}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] {J : ℕ → Type*} [∀ k, Fintype (J k)]
    {b ω α C : ℝ} (hb : α + 1 ≤ b) (hgap : ω < b)
    (z : (Σ k, J k) → ℂ) (e d v : (Σ k, J k) → H) (R : H →L[ℂ] H) (U : ℝ → H → H)
    (hstrip : ∀ i, |(z i).re| ≤ α)
    (hshell : ∀ i, (2 : ℝ) ^ i.1 ≤ 1 + |(z i).im|)
    (hcount : ∀ k, (Fintype.card (J k) : ℝ) ≤ C * 3 ^ k)
    (he : ∀ i, ‖e i‖ = 1) (hv : ∀ i, inner ℂ (v i) (e i) = 0)
    (hdiag : ∀ i, R (e i) = ((b : ℂ) - z i)⁻¹ • e i + v i)
    (hres : ∀ i, e i = (b : ℂ) • R (e i) - d i)
    (hu0 : ∀ i, U 0 (R (e i)) = R (e i))
    (hd : ∀ i, HasDerivAt (fun t : ℝ ↦ U t (R (e i))) (d i) 0)
    (hbound : ∀ i, ∀ᶠ t in 𝓝[>] (0 : ℝ),
      ‖U t (R (e i))‖ ^ 2 ≤ Real.exp (2 * ω * t) * ‖R (e i)‖ ^ 2) :
    Summable (fun i ↦ ‖R (e i)‖ ^ 2) := by
  have hs := summable_ordinates_of_dyadic_count (fun i ↦ (z i).im) hshell hcount
  apply Summable.of_nonneg_of_le (fun _ ↦ sq_nonneg _) _ (hs.mul_left ((b + α) / (b - ω)))
  intro i
  exact resolvent_column_le hb hgap (hstrip i) (e i) (R (e i)) (d i) (v i)
    (fun t ↦ U t (R (e i))) (he i) (hv i) (hdiag i) (hres i) (hu0 i) (hd i) (hbound i)

open MeasureTheory in
/-- Passing the coordinate functional through the Laplace integral identifies
the resolvent diagonal from the one-dimensional flag quotient. -/
theorem laplace_diagonal_of_orthogonal_error {H : Type*} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (e : H) (u v : ℝ → H) (b : ℝ)
    (z : ℂ) (hz : z.re < b) (he : ‖e‖ = 1)
    (hu : ∀ t, u t = Complex.exp (z * (t : ℂ)) • e + v t)
    (hv : ∀ t, inner ℂ e (v t) = 0)
    (hint : IntegrableOn (fun t : ℝ ↦ Complex.exp (-(b : ℂ) * (t : ℂ)) • u t) (Ioi 0)) :
    inner ℂ e (∫ t : ℝ in Ioi 0, Complex.exp (-(b : ℂ) * (t : ℂ)) • u t) =
      ((b : ℂ) - z)⁻¹ := by
  change innerSL ℂ e (∫ t : ℝ in Ioi 0, Complex.exp (-(b : ℂ) * (t : ℂ)) • u t) = _
  rw [← (innerSL ℂ e).integral_comp_comm hint]
  have hpoint (t : ℝ) :
      innerSL ℂ e (Complex.exp (-(b : ℂ) * (t : ℂ)) • u t) =
        Complex.exp ((z - (b : ℂ)) * (t : ℂ)) := by
    change inner ℂ e (Complex.exp (-(b : ℂ) * (t : ℂ)) • u t) = _
    have hunit : inner ℂ e e = 1 := by
      rw [inner_self_eq_norm_sq_to_K, he]
      norm_num
    rw [hu t, inner_smul_right, inner_add_right, hv t, add_zero, inner_smul_right,
      hunit, mul_one, ← Complex.exp_add]
    congr 1
    ring
  simp_rw [hpoint]
  rw [integral_exp_mul_complex_Ioi (by simpa using sub_neg.mpr hz)]
  simp only [Complex.ofReal_zero, mul_zero, Complex.exp_zero, neg_div, one_div]
  rw [show z - (b : ℂ) = -((b : ℂ) - z) by ring, inv_neg, neg_neg]

end E2AResolvent

#print axioms E2AResolvent.orbit_energy_le
#print axioms E2AResolvent.energy_of_inverse_equation
#print axioms E2AResolvent.diagonal_of_orthogonal_error
#print axioms E2AResolvent.real_part_inverse_le
#print axioms E2AResolvent.summable_ordinates_of_dyadic_count
#print axioms E2AResolvent.resolvent_column_le
#print axioms E2AResolvent.summable_resolvent_columns_of_dyadic_count
#print axioms E2AResolvent.laplace_diagonal_of_orthogonal_error
