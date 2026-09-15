import Std

/- C4 accounting only. No quantum/entropy assumptions are formalized here. -/

namespace ClosedMemory

theorem transaction_volume (input output c d work : Nat)
    (capital : input = output + c) :
    input + d + work = output + (c + d) + work := by
  omega

theorem parked_step (unused parked c d : Nat)
    (available : c + d <= unused) :
    (unused - (c + d)) + (parked + (c + d)) = unused + parked := by
  omega

theorem pool_suffices (pureStock mixedStock c d : Nat)
    (pureBudget : d <= pureStock)
    (totalBudget : 2*c + d <= pureStock + 2*mixedStock) :
    d + 2*(c-mixedStock) <= pureStock := by
  omega

theorem pool_necessary (pureStock mixedStock c d : Nat)
    (fits : d + 2*(c-mixedStock) <= pureStock) :
    d <= pureStock /\ 2*c + d <= pureStock + 2*mixedStock := by
  omega

theorem workspace_relabel (cells compressed residue : Nat) :
    compressed + residue + (cells-compressed) =
    cells + residue + (compressed-cells) := by
  omega

theorem finite_error_step (previous accumulated localError next : Nat)
    (oldBound : previous <= accumulated)
    (stepBound : next <= previous + localError) :
    next <= accumulated + localError := by
  omega

#print axioms transaction_volume
#print axioms parked_step
#print axioms pool_suffices
#print axioms pool_necessary
#print axioms workspace_relabel
#print axioms finite_error_step

end ClosedMemory
