character(len=5) :: w(3)

! This is invalid and would raise a compilation error:
! w = ["one", "four", "seven"]

w = ["one  ", "four ", "seven"]  ! same as below
w = [character(5) :: "one", "four", "seven"] 

print *, w

end
