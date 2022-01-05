implicit none

integer :: i, ssq

ssq = 0
do i = 1, 5
   ssq = ssq + i**2
end do
print *, "sum of squares is ", ssq

end
