module m

contains

integer function area(length, width)
   integer, intent(in) :: length, width
   area = length*width
end

end module m

program main
  use m
  
  print*,area(3,4) ! 12

end program main
