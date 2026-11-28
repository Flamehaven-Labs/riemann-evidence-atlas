import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.Calculus.Deriv.Support
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.SmoothTransition
import Mathlib.MeasureTheory.Integral.IntegralEqImproper
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-! A fixed radial test for the geometric trace comparison over ℚ. -/

namespace E2AGeometricTraceTest

open Filter Function MeasureTheory Set
open scoped ContDiff Topology

/-- Support radius 1/4 around log 2, with a plateau near the center. -/
noncomputable def bump (t : ℝ) : ℝ :=
  Real.smoothTransition (2 - 32 * (t - Real.log 2)^2)

noncomputable def kernel (t : ℝ) : ℝ :=
  deriv (deriv bump) t - bump t / 4

noncomputable def mellin (f : ℝ → ℝ) (z : ℝ) : ℝ :=
  ∫ t : ℝ, f t * Real.exp (z * t)

private theorem bump_smooth : ContDiff ℝ ∞ bump := by
  unfold bump
  exact Real.smoothTransition.contDiff.comp (by fun_prop)

private theorem bump_support :
    tsupport bump ⊆ Icc (Real.log 2 - 1/4) (Real.log 2 + 1/4) := by
  apply closure_minimal _ isClosed_Icc
  intro t ht
  change bump t ≠ 0 at ht
  have hpos : 0 < 2 - 32 * (t - Real.log 2)^2 := by
    exact lt_of_not_ge fun h ↦ ht (Real.smoothTransition.zero_of_nonpos h)
  have hsq : (t - Real.log 2)^2 < (1/4 : ℝ)^2 := by nlinarith
  have habs := abs_lt_of_sq_lt_sq' hsq (by norm_num)
  exact ⟨by linarith [habs.1], by linarith [habs.2]⟩

private theorem bump_compact : HasCompactSupport bump :=
  isCompact_Icc.of_isClosed_subset isClosed_closure bump_support

private theorem bracket_inside :
    Icc (Real.log 2 - 1/4) (Real.log 2 + 1/4) ⊆ Ioo 0 (Real.log 3) := by
  have low := Real.log_le_sub_one_of_pos (show 0 < (2 : ℝ)⁻¹ by norm_num)
  rw [Real.log_inv] at low
  have high := Real.log_le_sub_one_of_pos (show 0 < (2/3 : ℝ) by norm_num)
  rw [Real.log_div (by norm_num) (by norm_num)] at high
  intro t ht
  exact ⟨by linarith [ht.1], by linarith [ht.2]⟩

/-- The fixed test is smooth and vanishes outside the stated compact bracket. -/
theorem kernel_smooth_and_supported :
    ContDiff ℝ ∞ kernel ∧
      tsupport kernel ⊆ Icc (Real.log 2 - 1/4) (Real.log 2 + 1/4) := by
  have hd := (contDiff_infty_iff_deriv.mp bump_smooth).2
  refine ⟨(contDiff_infty_iff_deriv.mp hd).2.sub (bump_smooth.div_const 4), ?_⟩
  apply closure_minimal _ isClosed_Icc
  intro t ht
  change kernel t ≠ 0 at ht
  by_contra ht'
  have hb : bump t = 0 := by
    by_contra h
    exact ht' (bump_support (subset_closure h))
  have hd₂ : deriv (deriv bump) t = 0 := by
    by_contra h
    exact ht' (bump_support (tsupport_deriv_subset (support_deriv_subset h)))
  simp [kernel, hb, hd₂] at ht

/-- In particular the norm-one classes and all nonpositive log norms give zero. -/
theorem kernel_eq_zero_outside {t : ℝ} (ht : t ∉ Ioo 0 (Real.log 3)) :
    kernel t = 0 := by
  by_contra h
  exact ht (bracket_inside (kernel_smooth_and_supported.2 (subset_closure h)))

