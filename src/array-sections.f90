integer, parameter :: v(3) = [10, 20, 30]

print *, v(1:2)  ! output: 10 20
print *, v(:2)   ! 10 20
print *, v(2:3)  ! 20 30
print *, v(2:)   ! 20 30
print *, v(::2)  ! 10 30 -- stride of 2

end
