program alloc_stat
   implicit none

   real, allocatable :: x(:)
   integer :: ierr

   ! Initial allocation
   allocate (x(5))
   print *, allocated(x)  ! Confirm

   ! Trying to allocate again will error
   allocate (x(42), stat=ierr)
   if (ierr /= 0) then
      print *, "error", ierr
   else
      print *, "it worked"
   end if

end program alloc_stat
