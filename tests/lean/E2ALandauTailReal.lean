import Mathlib.Analysis.Complex.Exponential
import Mathlib.Analysis.SpecialFunctions.Gamma.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring
import E2ALandauTailRational

open MeasureTheory Set

noncomputable section

namespace E2ALandauTail

private theorem cast_term (y : Rat) (n : Nat) :
    (taylorTerm y n : ℝ) = (y : ℝ)^n / n.factorial := by
  induction n with
  | zero => norm_num [taylorTerm]
  | succ n ih =>
    simp [taylorTerm, ih, pow_succ, Nat.factorial_succ, div_eq_mul_inv,
      mul_assoc, mul_left_comm, mul_comm]

private theorem cast_sum (y : Rat) (n : Nat) :
    (taylorSum y n : ℝ) = ∑ k ∈ Finset.range (n + 1), (y : ℝ)^k / k.factorial := by
  induction n with
  | zero => norm_num [taylorSum]
  | succ n ih =>
    rw [taylorSum, Rat.cast_add, ih, cast_term]
    exact (Finset.sum_range_succ _ (n + 1)).symm

private theorem cast_library_remainder (y : Rat) (n : Nat) :
    (libraryRemainder y n : ℝ) =
      (y : ℝ)^(n+1) * ((n+1 : Nat) + 1 : ℝ) / (((n+1 : Nat).factorial : ℝ) * (n+1 : Nat)) := by
  simp only [libraryRemainder, Rat.cast_mul, Rat.cast_add, Rat.cast_one, Rat.cast_natCast,
    cast_term, div_eq_mul_inv, Rat.cast_inv, mul_inv]
  ring

