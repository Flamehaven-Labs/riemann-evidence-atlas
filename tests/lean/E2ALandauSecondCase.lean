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

namespace E2ALandauSecondCase

def kernel (u : ℝ) : ℝ := u * Real.exp (-(2*u))

def tailMass : ℝ := ∫ u in Ioi (0 : ℝ) \ Icc (1/2 : ℝ) 2, kernel u

private def primitive (u : ℝ) : ℝ := Real.exp (-(2*u)) * (-(1 + 2*u) / 4)

private theorem primitive_derivative (u : ℝ) : HasDerivAt primitive (kernel u) u := by
  have hu : HasDerivAt (fun x : ℝ => x) 1 u := hasDerivAt_id u
  have hp := (hasDerivAt_const u (1 : ℝ)).add (hu.const_mul 2)
  have he := (hu.const_mul 2).neg.exp
  convert he.mul (hp.neg.div_const 4) using 1 <;>
    first
    | rfl
    | (simp [kernel]; ring)

private theorem kernel_integrable : IntegrableOn kernel (Ioi 0) := by
  let f : ℝ → ℝ := fun t => Real.exp (-t) * t ^ ((2:ℝ) - 1)
  have hf : IntegrableOn f (Ioi 0) := Real.GammaIntegral_convergent (by norm_num : (0:ℝ) < 2)
  have h := (integrableOn_Ioi_comp_mul_left_iff f 0 (by norm_num : (0:ℝ) < 2)).2
    (by simpa only [mul_zero] using hf)
  have hd : (fun x : ℝ => (1 / 2 : ℝ) * f (2 * x)) = kernel := by
    funext x
    simp only [f, kernel, show (2 : ℝ) - 1 = 1 by norm_num, Real.rpow_one]
    ring
  rw [← hd]
  exact h.const_mul (1 / 2 : ℝ)

private theorem kernel_total : (∫ u in Ioi (0 : ℝ), kernel u) = 1 / 4 := by
  have h : (∫ u : ℝ in Ioi (0 : ℝ), u * Real.exp (-(2*u))) =
      (1/2:ℝ)^(2:ℕ) * Real.Gamma 2 := by
    have h' := Real.integral_rpow_mul_exp_neg_mul_Ioi (by norm_num : (0:ℝ) < 2)
      (by norm_num : (0:ℝ) < 2)
    simpa only [show (2:ℝ) - 1 = 1 by norm_num, Real.rpow_one, Real.rpow_ofNat] using h'
  have hg : Real.Gamma (2 : ℝ) = 1 := by norm_num [Nat.factorial]
  norm_num [kernel, h, hg]

theorem tail_mass_eq : tailMass = (1 - 2 * Real.exp (-1) + 5 * Real.exp (-4)) / 4 := by
  have hsubset : Icc (1/2 : ℝ) 2 ⊆ Ioi 0 := fun _ h => lt_of_lt_of_le (by norm_num) h.1
  have hw : (∫ u in Icc (1/2 : ℝ) 2, kernel u) = primitive 2 - primitive (1/2) := by
    rw [integral_Icc_eq_integral_Ioc, ← intervalIntegral.integral_of_le (by norm_num : (1/2:ℝ) ≤ 2)]
    apply intervalIntegral.integral_eq_sub_of_hasDerivAt (fun u _ => primitive_derivative u)
    exact (show Continuous kernel by unfold kernel; fun_prop).intervalIntegrable (1/2) 2
  rw [tailMass, setIntegral_sdiff measurableSet_Icc kernel_integrable hsubset, kernel_total, hw]
  norm_num [primitive]
  ring

open E2ALandauTail (taylorTerm taylorSum libraryRemainder)

private theorem cast_term (n : Nat) : (taylorTerm 1 n : ℝ) = 1 / n.factorial := by
  induction n with
  | zero => norm_num [taylorTerm]
  | succ n ih =>
    simp [taylorTerm, ih, Nat.factorial_succ, div_eq_mul_inv, mul_comm]

private theorem cast_sum (n : Nat) :
    (taylorSum 1 n : ℝ) = ∑ k ∈ Finset.range (n + 1), (1 : ℝ)^k / k.factorial := by
  induction n with
  | zero => norm_num [taylorSum]
  | succ n ih =>
    rw [taylorSum, Rat.cast_add, ih, cast_term]
    simpa only [one_pow] using
      (Finset.sum_range_succ (fun k => (1 : ℝ)^k / k.factorial) (n + 1)).symm

private theorem cast_remainder (n : Nat) :
    (libraryRemainder 1 n : ℝ) =
      (1 : ℝ)^(n+1) * ((n+1 : Nat) + 1 : ℝ) / (((n+1 : Nat).factorial : ℝ) * (n+1 : Nat)) := by
  simp only [libraryRemainder, Rat.cast_mul, Rat.cast_natCast,
    cast_term, one_pow, div_eq_mul_inv, Rat.cast_inv, mul_inv]
  push_cast
  ring

-- A single enclosure for exp(1) controls the two negative exponents by reciprocals.
private def eLower : Rat :=
  5806214745567907793827207199747154474831678955875791827999719186332486788515497861603488166640613 / 2^320
