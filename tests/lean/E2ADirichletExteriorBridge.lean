import Statements
import Mathlib.Topology.Algebra.InfiniteSum.Basic
import Mathlib.Tactic.NormNum

/-! A scoped bridge using Alpöge's archived Dirichlet statement as an input.
The tests supply no identification of completed Hecke zeros with Dirichlet zeros. -/

namespace E2ADirichletExteriorBridge

/-- The positive-order and exterior inequalities of the Sec. 12.5 index. -/
def Exterior {X : Type*} (order : X → ℂ → ℤ) (α : ℝ) :=
  {z : X × ℂ // 0 < order z.1 z.2 ∧ α ≤ |z.2.re - 1 / 2|}

/-- A character-by-character transfer of completed zeros gives an empty exterior. -/
theorem exterior_empty {X : Type*} (order : X → ℂ → ℤ)
    (level : X → ℕ) (hlevel : ∀ x, NeZero (level x))
    (χ : (x : X) → DirichletCharacter ℂ (level x))
    (hDirichlet : DirichletLZerosOnLine)
    (hStrip : ∀ x s, 0 < order x s → 0 < s.re ∧ s.re < 1)
    (hTransfer : ∀ x s, 0 < order x s → DirichletCharacter.LFunction (χ x) s = 0)
    {α : ℝ} (hα : 0 < α) : IsEmpty (Exterior order α) := by
  constructor
  intro z
  have := hlevel z.val.1
  have hs := hStrip z.val.1 z.val.2 z.property.1
  have hline := hDirichlet (level z.val.1) (χ z.val.1) z.val.2 hs.1 hs.2
    (hTransfer z.val.1 z.val.2 z.property.1)
  exact (not_le_of_gt hα) (by simpa [hline] using z.property.2)

/-- Once the index is empty, the sum vanishes for the original term or any weights. -/
theorem exterior_hasSum_zero {X : Type*} (order : X → ℂ → ℤ)
    (level : X → ℕ) (hlevel : ∀ x, NeZero (level x))
    (χ : (x : X) → DirichletCharacter ℂ (level x))
    (hDirichlet : DirichletLZerosOnLine)
    (hStrip : ∀ x s, 0 < order x s → 0 < s.re ∧ s.re < 1)
    (hTransfer : ∀ x s, 0 < order x s → DirichletCharacter.LFunction (χ x) s = 0)
    {α : ℝ} (hα : 0 < α) (term : Exterior order α → ℂ) : HasSum term 0 := by
  have := exterior_empty order level hlevel χ hDirichlet hStrip hTransfer hα
  exact hasSum_empty

/-- A synthetic positive order at the boundary shows the need for strip membership. -/
theorem strip_only_countermodel :
    ∃ order : Unit → ℂ → ℤ,
      (∀ (x : Unit) (s : ℂ), 0 < s.re → s.re < 1 → ¬ 0 < order x s) ∧
      Nonempty (Exterior order (1 / 4)) := by
  classical
  refine ⟨fun _ s => if s = 0 then 1 else 0, ?_, ?_⟩
  · intro x s hs _
    have hne : s ≠ 0 := by
      intro h
      simp [h] at hs
    simp [hne]
  · exact ⟨⟨((), 0), by norm_num⟩⟩

#print axioms exterior_empty
#print axioms exterior_hasSum_zero
#print axioms strip_only_countermodel

end E2ADirichletExteriorBridge
