program cf_numpy
   implicit none

   integer, parameter :: m = 2, n = 3
   integer :: a(m, n)
   character(len=*), parameter :: fmt = "(x, a, ':', x, *(g0, x))"

   print *, "Before setting:"
   call print11(a)

   a = 1  ! Set all elements

   print *, "After setting:"
   call print11(a)

   print fmt, "size", size(a)
   print fmt, "shape", shape(a)

   a(1,1) = 100
   
   print fmt, "maxval", maxval(a)
   print fmt, "minval", minval(a)

   print fmt, "sum", sum(a)
   print fmt, "sum, dim=1", sum(a, dim=1)
   print fmt, "sum, dim=2", sum(a, dim=2)

contains

   subroutine print11(mat)
      integer, intent(in) :: mat(:,:)

      print "(3x, 'row 1:', x, *(i0, x))", mat(1, :)
      print "(3x, 'col 1:', x, *(i0, x))", mat(:, 1)

   end subroutine print11

end program cf_numpy
