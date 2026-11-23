import Lean.Data.Json.FromToJson
import Lean.Environment
import Lean.Util.FoldConsts

open Lean

private structure CatalogRequest where
  names : List String
  artifacts : List (String × String)
  includeInit : Bool
  deriving FromJson

private def kindOf : ConstantInfo → String
  | .axiomInfo _ => "axiom"
  | .thmInfo _ => "theorem"
  | .defnInfo _ => "definition"
  | .opaqueInfo _ => "opaque"
  | .inductInfo _ => "inductive"
  | .ctorInfo _ => "constructor"
  | .recInfo _ => "recursor"
  | .quotInfo _ => "quotient"

private def refs (term : Expr) : Json :=
  toJson (term.getUsedConstants.map Name.toString |>.qsort (· < ·))

private def describe (info : ConstantInfo) (moduleName evidence : String)
    (imports : Array String := #[]) : Json :=
  let value := info.value? (allowOpaque := true)
  Json.mkObj [
    ("schema", toJson "riemann-evidence-direct-proof-refs-v2"),
    ("declaration", toJson info.name.toString),
    ("module", toJson moduleName),
    ("evidence", toJson evidence),
    ("kind", toJson (kindOf info)),
    ("module_imports", toJson imports),
    ("type_refs", refs info.type),
    ("has_value", toJson value.isSome),
    ("value_refs", (value.map refs).getD Json.null)
  ]

def main (args : List String) : IO Unit := do
  let [file] := args
    | throw (IO.userError "usage: lean --run tools/ProofCatalog.lean REQUEST.json")
  let raw ← IO.FS.readFile file
  let .ok request := Json.parse raw >>= fromJson? (α := CatalogRequest)
    | throw (IO.userError "expected names, artifacts, and includeInit")
  let targets : Std.HashSet String := request.names.foldl (fun acc name => acc.insert name) {}
  let mut found : Array Json := #[]
  if request.includeInit then
    let env ← importModules #[{ module := `Init }] {}
    found := env.constants.fold (init := found) fun rows name info =>
      if targets.contains name.toString then
        match env.getModuleIdxFor? name with
        | some idx => match env.header.moduleNames[idx.toNat]? with
          | some moduleName => rows.push (describe info moduleName.toString "LEAN_TOOLCHAIN_ENVIRONMENT")
          | none => rows
        | none => rows
      else rows
  for (moduleName, path) in request.artifacts do
    let (data, _) ← readModuleData ⟨path⟩
    let imports := data.imports.map (·.module.toString)
    for info in data.constants do
      if targets.contains info.name.toString then
        found := found.push (describe info moduleName "SUPPLIED_OLEAN" imports)
  IO.println (toJson found).compress
