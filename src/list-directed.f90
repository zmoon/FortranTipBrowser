program list_directed
   use iso_fortran_env, only: real64
   implicit none

   integer, parameter :: x = 1
   real(kind=real64), parameter :: y = acos(-1.0), &
      z = 6.62607015d-34

   print *, x, y, z
   print '(*(g0, :, x))', x, y, z
   print '(*(g0.4, :, ","))', x, y, z
   print '(/, i0, /, "and", /, f0.5, /, "and", /, es0.3)', x, y, z

end program list_directed
