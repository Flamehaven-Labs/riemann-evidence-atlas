import Lean.Util.FoldConsts

def ProbeProperty : Prop := True

theorem probeWitness : ProbeProperty := True.intro

theorem probeTarget : ProbeProperty := probeWitness

theorem probeUsesChoice : Nonempty Nat :=
  Classical.choice (show Nonempty (Nonempty Nat) from ⟨⟨7⟩⟩)

noncomputable def probeChosenNat : Nat :=
  Classical.choice (show Nonempty Nat from ⟨7⟩)
