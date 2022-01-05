! Demonstrate an `elemental recursive` function
module m
   implicit none

contains

   elemental recursive function factorial(n) result(nfac)
      integer, intent(in) :: n
      integer :: nfac

      if (n < 0) then
         nfac = -1
         return
      else if (n < 2) then
         nfac = 1
         return
      else
         nfac = n*factorial(n - 1)
      end if
   end function factorial

end module m

program xfactorial
   use m, only: factorial
   implicit none

   print *, factorial([-1, 0, 1, 4])  ! -1 1 1 24

end program xfactorial
