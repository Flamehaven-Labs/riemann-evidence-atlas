import Lean.Data.Json.FromToJson
import Lean.Environment
import Lean.Util.FoldConsts

open Lean

private def refs (term : Expr) : Json :=
  toJson (term.getUsedConstants.map Name.toString |>.qsort (· < ·))

def main (args : List String) : IO Unit := do
  let [file, target] := args
    | throw (IO.userError "usage: lean --run tools/ProofRefs.lean MODULE.olean DECLARATION")
  let (moduleData, _) ← readModuleData ⟨file⟩
  let some declaration := moduleData.constants.find? (·.name.toString == target)
    | throw (IO.userError s!"Declaration not stored in this artifact: {target}")
  let kind ← match declaration with
    | .thmInfo _ => pure "theorem"
    | .defnInfo _ => pure "definition"
    | .opaqueInfo _ => pure "opaque"
    | _ => throw (IO.userError s!"Unsupported declaration kind: {target}")
  let some body := declaration.value? (allowOpaque := true)
    | throw (IO.userError s!"No stored value: {target}")
  IO.println <| (Json.mkObj [
    ("schema", toJson "riemann-evidence-direct-proof-refs-v1"),
    ("declaration", toJson target),
    ("kind", toJson kind),
    ("module_imports", toJson (moduleData.imports.map (·.module.toString))),
    ("type_refs", refs declaration.type),
    ("value_refs", refs body)
  ]).compress
