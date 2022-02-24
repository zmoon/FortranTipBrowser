module date_mod
   implicit none

   interface operator(+)
      module procedure add
   end interface
   interface operator(>)
      module procedure greater
   end interface
   type :: ym
      integer :: year, month
   end type ym

contains

   elemental function str(date) result(text)
      type(ym), intent(in) :: date
      character(len=7)     :: text
      write (text, "(i4.4,'-',i2.2)") date%year, date%month
   end function str

   elemental function add(date, n) result(new_date)
      type(ym), intent(in) :: date
      integer, intent(in)  :: n
      type(ym)             :: new_date
      new_date = int_to_ym(int(date) + n)
   end function add

   elemental function int(date) result(idate)
      type(ym), intent(in) :: date
      integer              :: idate
      idate = date%year*12 + date%month
   end function int

   elemental function int_to_ym(idate) result(date)
      integer, intent(in) :: idate
      type(ym)            :: date
      date%year = idate/12
      date%month = idate - date%year*12
      if (date%month == 0) then
         date%month = 12
         date%year = date%year - 1
      end if
   end function int_to_ym

   elemental function greater(date_1, date_2) result(tf)
      type(ym), intent(in) :: date_1, date_2
      logical              :: tf
      tf = int(date_1) > int(date_2)
   end function greater

end module date_mod


program xdate
   use date_mod, only: ym, str, operator(+), operator(>)
   implicit none

   type(ym), allocatable :: dates(:)
   integer :: ta(3)

   ! Set array of type `ym`
   dates = [ym(2021, 11), ym(2021, 12), ym(2022, 1)]

   print "(a10,':',*(1x,a))", "dates", str(dates)
   print "(a10,':',*(i8))", "months", dates%month
   ! Note usage of `+` and `>` operators in the following:
   print "(a10,':',*(1x,a))", "dates+1", str(dates + 1)
   print *, "dates > dates(2)", dates > dates(2)

   ! Current date using `idate`
   print *
   call idate(ta)
   print "(i4.4,'-',i2.2,'-',i2.2)", ta(3:1:-1)

end program xdate
