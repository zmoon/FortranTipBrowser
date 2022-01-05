module kind_mod
    use iso_fortran_env, only: real32, real64, real128  ! constants from intrinsic module
    implicit none

    integer, parameter :: wp = real64  ! or `real32`, `real128`

end module kind_mod

module area_mod
    use kind_mod, only: wp

    ! We can use a literal:
    ! real(kind=wp), parameter :: pi = 3.141592653589793238462643383279_wp
    ! Accurate up to 3.141592653589793 (15 places after decimal) with `real64`
    
    ! Or calculate:
    real(kind=wp), parameter :: pi = acos(-1.0_wp)  ! same result

contains

    pure elemental function area_circle(radius) result(area)
        real(kind=wp), intent(in) :: radius
        real(kind=wp) :: area
        area = pi*radius**2
    end function area_circle

end module area_mod

program xkind
    use kind_mod, only: wp
    use area_mod, only: area_circle
    implicit none

    real(kind=wp), parameter :: radius = 10.0_wp

    print *, area_circle(radius)

end program xkind
