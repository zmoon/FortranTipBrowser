program factorial
   use, intrinsic :: iso_fortran_env, only: wp => real64

   integer, parameter :: n(*) = [0, 1, 5, 11, 170]
   integer            :: j

   do j = 1, size(n)
      print '(*(g0,1x))', 'factorial of', n(j), ' is ', &
         product([(real(i, kind=wp), i=1, n(j))]), &
         ' or ', &
         gamma(real(n(j) + 1, kind=wp))
   end do
   print *, huge(0._wp)

end program factorial
