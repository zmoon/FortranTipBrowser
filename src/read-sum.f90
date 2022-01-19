program sum_int
   implicit none
   integer :: i, ierr, isum

   isum = 0
   do
      print *, "enter an integer, 0 to stop"
      read (*, *, iostat=ierr) i
      if (ierr /= 0) then
         print *, "invalid input"
         cycle  ! return to beginning of loop
      end if
      if (i == 0) exit
      isum = isum + i
   end do
   print *, "sum is", isum

end program sum_int
