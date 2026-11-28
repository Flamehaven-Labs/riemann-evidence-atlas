import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Tactic.Abel

/-! Projection and boundary identities used in the S-local trace comparison.
The Paley–Wiener closure, trace class and cutoff limits are analytic inputs. -/
namespace E2ASLocalTraceSplit

open scoped InnerProductSpace

variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [CompleteSpace E]

/-- A solution of the weighted normal equation gives the orthogonal projection
onto the image of the subspace. -/
theorem projection_image_of_normal_equation
    (B V : Submodule 𝕜 E) [B.HasOrthogonalProjection] [V.HasOrthogonalProjection]
    (T : E →L[𝕜] E) (hV : V = B.map T.toLinearMap)
    (x b : E) (hb : b ∈ B)
    (hnormal : B.starProjection (T.adjoint (T b)) = B.starProjection (T.adjoint x)) :
    V.starProjection x = T b := by
  apply V.eq_starProjection_of_mem_of_inner_eq_zero
  · rw [hV]
    exact ⟨b, hb, rfl⟩
  · intro y hy
    rw [hV] at hy
    obtain ⟨u, hu, rfl⟩ := hy
    change ⟪x - T b, T u⟫_𝕜 = 0
    rw [← T.adjoint_inner_left, map_sub]
    have hp : B.starProjection (T.adjoint x - T.adjoint (T b)) = 0 := by
      rw [map_sub, hnormal, sub_self]
    rw [← B.starProjection_eq_self_iff.mpr hu, ← B.inner_starProjection_left_eq_right,
      hp, inner_zero_left]

/-- After the unmasked polar pairing vanishes, only the spatial cutoff defect
of its representing vector enters the bound. -/
theorem polar_pairing_le_cutoff_defect
    (M : E →L[𝕜] E) (e y : E) (h : ⟪e, y⟫_𝕜 = 0) :
    ‖⟪e, M y⟫_𝕜‖ ≤ ‖M.adjoint e - e‖ * ‖y‖ := by
  rw [← M.adjoint_inner_left, ← sub_zero ⟪M.adjoint e, y⟫_𝕜, ← h, ← inner_sub_left]
  exact norm_inner_le_norm _ _

/-- With the spatial floor held fixed, subtracting the lower frequency
window leaves the four-term two-sided unfolded expression. -/
theorem unfolded_band_eq_upper_sub_low {A G : Type*} [AddCommGroup G] [Inv A]
    (d : A → G) (P R : A) :
    d P - d R - d R⁻¹ + d P⁻¹ =
      (d P - d R⁻¹) - (d R - d P⁻¹) := by
  abel

end E2ASLocalTraceSplit

#print axioms E2ASLocalTraceSplit.projection_image_of_normal_equation
#print axioms E2ASLocalTraceSplit.polar_pairing_le_cutoff_defect
#print axioms E2ASLocalTraceSplit.unfolded_band_eq_upper_sub_low

