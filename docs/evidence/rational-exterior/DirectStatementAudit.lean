import Statements

theorem original_statement_defeq :
    DirichletLNonvanishingRightOfHalf =
      (∀ (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N) (s : ℂ),
        1 / 2 < s.re → (χ ≠ 1 ∨ s ≠ 1) → DirichletCharacter.LFunction χ s ≠ 0) := rfl

#print axioms original_statement_defeq
