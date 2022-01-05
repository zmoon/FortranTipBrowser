integer, allocatable :: v(:)

v = [4, 9]

deallocate(v)  ! necessary for line below to work
allocate(v, source=[4, 9])  ! same result as above

end
