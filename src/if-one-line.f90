integer :: i

do i = -1, 1
   if (i /= 0) print *, i, 1/i  ! one-line if equivalent to below
   if (i /= 0) then
      print *, i, 1/i
   end if
end do

end
