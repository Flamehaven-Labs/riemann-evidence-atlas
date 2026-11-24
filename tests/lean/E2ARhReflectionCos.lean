import Mathlib.Analysis.SpecialFunctions.Trigonometric.Complex
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

namespace E2ARhReflection

open Complex

theorem cos_reflection_eq_zero_iff {s : ℂ} :
    cos ((Real.pi : ℂ) * (1 - s) / 2) = 0 ↔ ∃ k : ℤ, s = -2 * (k : ℂ) := by
  rw [Complex.cos_eq_zero_iff]
  constructor
  · rintro ⟨k, hk⟩
    have hpi : (Real.pi : ℂ) ≠ 0 := by exact_mod_cast Real.pi_ne_zero
    have hprod : ((1 - s) - (2 * (k : ℂ) + 1)) * (Real.pi : ℂ) = 0 := by
      linear_combination 2 * hk
    have h := (mul_eq_zero.mp hprod).resolve_right hpi
    exact ⟨k, by linear_combination -h⟩
  · rintro ⟨k, rfl⟩
    exact ⟨k, by ring⟩

-- Below real part 2, the reflection factor vanishes exactly at 0 and the negative evens.
theorem cos_reflection_zeros_below_two {s : ℂ} (hs : s.re < 2) :
    cos ((Real.pi : ℂ) * (1 - s) / 2) = 0 ↔ ∃ n : ℕ, s = -2 * (n : ℂ) := by
  rw [cos_reflection_eq_zero_iff]
  constructor
  · rintro ⟨k, hk⟩
    have hre : s.re = -2 * (k : ℝ) := by
      rw [hk, Complex.mul_re]
      simp
    have hk0 : 0 ≤ k := by
      by_contra h
      have hneg : (k : ℝ) ≤ -1 := by exact_mod_cast (show k ≤ -1 by omega)
      linarith
    have hcast : ((k.toNat : ℕ) : ℂ) = (k : ℂ) := by
      exact_mod_cast Int.toNat_of_nonneg hk0
    exact ⟨k.toNat, by simpa only [hcast] using hk⟩
  · rintro ⟨n, hn⟩
    exact ⟨(n : ℤ), by simpa using hn⟩

theorem cos_reflection_ne_zero_in_original_branch {s : ℂ}
    (hs : s.re < 1 / 2) (h0 : s ≠ 0) (htriv : ¬∃ n : ℕ, s = -2 * (n + 1 : ℂ)) :
    cos ((Real.pi : ℂ) * (1 - s) / 2) ≠ 0 := by
  intro hz
  obtain ⟨n, hn⟩ := (cos_reflection_zeros_below_two (by linarith)).mp hz
  cases n with
  | zero => exact h0 (by simpa using hn)
  | succ n => exact htriv ⟨n, by simpa only [Nat.cast_succ] using hn⟩

theorem cos_reflection_at_two :
    cos ((Real.pi : ℂ) * (1 - 2) / 2) = 0 ∧ ¬∃ n : ℕ, (2 : ℂ) = -2 * (n : ℂ) := by
  constructor
  · exact cos_reflection_eq_zero_iff.mpr ⟨-1, by norm_num⟩
  · rintro ⟨n, hn⟩
    have hre := congrArg Complex.re hn
    norm_num [Complex.mul_re] at hre
    have hn0 : (0 : ℝ) ≤ (n : ℝ) := n.cast_nonneg
    linarith

#print axioms cos_reflection_eq_zero_iff
#print axioms cos_reflection_zeros_below_two
#print axioms cos_reflection_ne_zero_in_original_branch
#print axioms cos_reflection_at_two

end E2ARhReflection
