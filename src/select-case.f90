program select_case
   implicit none
   integer :: i
   character(len=6) :: rating

   do i = 0, 5
      select case (i)
         case (1:2)
            rating = "bad"
         case (3)
            rating = "medium"
         case (4:)
            rating = "good"
         case default
            rating = "???"
      end select
      print *, i, trim(rating)
   end do

end program select_case
