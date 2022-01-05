print *, area(3., 4.)  ! 12

contains

real pure function area(length, width)
   real, intent(in) :: length, width
   area = length*width
end function area

end
