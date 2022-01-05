character (len=5) :: v = "one"

print *, "'" // v // "'"  ! 'one  '
print *, "'" // trim(v) // "'"  ! 'one'
print *, len(v), len_trim(v)  ! 5 3

end
