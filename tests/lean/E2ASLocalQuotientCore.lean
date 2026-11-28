import Mathlib.Data.Real.Basic
import Mathlib.NumberTheory.Padics.PadicNorm
import Mathlib.Tactic.NormNum

/-! The dyadic witnesses for failure of uniform local constancy.
The Schwartz–Bruhat tensor description and the Fourier calculation are used in
the accompanying analytic proof. -/

namespace E2ASLocalQuotientCore

private instance : Fact (Nat.Prime 2) := ⟨Nat.prime_two⟩

theorem dyadic_product_norm (r : ℝ) (n : ℕ) :
    (r * 2 ^ n) * (padicNorm 2 ((2 : ℚ) ^ n) : ℝ) = r := by
  have hq : padicNorm 2 ((2 : ℚ) ^ n) = ((2 : ℚ)⁻¹) ^ n := by
    have htwo : padicNorm 2 (2 : ℚ) = (2 : ℚ)⁻¹ :=
      padicNorm.padicNorm_p (p := 2) (by decide)
    induction n with
    | zero => simp
    | succ n ih => rw [pow_succ, padicNorm.mul, ih, htwo, pow_succ]
  rw [hq]
  push_cast
  rw [mul_assoc, ← mul_pow, mul_inv_cancel₀ (by norm_num : (2 : ℝ) ≠ 0), one_pow, mul_one]

/-- Every common dyadic depth has two inputs in the same zero coset that a
product-norm multiplier distinguishes. The real Fourier factor is assumed
nonzero somewhere in every positive open interval. -/
theorem no_uniform_dyadic_level
    (g mask : ℝ → ℝ) {a b : ℝ} (ha : 0 < a) (hab : a < b)
    (hmask : ∀ r ∈ Set.Ioo a b, mask r ≠ mask 0)
    (hg : ∀ l u : ℝ, 0 < l → l < u → ∃ x ∈ Set.Ioo l u, g x ≠ 0) :
    ∀ n : ℕ, ∃ x > 0,
      g x * mask (x * (padicNorm 2 ((2 : ℚ) ^ n) : ℝ)) ≠
      g x * mask (x * (padicNorm 2 0 : ℝ)) := by
  intro n
  have hn : 0 < (2 : ℝ) ^ n := pow_pos (by norm_num) _
  obtain ⟨x, hx, hgx⟩ :=
    hg (a * 2 ^ n) (b * 2 ^ n) (mul_pos ha hn) (mul_lt_mul_of_pos_right hab hn)
  have hx0 : 0 < x := (mul_pos ha hn).trans hx.1
  let r := x / (2 : ℝ) ^ n
  have hr : r ∈ Set.Ioo a b :=
    ⟨(lt_div_iff₀ hn).mpr hx.1, (div_lt_iff₀ hn).mpr hx.2⟩
  have hxr : r * 2 ^ n = x := div_mul_cancel₀ x hn.ne'
  have heq := dyadic_product_norm r n
  rw [hxr] at heq
  refine ⟨x, hx0, ?_⟩
  rw [heq, padicNorm.zero, Rat.cast_zero, mul_zero]
  intro h
  exact hmask r hr (mul_left_cancel₀ hgx h)

end E2ASLocalQuotientCore

#print axioms E2ASLocalQuotientCore.dyadic_product_norm
#print axioms E2ASLocalQuotientCore.no_uniform_dyadic_level

