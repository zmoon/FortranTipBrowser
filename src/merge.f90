integer :: i

do i = -1, 1
   print *, i
   ! Note: "zero" padded to have same length as "negative"
   print *, merge("negative", merge("zero    ", &  
                  "positive", i == 0 ), i < 0)
end do

end
