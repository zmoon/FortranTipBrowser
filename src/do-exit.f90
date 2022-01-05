implicit none
integer :: i,ssq

ssq = 0
i = 0

do
   i = i+1
   ssq = ssq + i**2
   if (ssq > 100) exit
end do  
print *, "sum of squares from 1 to ", i, " is", ssq

end
