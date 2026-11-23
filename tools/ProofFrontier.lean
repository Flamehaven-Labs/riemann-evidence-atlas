import Lean.Data.Json.FromToJson
import Lean.Environment
import Lean.Util.FoldConsts

open Lean

private def kindOf : ConstantInfo → String
  | .axiomInfo _ => "axiom"
  | .thmInfo _ => "theorem"
  | .defnInfo _ => "definition"
  | .opaqueInfo _ => "opaque"
  | .inductInfo _ => "inductive"
  | .ctorInfo _ => "constructor"
  | .recInfo _ => "recursor"
  | .quotInfo _ => "quotient"

private def describe (info : ConstantInfo) (moduleName evidence : String) : Json :=
  let value := info.value? (allowOpaque := true)
  Json.mkObj [
    ("name", toJson info.name.toString),
    ("module", toJson moduleName),
    ("evidence", toJson evidence),
    ("kind", toJson (kindOf info)),
    ("has_value", toJson value.isSome),
    ("value_refs", if evidence == "PINNED_RH_OLEAN" then
        toJson (value.map fun val => val.getUsedConstants.map Name.toString |>.qsort (· < ·))
      else Json.null)
  ]

def main (args : List String) : IO Unit := do
  let [file] := args
    | throw (IO.userError "usage: lean --run tools/ProofFrontier.lean INPUT.json")
  let raw ← IO.FS.readFile file
  let .ok input := Json.parse raw >>= fromJson? (α := List String × List (String × String))
    | throw (IO.userError "expected a JSON pair of names and [module, .olean] pairs")
  let (names, artifacts) := input
  let targets : Std.HashSet String := names.foldl (fun acc name => acc.insert name) {}
  let env ← importModules #[{ module := `Init }] {}
  let mut found := env.constants.fold (init := (#[] : Array Json)) fun rows name info =>
    if targets.contains name.toString then
      match env.getModuleIdxFor? name with
      | some idx => match env.header.moduleNames[idx.toNat]? with
        | some moduleName => rows.push (describe info moduleName.toString "LEAN_TOOLCHAIN_ENVIRONMENT")
        | none => rows
      | none => rows
    else rows
  for (moduleName, path) in artifacts do
    let (data, _) ← readModuleData ⟨path⟩
    for info in data.constants do
      if targets.contains info.name.toString then
        found := found.push (describe info moduleName "PINNED_RH_OLEAN")
  IO.println (toJson found).compress
