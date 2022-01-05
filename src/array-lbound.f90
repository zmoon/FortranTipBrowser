integer :: v(-1:1) = [1, -2, 3]

print *, lbound(v), ubound(v), size(v)  ! -1 1 3
print *, sum(v)  ! 2
print *, sum(v,mask=v>0)  ! 4 -- sum excludes -2

end
