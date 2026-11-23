import E2ATailEndpointAlgebra

namespace E2ALandauTail

def taylorTerm (y : Rat) : Nat → Rat
  | 0 => 1
  | n + 1 => taylorTerm y n * y / (n + 1 : Nat)

def taylorSum (y : Rat) : Nat → Rat
  | 0 => 1
  | n + 1 => taylorSum y n + taylorTerm y (n + 1)

def geometricRemainder (y : Rat) (n : Nat) : Rat :=
  taylorTerm y (n + 1) / (1 - y / (n + 2 : Nat))

-- The pinned Mathlib exponential theorem uses this slightly looser remainder.
def libraryRemainder (y : Rat) (n : Nat) : Rat :=
  taylorTerm y (n + 1) * (((n + 1 : Nat) : Rat) + 1) / ((n + 1 : Nat) : Rat)

def small3Lower : Rat := 9133129133672633160701668318815661493442582174397409844093 / 2^192
def small3Upper : Rat := 9133129133672633160701668318815661493442582174397409844094 / 2^192
def small9Lower : Rat := 8315808708030787239768431532530479343267966789737216480290 / 2^192
def small9Upper : Rat := 8315808708030787239768431532530479343267966789737216480291 / 2^192

abbrev exp3Lower : Rat := E2ATailEndpointAlgebra.exp3Lower
abbrev exp3Upper : Rat := E2ATailEndpointAlgebra.exp3Upper
abbrev exp9Lower : Rat := E2ATailEndpointAlgebra.exp9Lower
abbrev exp9Upper : Rat := E2ATailEndpointAlgebra.exp9Upper

set_option maxRecDepth 4096 in
set_option maxHeartbeats 1000000 in
theorem small3_arithmetic :
    0 < small3Lower ∧ small3Lower ≤ taylorSum (3 / 8) 37 ∧
      taylorSum (3 / 8) 37 + geometricRemainder (3 / 8) 37 ≤ small3Upper := by
  decide +kernel

set_option maxRecDepth 4096 in
set_option maxHeartbeats 1000000 in
theorem small9_arithmetic :
    0 < small9Lower ∧ small9Lower ≤ taylorSum (9 / 32) 34 ∧
      taylorSum (9 / 32) 34 + geometricRemainder (9 / 32) 34 ≤ small9Upper := by
  decide +kernel

set_option maxRecDepth 4096 in
set_option maxHeartbeats 1000000 in
theorem small3_library_arithmetic :
    taylorSum (3 / 8) 37 + libraryRemainder (3 / 8) 37 ≤ small3Upper := by
  decide +kernel

set_option maxRecDepth 4096 in
set_option maxHeartbeats 1000000 in
theorem small9_library_arithmetic :
    taylorSum (9 / 32) 34 + libraryRemainder (9 / 32) 34 ≤ small9Upper := by
  decide +kernel

theorem reciprocal3_arithmetic :
    exp3Lower ≤ 1 / small3Upper^8 ∧ 1 / small3Lower^8 ≤ exp3Upper := by
  decide +kernel

theorem reciprocal9_arithmetic :
    exp9Lower ≤ 1 / small9Upper^32 ∧ 1 / small9Lower^32 ≤ exp9Upper := by
  decide +kernel

abbrev tailLower : Rat := E2ATailEndpointAlgebra.propagatedLower
abbrev tailUpper : Rat := E2ATailEndpointAlgebra.propagatedUpper

theorem exact_interval :
    tailLower = 127263766859979925728141246211069006267 / 27562871720596015540533343201973225127936 ∧
    tailUpper = 10605313904998327144011770517589083871 / 2296905976716334628377778600164435427328 :=
  ⟨E2ATailEndpointAlgebra.propagated_lower_matches, E2ATailEndpointAlgebra.propagated_upper_matches⟩

theorem cap_comparisons : (1 / 300 : Rat) < tailLower ∧ tailUpper ≤ 1 / 200 :=
  ⟨E2ATailEndpointAlgebra.propagated_lower_exceeds_rejected,
    E2ATailEndpointAlgebra.propagated_upper_meets_cap⟩

#print axioms small3_arithmetic
#print axioms small9_arithmetic
#print axioms small3_library_arithmetic
#print axioms small9_library_arithmetic
#print axioms reciprocal3_arithmetic
#print axioms reciprocal9_arithmetic
#print axioms exact_interval
#print axioms cap_comparisons

end E2ALandauTail
