integer :: v(2,3) ! 2x3 matrix

v(1,:) = [1, 2, 3]
v(2,:) = 10*v(1,:)  ! [10, 20, 30]

print *, sum(v)  ! all elements: 66
print *, sum(v,dim=1)  ! sum each row: 6 60
print *, sum(v,dim=2)  ! sum each col: 11 22 33

end
