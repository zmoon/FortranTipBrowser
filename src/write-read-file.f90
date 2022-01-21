program read_write
   implicit none
   
   integer, parameter :: max_read = 10**6
   integer :: i, ierr, iunit, nread
   integer, allocatable :: vec_write(:), vec_read(:)
   character(len=*), parameter :: data_file = "temp.txt"
   
   vec_write = [1, 4, 9]

   ! Connect file to unit `iunit` for writing
   print *, "initial (unset) iunit =", iunit
   open (newunit=iunit, file=data_file, action="write", status="replace")
   print *, "iunit for writing =", iunit
   do i = 1, size(vec_write)
      write (iunit, *) vec_write(i)  ! Write one element of `vec_write` per line
   end do
   close (iunit)  ! Close the connection to the file

   ! Connect file to unit `iunit` for reading
   open (newunit=iunit, file=data_file, action="read", status="old")
   print *, "iunit for reading =", iunit
   allocate (vec_read(max_read))
   nread = max_read
   do i = 1, max_read
      read (iunit, *, iostat=ierr) vec_read(i)  ! Read one element of `vec_read` per line
      if (ierr /= 0) then  ! Reached end of file
         nread = i - 1
         exit
      end if
   end do
   print *, "# read =", nread
   print *, "data read =", vec_read(:nread)

end program read_write
