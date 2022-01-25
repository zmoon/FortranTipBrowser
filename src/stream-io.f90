program stream_io
   use iso_fortran_env, only: wp => real64, int64
   implicit none

   integer, parameter  :: n = 10**6
   real(kind=wp)       :: x(n), xchk(n)
   integer(kind=int64) :: iunit, irate, times(6)

   call system_clock(count_rate=irate)  ! # of clock ticks per second
   print *, "n =", n
   print *, "irate =", irate
   call random_number(x)
   call system_clock(count=times(1))

   ! Use formatted write and read
   open (newunit=iunit, file="temp.txt", action="write", status="replace")
   write (iunit, "(f0.16)") x
   close (iunit)
   call system_clock(count=times(2))
   open (newunit=iunit, file="temp.txt", action="read", status="old")
   read (iunit, *) xchk  ! List-directed read with `*` gets data from as many lines as are needed
   call system_clock(count=times(3))
   print *, maxval(x - xchk), minval(x), maxval(x), minval(xchk), maxval(xchk) ! check
   call system_clock(count=times(4))

   ! Use unformatted stream write and read
   open (newunit=iunit, file="temp.bin", action="write", status="replace", &
         form="unformatted", access="stream")
   write (iunit) x  ! Note no format supplied for unformatted I/O
   close (iunit)
   call system_clock(count=times(5))
   open (newunit=iunit, file="temp.bin", action="read", status="old", &
         form="unformatted", access="stream")
   read (iunit) xchk
   call system_clock(count=times(6))
   print *, maxval(x - xchk), minval(x), maxval(x), minval(xchk), maxval(xchk)  ! check

   ! Count differences divided by `count_rate` gives seconds elapsed
   print "(/, *(a12))", "formatted", "formatted", "unformatted", "unformatted"
   print "(*(a12))", "write", "read", "write", "read"
   print "(*(g12.3))", [times(2:3) - times(1:2), times(5:6) - times(4:5)] / real(irate, wp)

   ! Enhancement factors
   print "(/, *(a12))", "enhancement", "enhancement"
   print "(*(a12))", "write", "read"
   print "(*(g12.3))", real(times(2) - times(1), wp) / (times(5) - times(4)), &
                       real(times(3) - times(2), wp) / (times(6) - times(5))

end program stream_io