/-- Among log norms of finite-place shells, only the norm-2 shell can contribute. -/
theorem kernel_zero_on_other_shells {p : ℕ} {m : ℤ} (hp : 2 ≤ p)
    (h : ¬ (p = 2 ∧ m = -1)) : kernel (-(m : ℝ) * Real.log p) = 0 := by
  apply kernel_eq_zero_outside
  intro ht
  have hp' : (2 : ℝ) ≤ p := by exact_mod_cast hp
  have hpos : 0 < Real.log (p : ℝ) := Real.log_pos (by linarith)
  have hm : m ≤ -1 := by
    by_contra! hneg
    have hm' : (0 : ℝ) ≤ m := by exact_mod_cast (show 0 ≤ m by omega)
    exact (not_lt_of_ge (mul_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr hm') hpos.le)) ht.1
  by_cases hp2 : p = 2
  · have hm2 : m ≤ -2 := by
      have hne : m ≠ -1 := fun hm' ↦ h ⟨hp2, hm'⟩
      omega
    have hm2' : (m : ℝ) ≤ -2 := by exact_mod_cast hm2
    have hlog : Real.log 3 < 2 * Real.log 2 := by
      simpa [Real.log_pow] using Real.log_lt_log (by norm_num : (0 : ℝ) < 3)
        (by norm_num : (3 : ℝ) < (2 : ℝ)^2)
    have hmul := mul_le_mul_of_nonneg_right (show (2 : ℝ) ≤ -(m : ℝ) by linarith) hpos.le
    rw [hp2] at hmul ht
    exact (hlog.le.trans hmul).not_gt ht.2
  · have hp3 : (3 : ℝ) ≤ p := by exact_mod_cast (show 3 ≤ p by omega)
    have hlog : Real.log 3 ≤ Real.log (p : ℝ) :=
      (Real.log_le_log_iff (by norm_num) (by linarith)).2 hp3
    have hm' : (m : ℝ) ≤ -1 := by exact_mod_cast hm
    have hmul := mul_le_mul_of_nonneg_right (show (1 : ℝ) ≤ -(m : ℝ) by linarith) hpos.le
    rw [one_mul] at hmul
    exact (hlog.trans hmul).not_gt ht.2

/-- The plateau forces the exact value at the non-unit shell of norm 2. -/
theorem kernel_at_log_two : kernel (Real.log 2) = -1/4 := by
  have h : bump =ᶠ[𝓝 (Real.log 2)] (fun _ ↦ (1 : ℝ)) := by
    filter_upwards [Metric.ball_mem_nhds (Real.log 2) (show (0 : ℝ) < 1/8 by norm_num)] with t ht
    rw [Metric.mem_ball, Real.dist_eq] at ht
    have hsq : (t - Real.log 2)^2 < (1/8 : ℝ)^2 :=
      sq_lt_sq.mpr (by simpa only [abs_of_pos (show (0 : ℝ) < 1/8 by norm_num)] using ht)
    exact Real.smoothTransition.one_of_one_le (by nlinarith)
  have h₂ : deriv (deriv bump) (Real.log 2) = 0 := by
    simpa using h.deriv.deriv_eq
  rw [kernel, h₂, h.eq_of_nhds]
  norm_num

private theorem mellin_deriv (f : ℝ → ℝ) (hf : ContDiff ℝ ∞ f)
    (hc : HasCompactSupport f) (z : ℝ) :
    mellin (deriv f) z = -z * mellin f z := by
  let v (t : ℝ) := Real.exp (z * t)
  let v' (t : ℝ) := z * v t
  have hv : ∀ t, HasDerivAt v (v' t) t := by
    intro t
    simpa [v, v', mul_comm] using (hasDerivAt_id t).const_mul z |>.exp
  have hf' := (contDiff_infty_iff_deriv.mp hf).2
  have cv : Continuous v := by fun_prop
  have cv' : Continuous v' := by fun_prop
  have h := integral_mul_deriv_eq_deriv_mul_of_integrable
    (u := f) (u' := deriv f) (v := v) (v' := v')
    (fun t _ ↦ ((hf.differentiable (by simp)) t).hasDerivAt)
    (fun t _ ↦ hv t)
    ((hf.continuous.mul cv').integrable_of_hasCompactSupport hc.mul_right)
    ((hf'.continuous.mul cv).integrable_of_hasCompactSupport hc.deriv.mul_right)
    ((hf.continuous.mul cv).integrable_of_hasCompactSupport hc.mul_right)
  change (∫ t : ℝ, f t * (z * v t)) = -mellin (deriv f) z at h
  simp_rw [mul_left_comm (f _) z, integral_const_mul] at h
  change z * mellin f z = -mellin (deriv f) z at h
  linarith

/-- The multiplier identity on the real axis, including both polar points. -/
theorem kernel_mellin (z : ℝ) :
    mellin kernel z = (z^2 - 1/4) * mellin bump z := by
  let v (t : ℝ) := Real.exp (z * t)
  have cv : Continuous v := by fun_prop
  have hd := (contDiff_infty_iff_deriv.mp bump_smooth).2
  have hd₂ := (contDiff_infty_iff_deriv.mp hd).2
  have i₂ : Integrable (fun t ↦ deriv (deriv bump) t * v t) :=
    (hd₂.continuous.mul cv).integrable_of_hasCompactSupport bump_compact.deriv.deriv.mul_right
  have i₀ : Integrable (fun t ↦ ((4 : ℝ)⁻¹ * bump t) * v t) :=
    ((continuous_const.mul bump_smooth.continuous).mul cv).integrable_of_hasCompactSupport
      bump_compact.mul_left.mul_right
  change (∫ t : ℝ, (deriv (deriv bump) t - bump t / 4) * v t) = _
  simp_rw [div_eq_inv_mul, sub_mul]
  rw [integral_sub i₂ i₀]
  simp_rw [mul_assoc, integral_const_mul]
  change mellin (deriv (deriv bump)) z - (4 : ℝ)⁻¹ * mellin bump z = _
  rw [mellin_deriv _ hd bump_compact.deriv, mellin_deriv _ bump_smooth bump_compact]
  ring

theorem polar_moments_eq_zero :
    mellin kernel (-1/2) = 0 ∧ mellin kernel (1/2) = 0 := by
  constructor <;> rw [kernel_mellin] <;> norm_num

/-- The expected local factor after Haar-volume cancellation on the norm-2 shell. -/
theorem prime_two_term :
    Real.log 2 / Real.sqrt 2 * kernel (Real.log 2) = -Real.log 2 / (4 * Real.sqrt 2) := by
  rw [kernel_at_log_two]
  have h : Real.sqrt (2 : ℝ) ≠ 0 := by positivity
  field_simp

end E2AGeometricTraceTest

#print axioms E2AGeometricTraceTest.kernel_smooth_and_supported
#print axioms E2AGeometricTraceTest.kernel_eq_zero_outside
#print axioms E2AGeometricTraceTest.kernel_zero_on_other_shells
#print axioms E2AGeometricTraceTest.kernel_at_log_two
#print axioms E2AGeometricTraceTest.kernel_mellin
#print axioms E2AGeometricTraceTest.polar_moments_eq_zero
#print axioms E2AGeometricTraceTest.prime_two_term
