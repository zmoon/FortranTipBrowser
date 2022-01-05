integer, allocatable :: u(:)

u = [4,9]

associate (v => u)
v = v - 2
print *, v  ! 2 7
print *, u  ! 2 7

associate (w => [4, 9])
print *, w

! The following is illegal since `w` is set to a constant expression;
! it will raise a compilation error:
! w = w - 2  

! Need one for each of the `associate`s above
end associate
end associate

end