private def eUpper : Rat :=
  5806214745567907793827207199747154474831678955875791827999719186332486788515497861603488166640614 / 2^320

set_option maxRecDepth 4096 in
set_option maxHeartbeats 2000000 in
private theorem exp_one_arithmetic :
    0 < eLower ∧ eLower ≤ taylorSum 1 70 ∧ taylorSum 1 70 + libraryRemainder 1 70 ≤ eUpper := by
  decide +kernel

theorem exp_one_enclosed : (eLower : ℝ) ≤ Real.exp 1 ∧ Real.exp 1 ≤ (eUpper : ℝ) := by
  have hl : (eLower : ℝ) ≤ (taylorSum 1 70 : ℝ) := by exact_mod_cast exp_one_arithmetic.2.1
  have hu : (taylorSum 1 70 : ℝ) + (libraryRemainder 1 70 : ℝ) ≤ (eUpper : ℝ) := by
    exact_mod_cast exp_one_arithmetic.2.2
  rw [cast_sum] at hl
  rw [cast_sum, cast_remainder] at hu
  exact ⟨hl.trans (Real.sum_le_exp_of_nonneg zero_le_one _),
    (Real.exp_bound' zero_le_one (le_refl (1:ℝ)) (by decide : 0 < (71:Nat))).trans hu⟩

private theorem exp_neg_nat_enclosed (k : Nat) :
    ((1 / eUpper^k : Rat) : ℝ) ≤ Real.exp (-(k : ℝ)) ∧
      Real.exp (-(k : ℝ)) ≤ ((1 / eLower^k : Rat) : ℝ) := by
  have hpos : 0 < (eLower : ℝ) := by exact_mod_cast exp_one_arithmetic.1
  rw [show (k : ℝ) = (k : ℝ) * 1 by ring, Real.exp_neg, Real.exp_nat_mul, ← one_div]
  push_cast
  exact ⟨one_div_le_one_div_of_le (pow_pos (Real.exp_pos _) _)
      (pow_le_pow_left₀ (Real.exp_pos _).le exp_one_enclosed.2 _),
    one_div_le_one_div_of_le (pow_pos hpos _) (pow_le_pow_left₀ hpos.le exp_one_enclosed.1 _)⟩

def lower256 : Rat :=
  5150132692391838099305122917866226216214174311535347965444171447923760414037 / 57896044618658097711785492504343953926634992332820282019728792003956564819968
def upper256 : Rat :=
  41201061539134704794440983342929809729713394492282783723553371583390083312303 / 463168356949264781694283940034751631413079938662562256157830336031652518559744
def nearCap : Rat :=
  242158075435671337967324601779809645921 / 2722258935367507707706996859454145691648

private theorem propagated_arithmetic :
    lower256 ≤ (1 - 2 * (1 / eLower^1) + 5 * (1 / eUpper^4)) / 4 ∧
      (1 - 2 * (1 / eUpper^1) + 5 * (1 / eLower^4)) / 4 ≤ upper256 := by
  decide +kernel

theorem tail_mass_enclosed : (lower256 : ℝ) ≤ tailMass ∧ tailMass ≤ (upper256 : ℝ) := by
  have hl : (lower256 : ℝ) ≤
      (1 - 2 * ((1 / eLower^1 : Rat) : ℝ) + 5 * ((1 / eUpper^4 : Rat) : ℝ)) / 4 := by
    exact_mod_cast propagated_arithmetic.1
  have hu : (1 - 2 * ((1 / eUpper^1 : Rat) : ℝ) + 5 * ((1 / eLower^4 : Rat) : ℝ)) / 4 ≤
      (upper256 : ℝ) := by
    exact_mod_cast propagated_arithmetic.2
  have h1 := exp_neg_nat_enclosed 1
  have h4 := exp_neg_nat_enclosed 4
  simp only [Nat.cast_one] at h1
  simp only [Nat.cast_ofNat] at h4
  rw [tail_mass_eq]
  constructor
  · linarith [h1.2, h4.1]
  · linarith [h1.1, h4.2]

theorem tail_mass_caps :
    (1/20 : ℝ) < tailMass ∧ tailMass ≤ (nearCap : ℝ) ∧ tailMass ≤ 1/10 := by
  have hl : ((1/20 : Rat) : ℝ) < (lower256 : ℝ) := Rat.cast_lt.mpr (by decide +kernel)
  have hn : (upper256 : ℝ) ≤ (nearCap : ℝ) := Rat.cast_le.mpr (by decide +kernel)
  have hu : (upper256 : ℝ) ≤ ((1/10 : Rat) : ℝ) := Rat.cast_le.mpr (by decide +kernel)
  exact ⟨by simpa only [Rat.cast_div, Rat.cast_one, Rat.cast_ofNat] using
      hl.trans_le tail_mass_enclosed.1,
    tail_mass_enclosed.2.trans hn,
    by simpa only [Rat.cast_div, Rat.cast_one, Rat.cast_ofNat] using
      tail_mass_enclosed.2.trans hu⟩

#print axioms tail_mass_eq
#print axioms exp_one_enclosed
#print axioms tail_mass_enclosed
#print axioms tail_mass_caps

end E2ALandauSecondCase
end
