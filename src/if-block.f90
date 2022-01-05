integer :: i

do i = -1, 1
   print *, i
   if (i < 0) then
      print *, "negative"
   else if (i == 0) then
      print *, "zero"
   else
      print *, "positive"
   end if
end do

end
