import Lean
import Statements
import RiemannMasullo.Ch13_ZerosHecke.RationalExteriorZeros

open Lean Meta Elab Term in
elab "atlas_type_of% " t:term : term => do
  let expr ← elabTerm t none
  synthesizeSyntheticMVarsNoPostponing
  inferType (← instantiateMVars expr)


theorem atlas_exterior_zeros_of_archived_statement
    (h : DirichletLNonvanishingRightOfHalf) :
    atlas_type_of% (@RiemannMasullo.traceFormula_exteriorZeros_rat_of_dirichletGRH h) :=
  @RiemannMasullo.traceFormula_exteriorZeros_rat_of_dirichletGRH h

#check atlas_exterior_zeros_of_archived_statement
#print axioms atlas_exterior_zeros_of_archived_statement
