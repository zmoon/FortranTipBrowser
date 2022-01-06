integer :: v(2,3)  ! 2x3 matrix

v(1,:) = [1, 2, 3]
v(2,:) = 10*v(1,:)  ! [10, 20, 30]

print *, v  ! elements in column-major order

print *, sum(v)         ! sum all elements: 66
print *, sum(v, dim=1)  ! sum each col (along row dim): 11 22 33
print *, sum(v, dim=2)  ! sum each row (along col dim): 6 60

end
