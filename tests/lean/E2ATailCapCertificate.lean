import Init.Data.Rat.Lemmas

namespace E2ATailCapCertificate

-- Exact fractions replayed by the Python tail-mass verifier at 128 bits.
def lower : Rat := 127263766859979925728141246211069006267 / 27562871720596015540533343201973225127936
def upper : Rat := 10605313904998327144011770517589083871 / 2296905976716334628377778600164435427328
def acceptedCap : Rat := 1 / 200
def rejectedCap : Rat := 1 / 300

theorem ordered_enclosure : lower ≤ upper := by decide +kernel
theorem upper_meets_cap : upper ≤ acceptedCap := by decide +kernel
theorem lower_exceeds_cap : rejectedCap < lower := by decide +kernel

-- These implications operate on a rational value given the respective enclosure bound.
theorem accepted_given_enclosure (mass : Rat) (h : mass ≤ upper) : mass ≤ acceptedCap :=
  Rat.le_trans h upper_meets_cap

theorem rejected_given_enclosure (mass : Rat) (h : lower ≤ mass) : rejectedCap < mass :=
  Rat.not_le.mp (fun mass_le_cap => Rat.not_le.mpr lower_exceeds_cap (Rat.le_trans h mass_le_cap))

#print axioms ordered_enclosure
#print axioms accepted_given_enclosure
#print axioms rejected_given_enclosure

end E2ATailCapCertificate
