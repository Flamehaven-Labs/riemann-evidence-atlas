import Init.Data.Rat.Lemmas

/-!
P3.1a: fixed rational endpoint propagation only.
No real exponential enclosure, actual integral identity, or RH proof is claimed.
-/

namespace E2ATailEndpointAlgebra

def exp3Lower : Rat :=
  132356730205244743173018186111025421 / 2658455991569831745807614120560689152

def exp3Upper : Rat :=
  16941661466271327126146327822211253889 / 340282366920938463463374607431768211456

def exp9Lower : Rat :=
  20997090117932310769386338569904347 / 170141183460469231731687303715884105728

def exp9Upper : Rat :=
  41994180235864621538772677139808695 / 340282366920938463463374607431768211456

def baselineLower : Rat :=
  127263766859979925728141246211069006267 /
    27562871720596015540533343201973225127936

def baselineUpper : Rat :=
  10605313904998327144011770517589083871 /
    2296905976716334628377778600164435427328

-- Negative coefficient -13 requires the opposing interval endpoint.
def propagatedLower : Rat := (1 - 13 * exp3Upper + 172 * exp9Lower) / 81
def propagatedUpper : Rat := (1 - 13 * exp3Lower + 172 * exp9Upper) / 81

theorem exp3_endpoints_ordered : exp3Lower ≤ exp3Upper := by decide +kernel
theorem exp9_endpoints_ordered : exp9Lower ≤ exp9Upper := by decide +kernel

theorem propagated_lower_matches : propagatedLower = baselineLower := by
  decide +kernel

theorem propagated_upper_matches : propagatedUpper = baselineUpper := by
  decide +kernel

theorem propagated_endpoints_ordered : propagatedLower ≤ propagatedUpper := by
  decide +kernel

theorem propagated_upper_meets_cap : propagatedUpper ≤ (1 / 200 : Rat) := by
  decide +kernel

theorem propagated_lower_exceeds_rejected : (1 / 300 : Rat) < propagatedLower := by
  decide +kernel

#print axioms propagated_lower_matches
#print axioms propagated_upper_matches

end E2ATailEndpointAlgebra
