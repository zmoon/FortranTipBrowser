! Define and call a subroutine
program optional_arg
   implicit none
   real :: x(1000000), xmean, xsd

   call random_seed()
   call random_number(x)  ! generate uniform random deviates on (0, 1]
   call stats(x, xmean, xsd)

   print *, xmean, xsd

contains

   pure subroutine stats(x, xmean, xsd)
      real, intent(in)  :: x(:)  ! data for which stats computed
      real, intent(out) :: xmean ! mean of x(:)
      real, intent(out) :: xsd   ! standard deviation of x(:)
      real, parameter   :: bad = -999.0
      integer           :: n
      n = size(x)

      ! Set outputs to bad value if there is insufficient data
      xmean = bad
      xsd = bad
      if (n < 1) return
    
      ! We have at least one value, enough to compute mean
      xmean = sum(x)/size(x)
      if (n < 2) return

      ! If we get to here, we have at least two values,
      ! enough data to compute standard deviation.
      xsd = sqrt(sum((x - xmean)**2)/(n - 1))
   end subroutine stats

end program optional_arg
