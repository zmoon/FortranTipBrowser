program column_major
   use iso_fortran_env, only: wp => real64, int64

   integer, parameter :: m = 10000, n = m
   integer :: array(m, n)
   integer :: i, j, tot
   integer(int64) :: irate, tic, toc

   call system_clock(count_rate=irate)  ! # of clock ticks per second
   array = 0

   ! FASTER: Looping consecutively through columns
   call system_clock(count=tic)
   tot = 0
   do j = 1, size(array, dim=2)
      do i = 1, size(array, dim=1)
         ! Do something with array(i, j)
         tot = tot + array(i, j)
      end do
   end do
   call system_clock(count=toc)
   print "(g12.3)", (toc - tic) / real(irate, wp)

   ! SLOWER: Looping consecutively through rows
   call system_clock(count=tic)
   tot = 0
   do i = 1, size(array, dim=1)
      do j = 1, size(array, dim=2)
         ! Do something with array(i, j)
         tot = tot + array(i, j)
      end do
   end do
   call system_clock(count=toc)
   print "(g12.3)", (toc - tic) / real(irate, wp)

end program