private theorem small_exp_bounds {y lo hi : Rat} {n : Nat}
    (hy0 : 0 ≤ (y : ℝ)) (hy1 : (y : ℝ) ≤ 1)
    (hl : lo ≤ taylorSum y n) (hu : taylorSum y n + libraryRemainder y n ≤ hi) :
    (lo : ℝ) ≤ Real.exp (y : ℝ) ∧ Real.exp (y : ℝ) ≤ (hi : ℝ) := by
  have hl' : (lo : ℝ) ≤ (taylorSum y n : ℝ) := by exact_mod_cast hl
  have hu' : (taylorSum y n : ℝ) + (libraryRemainder y n : ℝ) ≤ (hi : ℝ) := by
    exact_mod_cast hu
  rw [cast_sum] at hl'
  rw [cast_sum, cast_library_remainder] at hu'
  exact ⟨hl'.trans (Real.sum_le_exp_of_nonneg hy0 _),
    (Real.exp_bound' hy0 hy1 (Nat.succ_pos n)).trans hu'⟩

private theorem reciprocal_exp_bounds {y lo hi low high : ℝ} (k : Nat)
    (hp : 0 < lo) (hb : lo ≤ Real.exp y ∧ Real.exp y ≤ hi)
    (hl : low ≤ 1 / hi^k) (hu : 1 / lo^k ≤ high) :
    low ≤ Real.exp (-((k : ℝ) * y)) ∧ Real.exp (-((k : ℝ) * y)) ≤ high := by
  rw [Real.exp_neg, Real.exp_nat_mul, ← one_div]
  exact ⟨hl.trans (one_div_le_one_div_of_le (pow_pos (Real.exp_pos _) _)
    (pow_le_pow_left₀ (Real.exp_pos _).le hb.2 _)),
    (one_div_le_one_div_of_le (pow_pos hp _) (pow_le_pow_left₀ hp.le hb.1 _)).trans hu⟩

theorem exp_neg_three_enclosed :
    (exp3Lower : ℝ) ≤ Real.exp (-3) ∧ Real.exp (-3) ≤ (exp3Upper : ℝ) := by
  have h := small_exp_bounds (n := 37) (by norm_num : 0 ≤ ((3 / 8 : Rat) : ℝ))
    (by norm_num) small3_arithmetic.2.1 small3_library_arithmetic
  have hpos : 0 < (small3Lower : ℝ) := by exact_mod_cast small3_arithmetic.1
  have hl : (exp3Lower : ℝ) ≤ 1 / (small3Upper : ℝ)^8 := by
    exact_mod_cast reciprocal3_arithmetic.1
  have hu : 1 / (small3Lower : ℝ)^8 ≤ (exp3Upper : ℝ) := by
    exact_mod_cast reciprocal3_arithmetic.2
  convert reciprocal_exp_bounds 8 hpos h hl hu using 1 <;> norm_num

theorem exp_neg_nine_enclosed :
    (exp9Lower : ℝ) ≤ Real.exp (-9) ∧ Real.exp (-9) ≤ (exp9Upper : ℝ) := by
  have h := small_exp_bounds (n := 34) (by norm_num : 0 ≤ ((9 / 32 : Rat) : ℝ))
    (by norm_num) small9_arithmetic.2.1 small9_library_arithmetic
  have hpos : 0 < (small9Lower : ℝ) := by exact_mod_cast small9_arithmetic.1
  have hl : (exp9Lower : ℝ) ≤ 1 / (small9Upper : ℝ)^32 := by
    exact_mod_cast reciprocal9_arithmetic.1
  have hu : 1 / (small9Lower : ℝ)^32 ≤ (exp9Upper : ℝ) := by
    exact_mod_cast reciprocal9_arithmetic.2
  convert reciprocal_exp_bounds 32 hpos h hl hu using 1 <;> norm_num

def kernel (u : ℝ) : ℝ := u^3 * Real.exp (-(3*u)) / 6

def tailMass : ℝ := ∫ u in Ioi (0 : ℝ) \ Icc (1 : ℝ) 3, kernel u

private def primitive (u : ℝ) : ℝ :=
  Real.exp (-(3*u)) * (-(1 + 3*u + (9/2)*u^2 + (9/2)*u^3) / 81)

private theorem primitive_derivative (u : ℝ) : HasDerivAt primitive (kernel u) u := by
  have hu : HasDerivAt (fun x : ℝ => x) 1 u := hasDerivAt_id u
  have hp := (((hasDerivAt_const u (1 : ℝ)).add (hu.const_mul 3)).add
    ((hu.pow 2).const_mul (9/2))).add ((hu.pow 3).const_mul (9/2))
  have he := (hu.const_mul 3).neg.exp
  convert he.mul (hp.neg.div_const 81) using 1 <;>
    first
    | rfl
    | (simp [kernel]; ring)

private theorem kernel_integrable : IntegrableOn kernel (Ioi 0) := by
  let f : ℝ → ℝ := fun t => Real.exp (-t) * t ^ ((4:ℝ) - 1)
  have hf : IntegrableOn f (Ioi 0) := Real.GammaIntegral_convergent (by norm_num : (0:ℝ) < 4)
  have h := (integrableOn_Ioi_comp_mul_left_iff f 0 (by norm_num : (0:ℝ) < 3)).2
    (by simpa only [mul_zero] using hf)
  have hd : (fun x : ℝ => (1 / 162 : ℝ) * f (3 * x)) = kernel := by
    funext x
    simp only [f, kernel]
    rw [show (4 : ℝ) - 1 = 3 by norm_num, Real.rpow_ofNat]
    ring
  rw [← hd]
  exact h.const_mul (1 / 162 : ℝ)

private theorem kernel_total : (∫ u in Ioi (0 : ℝ), kernel u) = 1 / 81 := by
  have h : (∫ u : ℝ in Ioi (0 : ℝ), u^(3:ℕ) * Real.exp (-(3*u))) =
      (1/3:ℝ)^(4:ℕ) * Real.Gamma 4 := by
    have h' := Real.integral_rpow_mul_exp_neg_mul_Ioi (by norm_num : (0:ℝ) < 4)
      (by norm_num : (0:ℝ) < 3)
    simpa only [show (4:ℝ) - 1 = 3 by norm_num, Real.rpow_ofNat] using h'
  have hg : Real.Gamma (4 : ℝ) = 6 := by norm_num [Nat.factorial]
  simp only [kernel, integral_div, h, hg]
  norm_num

theorem tail_mass_eq :
    tailMass = (1 - 13 * Real.exp (-3) + 172 * Real.exp (-9)) / 81 := by
  have hsubset : Icc (1 : ℝ) 3 ⊆ Ioi 0 := fun _ h => lt_of_lt_of_le zero_lt_one h.1
  have hw : (∫ u in Icc (1 : ℝ) 3, kernel u) = primitive 3 - primitive 1 := by
    rw [integral_Icc_eq_integral_Ioc, ← intervalIntegral.integral_of_le (by norm_num : (1:ℝ) ≤ 3)]
    apply intervalIntegral.integral_eq_sub_of_hasDerivAt (fun u _ => primitive_derivative u)
    exact (show Continuous kernel by unfold kernel; fun_prop).intervalIntegrable 1 3
  rw [tailMass, setIntegral_sdiff measurableSet_Icc kernel_integrable hsubset, kernel_total, hw]
  norm_num [primitive]
  ring

theorem tail_mass_enclosed : (tailLower : ℝ) ≤ tailMass ∧ tailMass ≤ (tailUpper : ℝ) := by
  rw [tail_mass_eq]
  push_cast [tailLower, tailUpper, E2ATailEndpointAlgebra.propagatedLower,
    E2ATailEndpointAlgebra.propagatedUpper]
  constructor
  · linarith [exp_neg_three_enclosed.2, exp_neg_nine_enclosed.1]
  · linarith [exp_neg_three_enclosed.1, exp_neg_nine_enclosed.2]

theorem tail_mass_caps : 1 / 300 < tailMass ∧ tailMass ≤ 1 / 200 := by
  have hl : ((1 / 300 : Rat) : ℝ) < (tailLower : ℝ) := Rat.cast_lt.mpr cap_comparisons.1
  have hu : (tailUpper : ℝ) ≤ ((1 / 200 : Rat) : ℝ) := Rat.cast_le.mpr cap_comparisons.2
  exact ⟨by simpa only [Rat.cast_div, Rat.cast_one, Rat.cast_ofNat] using
      hl.trans_le tail_mass_enclosed.1,
    by simpa only [Rat.cast_div, Rat.cast_one, Rat.cast_ofNat] using
      tail_mass_enclosed.2.trans hu⟩

#print axioms exp_neg_three_enclosed
#print axioms exp_neg_nine_enclosed
#print axioms tail_mass_eq
#print axioms tail_mass_enclosed
#print axioms tail_mass_caps

end E2ALandauTail
end
