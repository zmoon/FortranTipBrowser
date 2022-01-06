program intent_in_out
   implicit none
   real :: x(3)

   x = [1., 4., 5.]
   call normalize(x)
   print *, x  ! 0.1 0.4 0.5

contains

   subroutine normalize(x)
      ! Scale `x` so that `sum(x)` = 1.
      real, intent(in out) :: x(:)
      real                 :: xsum
      xsum = sum(x)
      if (xsum /= 0) x = x/xsum
   end subroutine normalize

end program intent_in_out
