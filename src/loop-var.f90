integer :: i

do i = 1, 3
  if (i > 1) exit
end do
print *, i  ! 2

do i = 1, 3  ! stride of 1
  continue  ! placeholder
end do
print *, i  ! 4

do i = 1, 3, 2  ! stride of 2
  continue
end do
print *, i  ! 5

end
