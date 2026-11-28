import Mathlib.Analysis.Normed.Group.Uniform
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Topology.Algebra.Order.Field
import Mathlib.Tactic.NormNum

/-! Limit calculus for the four unfolded cutoff terms. The Fourier estimates
are hypotheses here. -/

namespace E2ASLocalCutoffSchedule

open Filter Set
open scoped Topology

variable {E : Type*} [NormedAddCommGroup E]

/-- Inclusion–exclusion for a product cutoff P and a quotient of cutoffs R. -/
noncomputable def bandDifference (d : ℝ → E) (P R : ℝ) : E :=
  d P - d R - d R⁻¹ + d P⁻¹

theorem small_limit_of_sqrt_bound (d : ℝ → E) (K : ℝ)
    (h : ∀ x > 0, ‖d x‖ ≤ K * Real.sqrt x) :
    Tendsto d (𝓝[>] (0 : ℝ)) (𝓝 0) := by
  have hs : Tendsto (fun x : ℝ ↦ Real.sqrt x) (𝓝[>] (0 : ℝ)) (𝓝 0) := by
    simpa only [Real.sqrt_zero] using
      (Real.continuous_sqrt.continuousAt (x := (0 : ℝ))).mono_left nhdsWithin_le_nhds
  refine squeeze_zero_norm' ?_ (by simpa only [mul_zero] using hs.const_mul K)
  filter_upwards [self_mem_nhdsWithin (s := Ioi (0 : ℝ))] with x hx
  exact h x hx

private theorem inv_tendsto_zero_right {ι : Type*} {l : Filter ι} {u : ι → ℝ}
    (h : Tendsto u l atTop) :
    Tendsto (fun x ↦ (u x)⁻¹) l (𝓝[>] (0 : ℝ)) := by
  refine tendsto_nhdsWithin_iff.mpr ⟨tendsto_inv_atTop_zero.comp h, ?_⟩
  filter_upwards [tendsto_atTop.mp h (1 : ℝ)] with x hx
  exact inv_pos.mpr (zero_lt_one.trans_le hx)

/-- A positive finite cutoff ratio leaves both correction terms in the limit. -/
theorem band_limit_finite_ratio {ι : Type*} {l : Filter ι} {P R : ι → ℝ}
    (d : ℝ → E) {C : E} {q : ℝ} (hq : 0 < q)
    (h0 : Tendsto d (𝓝[>] (0 : ℝ)) (𝓝 0))
    (hinfty : Tendsto d atTop (𝓝 C))
    (hP : Tendsto P l atTop) (hR : Tendsto R l (𝓝 q))
    (hc : ContinuousAt d q) (hcInv : ContinuousAt d q⁻¹) :
    Tendsto (fun x ↦ bandDifference d (P x) (R x)) l (𝓝 (C - d q - d q⁻¹)) := by
  have hp := hinfty.comp hP
  have hpInv := h0.comp (inv_tendsto_zero_right hP)
  have hr := hc.tendsto.comp hR
  have hrInv := hcInv.tendsto.comp (hR.inv₀ hq.ne')
  simpa only [bandDifference, add_zero, Function.comp_def] using
    (((hp.sub hr).sub hrInv).add hpInv)

/-- If the product and one of the two reciprocal ratios tend to infinity,
the two large-cutoff constants cancel. -/
theorem band_limit_diverging_ratio {ι : Type*} {l : Filter ι} {P R : ι → ℝ}
    (d : ℝ → E) {C : E}
    (h0 : Tendsto d (𝓝[>] (0 : ℝ)) (𝓝 0))
    (hinfty : Tendsto d atTop (𝓝 C))
    (hP : Tendsto P l atTop) (hR : Tendsto R l atTop) :
    Tendsto (fun x ↦ bandDifference d (P x) (R x)) l (𝓝 0) := by
  have hp := hinfty.comp hP
  have hpInv := h0.comp (inv_tendsto_zero_right hP)
  have hr := hinfty.comp hR
  have hrInv := h0.comp (inv_tendsto_zero_right hR)
  simpa only [bandDifference, sub_self, sub_zero, add_zero, Function.comp_def] using
    (((hp.sub hr).sub hrInv).add hpInv)

theorem band_difference_inv_ratio (d : ℝ → E) (P R : ℝ) :
    bandDifference d P R⁻¹ = bandDifference d P R := by
  simp only [bandDifference, inv_inv, sub_sub]
  rw [add_comm (d R⁻¹) (d R)]

theorem quadratic_cutoff_limit (d : ℝ → E) {C : E}
    (h0 : Tendsto d (𝓝[>] (0 : ℝ)) (𝓝 0))
    (hinfty : Tendsto d atTop (𝓝 C)) :
    Tendsto (fun L : ℝ ↦ bandDifference d (L ^ 3) L) atTop (𝓝 0) :=
  band_limit_diverging_ratio d h0 hinfty (tendsto_pow_atTop (by norm_num)) tendsto_id

end E2ASLocalCutoffSchedule

#print axioms E2ASLocalCutoffSchedule.small_limit_of_sqrt_bound
#print axioms E2ASLocalCutoffSchedule.band_limit_finite_ratio
#print axioms E2ASLocalCutoffSchedule.band_limit_diverging_ratio
#print axioms E2ASLocalCutoffSchedule.band_difference_inv_ratio
#print axioms E2ASLocalCutoffSchedule.quadratic_cutoff_limit
