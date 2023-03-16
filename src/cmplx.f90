program test_cmplx
   implicit none

   integer, parameter :: dp = kind(0.0d0)

   complex, parameter :: c1 = (1.0, 1.0)
   complex, parameter :: c2 = (1.0d0, 1.0d0)
   complex(kind=dp), parameter :: c3 = (1.0d0, 1.0d0)

   ! Parameter
   print *, kind(c1)  ! 4
   print *, kind(c2)  ! 4
   print *, kind(c3)  ! 8
   print *

   ! Inline literal
   print *, kind((1.0, 1.0))      ! 4
   print *, kind((1.0, 1.0d0))    ! 8
   print *, kind((1.0d0, 1.0))    ! 8
   print *, kind((1.0d0, 1.0d0))  ! 8
   print *

   ! Calling `cmplx`
   print *, kind(cmplx(1.0d0, 1.0d0))  ! 4 -- likely unintended!
   print *, kind(cmplx(1.0d0, 1.0d0, kind=dp))  ! 8
   print *

   ! Same if passing real component only
   print *, kind(cmplx(1.0d0))  ! 4
   print *, kind(cmplx(1.0d0, kind=dp))  ! 8
   print *

end program test_cmplx
