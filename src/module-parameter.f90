module constants_mod
   implicit none
   private
   public :: pi

   real, parameter :: pi = 3.14159

end module constants_mod

module m
   use constants_mod, only: pi
   implicit none
   private
   public :: area_circle

contains

   real pure elemental function area_circle(radius) result(area)
      real, intent(in) :: radius
      area = pi*radius**2
   end function area_circle

end module m

program main
   use constants_mod, only: pi
   use m, only: area_circle
   implicit none

   real, parameter :: radius = 10.0

   print *, "circumference, area =", 2*pi*radius, area_circle(radius)

end program main
