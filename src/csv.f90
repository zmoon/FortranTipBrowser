program csv
   implicit none

   integer :: x, y
   integer, parameter :: n = 3
   character(len=*), parameter :: fmt = "(*(g0.5, :, ','))"

   print fmt, "x", "y", "r"
   do x = 1, n
      do y = 1, n
         print fmt, x, y, norm2(real([x, y]))
      end do
   end do

end program csv
