import Lean.Util.FoldConsts

-- This is a test of expression-reference custody, not an original RH result.
noncomputable def auditChosenNat : Nat :=
  Classical.choice (show Nonempty Nat from ⟨7⟩)

noncomputable def auditComputedFromChosen : Nat :=
  auditChosenNat + 1

theorem auditProofMentionsComputed : auditComputedFromChosen = auditComputedFromChosen := by
  rfl

theorem auditProofCallsChoice : Nonempty Nat :=
  Classical.choice (show Nonempty (Nonempty Nat) from ⟨⟨7⟩⟩)

theorem auditIndependent : True := True.intro

axiom auditFixtureAxiom : True

noncomputable opaque auditOpaque : Nat := auditChosenNat

theorem auditJoinChoicePaths : Nonempty Nat ∧ auditComputedFromChosen = auditComputedFromChosen :=
  ⟨auditProofCallsChoice, auditProofMentionsComputed⟩
