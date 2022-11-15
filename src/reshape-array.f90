program test_reshape
   implicit none

   integer, allocatable :: v(:), m(:, :)

   v = [1, 2, 3, 4, 5, 6]

   print *, "Fill column-wise (default):"
   m = reshape(source=v, shape=[2, 3])
   print *, m(1, :)  ! 1 3 5
   print *, m(2, :)  ! 2 4 6

   print *, "Fill row-wise:"
   m = reshape(source=v, shape=[2, 3], order=[2, 1])
   print *, m(1, :)  ! 1 2 3
   print *, m(2, :)  ! 4 5 6

   print *, "Pad with [1, -1] after exhausting source [0, 0]:"
   m = reshape(source=[0, 0], shape=[2, 3], order=[2, 1], pad=[1, -1])
   print *, m(1, :)  !  0 0  1
   print *, m(2, :)  ! -1 1 -1

   print *, "Repeat row-wise example supplying `pad` (unused):"
   ! Here `pad` is unused because `size(source)` equals `product(shape)`
   m = reshape(source=v, shape=[2, 3], order=[2, 1], pad=[1, -1])
   print *, m(1, :)  !  1 2 3
   print *, m(2, :)  !  4 5 6

end program test_reshape
