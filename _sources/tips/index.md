---
sd_hide_title: true
...

# Tips index

```{toctree}
:hidden:

001
002
003
004
005
006
007
008
009
010
011
012
013
014
015
016
017
018
019
020
021
022
023
024
025
026
027
028
029
030
031
032
033
034
035
036
037
038
039
040
041
042
043
044
045
046
047
048
049
050
051
052
053
054
055
056
057
058
059
060
061
062
063
064
065
066
067
068
069
070
071
072
073
074
075
076
077
078
079
080
081
082
083
084
085
086
087
088
089
090
091
092
093
094
095
096
097
098
099
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
```

(by-topic)=
## By topic

*According to [the FortranTip topics page](https://github.com/Beliavsky/FortranTip/blob/main/topics.md).*
*Note that these [are exclusive categories](https://github.com/zmoon/FortranTipBrowser/issues/5#issuecomment-1060020993).*

(allocation)=
### Allocation

- [012.](./012.md) Fortran has allocation-on-assignment
- [040.](./040.md) If allocation errors must be handled, use `allocatable` rather than automatic arrays in procedures
- [180.](./180.md) ALLOCATE with SOURCE or MOLD to set values or SHAPE.
- [182.](./182.md) ALLOCATE has an optional ERRMSG specifier.
- [183.](./183.md) If unsure, test whether a variable is ALLOCATED before using DEALLOCATE.
- [184.](./184.md) Use MOVE_ALLOC to resize an array.
- [185.](./185.md) MOVE_ALLOC may be faster than RESHAPE or allocation on asignment to resize an array.

(array-arguments)=
### Array arguments

- [122.](./122.md) Array lower bounds are not preserved when passed as assumed shape argument.
- [123.](./123.md) Bounds of a derived type array component are preserved when passed to procedure.
- [124.](./124.md) Bounds of an allocatable array are preserved when passed to an allocatable, intent(in) or intent(in out) argument.
- [136.](./136.md) Check that assumed-shape array arguments have consistent dimensions.
- [226.](./226.md) Wrap a procedure with explicit shape array arguments in a procedure with an assumed shape arguments for safety.
- [227.](./227.md) Sequence association effectively lets you pass a pointer to an array element.
- [228.](./228.md) With sequence association, the shapes of the actual and dummy arguments need not match.

(arrays)=
### Arrays

- [008.](./008.md) Array intrinsic functions: `sum`, `minval`, `maxval`, `minloc`, `findloc`
- [009.](./009.md) Fortran array sections contain both endpoints
- [010.](./010.md) Fortran arrays can have any lower bound (the default is 1)
- [011.](./011.md) `sum` and other array functions have an optional `dim`ension argument
- [021.](./021.md) `pack` selects elements
- [042.](./042.md) Zero-size array constructor
- [043.](./043.md) Comparing Fortran and NumPy syntax
- [047.](./047.md) `reshape` with the optional `order` and `pad` arguments
- [049.](./049.md) Fortran is column-major
- [053.](./053.md) Use ALL(A==B) to test for array equality
- [060.](./060.md) Many compilers evaluate ALL(x==y) efficiently with short-circuiting
- [073.](./073.md) Use parameters to dimension fixed-size arrays to make a code easier to change
- [084.](./084.md) DIMENSION can be used to declare several arrays of the same SHAPE
- [095.](./095.md) Array constructor with [] was introduced in Fortran 2003. Still valid is (//)
- [108.](./108.md) Vector subscript can be used for non-contiguous array sections.
- [109.](./109.md) Setting the values of an array section
- [116.](./116.md) Concatenate arrays and scalars in an array constructor []
- [117.](./117.md) spread(source, dim, ncopies) copies a SOURCE array NCOPIES times along dimension DIM.
- [121.](./121.md) How to reverse an array or character string
- [229.](./229.md) Use the optional KIND argument of SIZE, MINLOC, FINDLOC etc. for large arrays.

(associate)=
### Associate

- [019.](./019.md) `associate` creates an alias for expressions or variables
- [141.](./141.md) Pointer assignment and ASSOCIATE can create shallow copies.
- [142.](./142.md) ASSOCIATE is preferred over POINTER to create an alias because POINTER can inhibit optimization.
- [143.](./143.md) ASSOCIATE statement can set several independent variables.
- [144.](./144.md) A variable ASSOCIATEd to an ALLOCATABLE variable is not ALLOCATABLE.
- [146.](./146.md) Bounds of associate-name for whole array or array section selector
- [181.](./181.md) ASSOCIATE to an array-valued expression allocates an array.

(basics)=
### Basics

- [001.](./001.md) Hello World
- [006.](./006.md) `**` is the exponentiation operator
- [007.](./007.md) Integer division truncates
- [054.](./054.md) Consider using a tolerance to compare floats
- [064.](./064.md) Case insensitivity
- [077.](./077.md) Use integer powers when possible.
- [078.](./078.md) Parenthesize a variable to copy it "on the fly".
- [135.](./135.md) ERROR STOP vs. STOP.
- [139.](./139.md) BLOCK construct allows declarations after executable statements.

(character-variables)=
### Character variables

- [016.](./016.md) An array of character variables has elements of the same `len`gth
- [017.](./017.md) Character variables are padded with spaces at the end if necessary
- [051.](./051.md) Doubled delimiter in a string is regarded as a single character of the constant
- [059.](./059.md) LEN of a character variable may be deferred in Fortran 2003 on
- [066.](./066.md) Do case-insensitive string comparisons by converting to lower case
- [079.](./079.md) Substrings of character variable arrays
- [080.](./080.md) Intrinsic character functions
- [081.](./081.md) Syntax for character array without manual padding
- [118.](./118.md) Convert from strings to numbers and the reverse using internal READ and WRITE.
- [119.](./119.md) Internal write to character variable too small to hold output causes run-time error.
- [120.](./120.md) Character variables can be compared like numerical variables.
- [169.](./169.md) print*,char(7) causes the program to beep.
- [170.](./170.md) Use an implied do loop with TRIM to print an array of character variables without trailing blanks.

(compiling)=
### Compiling

- [197.](./197.md) Create an executable in one step by compiling all source files or by compiling source files with -c and linking the object files.
- [198.](./198.md) Compilation can fail if there is no main program or if a USEd module has not been compiled.
- [199.](./199.md) Fortran Package Manger simplifies building programs.
- [200.](./200.md) Fortran-lang has a section on Building Programs, and F18 has a compiler options comparison.
- [201.](./201.md) Compiler Explorer shows the assembly code generated by many Fortran compilers.
- [202.](./202.md) Compilers may accept extensions by default but have options to flag non-standard code.
- [203.](./203.md) Use ifort -fast or gfortran -O3 -march=native for speed.
- [204.](./204.md) When is the -ffast-math option safe?
- [207.](./207.md) Use compiler options to catch the use of uninitialized variables.

(conditionals)=
### Conditionals

- [014.](./014.md) `if`-`else if`-`end if` block
- [015.](./015.md) `merge(x, y, cond)`
- [018.](./018.md) Fortran has a one-line `if`
- [035.](./035.md) `select case` for conditional execution
- [055.](./055.md) ANY and ALL may not be the most efficient methods to compare arrays.
- [056.](./056.md) Standards committee has approved conditional expressions

(data-types)=
### Data types

- [002.](./002.md) Intrinsic data types
- [033.](./033.md) Declare floating point variables with `kind`s
- [034.](./034.md) Replace non-standard `REAL*8` declaration with `real(kind=real64)`
- [048.](./048.md) `cmplx` should be used with a `kind` argument
- [057.](./057.md) Use .true. and .false. for Booleans, not 1 and 0
- [070.](./070.md) Real and integer KIND constants from iso_fortran_env; HUGE() and TINY()
- [071.](./071.md) KindFinder code finds all KIND Values implemented by a compiler
- [072.](./072.md) Fortran 2008 introduced z%re and z%im as alternatives to real(z) and aimag(z)
- [075.](./075.md) KIND numbers of types are not portable across compilers and should not be used directly.
- [076.](./076.md) Use d0 or \_kind to make a constant double precision.
- [130.](./130.md) storage_size(A) returns the storage size of argument A in bits.
- [195.](./195.md) TRANSFER can be used to store one type in another type.
- [196.](./196.md) NOT, IAND, IOR, and IEOR perform logical operations on the bit representations of integers.
- [205.](./205.md) Use IANY instead of nested IOR, IALL instead of nested IAND.
- [206.](./206.md) B, O, Z edit descriptors can be used to print integers as binary, octal, or hexadecimal.
- [224.](./224.md) Ways of declaring character variables

(derived-types)=
### Derived types

- [045.](./045.md) Derived type definition, initialization, and operator overloading
- [050.](./050.md) Store data as an array of derived types or a derived type with array components?
- [126.](./126.md) A derived type can be used where a scalar is needed.
- [127.](./127.md) A derived type can have derived type components.
- [128.](./128.md) A derived type component can have a default value.
- [129.](./129.md) A derived type can have PRIVATE components.
- [186.](./186.md) Deallocating a derived type deallocates its allocatable components.
- [191.](./191.md) Derived type array sections are allowed before or after the % component selector, but not in both places.
- [192.](./192.md) Implied do loop can access arbitrary derived type array sections.
- [194.](./194.md) Use PACK to select records from an array of derived types.

(environment-variables)=
### Environment variables

- [111.](./111.md) Execute_command_line() to pass a command to the shell.
- [112.](./112.md) Execute_command_line() can call gnuplot to display a plot during a run.
- [113.](./113.md) Document results with compiler_version(), compiler_options(), and other intrinsics.
- [114.](./114.md) Demonstrate subroutine get_environment_variable(name,value) of Fortran 2003.
- [115.](./115.md) get_command() and get_command_argument() get command line arguments.

(floating-point-arithmetic)=
### Floating point arithmetic

- [103.](./103.md) IEEE_ARITHMETIC module has functions to test numerical conditions.
- [104.](./104.md) Call ieee_set_halting_mode() to set floating point conditions that halt program.

(fortran-resources)=
### Fortran resources

- [005.](./005.md) Fortran compilers and tutorials
- [052.](./052.md) Intel Fortran Compiler (ifx)
- [058.](./058.md) To learn about Fortran beyond F95, read the New Features articles of John Reid
- [061.](./061.md) Compiler Support for the Fortran 2008 and 2018 Standards
- [065.](./065.md) Fortran-lang suggested variable naming conventions
- [092.](./092.md) List of Fortran compilers, build tools, text editors, etc.
- [106.](./106.md) Google foo filetype:f90 or foo filetype:f to find Fortran code with foo.
- [107.](./107.md) Polyhedron suggested compiler optimization options and Fortran 95 benchmarks
- [110.](./110.md) Mistakes in Fortran 90 Programs That Might Surprise You, by Szymanski
- [125.](./125.md) Modern Fortran Reference Card and Quick Reference/Cheat Sheet.
- [138.](./138.md) Five free C C++ Fortran compiler families
- [173.](./173.md) MOOC on "Defensive programming and debugging"
- [193.](./193.md) Fortran codes are listed by topic at the fortran-lang package index and Fortran Code on GitHub
- [219.](./219.md) Use valgrind to find memory leaks in programs that use pointers.
- [223.](./223.md) List of books with Fortran code other than Fortran textbooks.

(generic-programming)=
### Generic programming

- [132.](./132.md) Unlimited polymorphic allocatable variable can be set to any type.
- [133.](./133.md) Unlimited polymorphic pointer can point to any type.
- [134.](./134.md) Assumed type arguments have no declared type.

(input-and-output)=
### Input and Output

- [036.](./036.md) Reading user input
- [037.](./037.md) Using `read` and `write` for file I/O
- [038.](./038.md) Use unformatted stream of Fortran 2003 for large-scale I/O
- [041.](./041.md) Use `g0.d` and `:` edit descriptors with infinite repeat count to write delimited (CSV, etc.) output
- [044.](./044.md) List-directed vs. explicitly formatted output
- [069.](./069.md) Advance="no" specifier of WRITE
- [091.](./091.md) Use iostat and iomsg to handle READ errors
- [150.](./150.md) Connect INPUT_UNIT and OUTPUT_UNIT to files to redirect standard input and output.
- [151.](./151.md) Unit n is connected to fort.n by default for most compilers.
- [152.](./152.md) Write to many files by creating file names with internal write.
- [153.](./153.md) Number of files open simultaneously is limited, so they should be closed when possible.
- [154.](./154.md) Use NEWUNIT in OPEN to get an unused unit number.
- [155.](./155.md) Use INQUIRE to get unit and file properties.
- [156.](./156.md) How to append to a file or delete it
- [157.](./157.md) DIRECT access file allows access to arbitrary record without looping over the previous records.
- [158.](./158.md) Specific array elements can read or written to unformatted stream file by specifying the POS.
- [159.](./159.md) Stream input/output article by Clive Page
- [160.](./160.md) Slash / terminates a record.
- [161.](./161.md) Use REWIND and BACKSPACE to change file position.
- [171.](./171.md) Error in READ statement causes all variables to become undefined.
- [172.](./172.md) Use the "(a)" format to read a line of a file into a string.
- [174.](./174.md) List-directed READ will use several lines if necessary.
- [175.](./175.md) Use an implied do loop with a dummy variable to skip fields when reading a file.
- [176.](./176.md) Because recursive I/O is prohibited, a function should use ERROR STOP msg instead of PRINT statements for error messages.
- [177.](./177.md) Read a file into a string with unformatted stream.
- [178.](./178.md) Scratch files are unnamed temporary files for I/O.
- [190.](./190.md) Serialize a derived type using unformatted stream I/O.
- [225.](./225.md) Special meanings of * and / in list-directed input

(interoperability-with-c)=
### Interoperability with C and C++

- [208.](./208.md) Fortran 2003 standardized the interoperation of Fortran and C.
- [209.](./209.md) C library functions can be called if an INTERFACE is provided.
- [210.](./210.md) Non-pointer arguments of C functions should have the VALUE attribute in the Fortran interface.
- [211.](./211.md) A simple derived type with the BIND(C) attribute interoperates with a C struct.
- [212.](./212.md) The Fortran name can differ from the C name of a function if the NAME attribute appears in BIND.
- [213.](./213.md) C++ functions can be called from Fortran if they are declared extern "C" and have C-like arguments.
- [214.](./214.md) Use the std::span container from C++ 20 to view a contiguous Fortran array with a STL-compatible interface.
- [215.](./215.md) Fortran array x(n1,n2) passed to C array x[n2][n1]
- [216.](./216.md) Common block and module variables with bind(c) can be accessed from C.
- [217.](./217.md) An allocated allocatable array can be passed to C as an explicit-shape array.
- [218.](./218.md) Use TYPE(C_PTR) and C_F_POINTER to call a C function returning a pointer.
- [220.](./220.md) Use c_funloc() to pass a Fortran function as an argument to a C function.
- [221.](./221.md) An omitted Fortran optional argument corresponds to a NULL argument of a C function.
- [222.](./222.md) C can call Fortran procedures with prototypes generated by gfortran -fc-prototypes.

(loops)=
### Loops

- [003.](./003.md) `do` loop
- [004.](./004.md) `exit`ing a `do` loop
- [020.](./020.md) Loop variable after completion
- [162.](./162.md) EXIT can be used to leave a named outer loop.
- [163.](./163.md) CYCLE skips the remaining statements in a loop.
- [164.](./164.md) Changing a loop index within a loop is invalid.
- [165.](./165.md) Number of iterations in a loop is determined at the beginning.
- [166.](./166.md) Beware of a loop to huge(i), since huge(i)+1 is out of range.
- [167.](./167.md) Invalid loop bounds were discussed at Fortran Discourse.
- [168.](./168.md) DO WHILE loop iterates as long as condition at beginning is met.

(math-intrinsic-functions)=
### Math intrinsic functions

- [046.](./046.md) Use GAMMA to compute factorials
- [062.](./062.md) MODULO vs. MOD function

(modules)=
### Modules

- [025.](./025.md) Avoid polluting the namespace by using `use`-`only`
- [026.](./026.md) Function overloading using an interface with module procedures
- [032.](./032.md) Use `parameter`s in modules to define constants
- [039.](./039.md) Name modules and the source files containing them consistently, with one module per file
- [087.](./087.md) Use the same name for analogous procedures defined in different modules using an INTERFACE
- [088.](./088.md) How to rename an imported module entity
- [089.](./089.md) Module entities are PUBLIC by default.
- [090.](./090.md) An unqualified USE foo statement imports public entities defined in foo and what foo imported.
- [096.](./096.md) PROTECTED module variables cannot be changed outside the module.
- [179.](./179.md) Place IMPLICIT NONE before CONTAINS in a module.

(parameterized-derived-types)=
### Parameterized derived types

- [187.](./187.md) Links to tutorials on parameterized derived types (PDT).
- [188.](./188.md) PDT can have array dimension, KIND, and character LEN parameters.
- [189.](./189.md) PDT can have fixed parameters at compile time or be ALLOCATABLE.

(pointers)=
### Pointers

- [147.](./147.md) Pointer can remap array shape and bounds.
- [148.](./148.md) Pointer should be initialized to null() to avoid undefined association status.
- [149.](./149.md) Use ALLOCATABLE arrays or ASSOCIATE instead of POINTER when possible.

(procedures)=
### Procedures

- [022.](./022.md) Functions should be `pure` and have `intent(in)` arguments
- [023.](./023.md) `elemental` functions broadcast arguments
- [024.](./024.md) Put functions and subroutines in modules to ensure that interfaces are checked
- [027.](./027.md) Optional arguments (and the `random_number` intrinsic)
- [028.](./028.md) Define and call a subroutine
- [029.](./029.md) Subroutines can have `intent(in out)` arguments, but functions should not
- [030.](./030.md) Specify function and subroutine `intent`s
- [031.](./031.md) Procedures can be recursive
- [063.](./063.md) Returning multiple values from a subroutine or function
- [067.](./067.md) How size of an array function result can depend on function arguments
- [068.](./068.md) Len of character variable function result can depend on arguments
- [074.](./074.md) Avoid implicit save
- [082.](./082.md) Two types of syntax for defining a function
- [083.](./083.md) Propagation of an optional argument
- [085.](./085.md) UnALLOCATED variable passed to a procedure is not PRESENT there.
- [086.](./086.md) Procedures can be called with a mix of named and positional arguments.
- [093.](./093.md) Fortran 2008 introduced IMPURE ELEMENTAL procedures
- [094.](./094.md) Impure elemental procedure can be used to generate array of non-uniform variates
- [097.](./097.md) Use INTRINSIC to specify that compiler-provided procedures and modules are referenced
- [098.](./098.md) VALUE attribute for procedure arguments introduced in Fortran 2003
- [100.](./100.md) An INTENT(OUT) argument is undefined at the beginning of a procedure
- [101.](./101.md) ALLOCATABLE INTENT(OUT) argument is deallocated.
- [102.](./102.md) Dummy argument that is changed must be definable in the caller.
- [105.](./105.md) A procedure can have an argument that is another PROCEDURE with an INTERFACE.
- [131.](./131.md) Fortran 2018 procedures can have assumed-rank arguments.
- [137.](./137.md) Errors in a procedure can be handled with an optional argument.
- [140.](./140.md) Internal procedures have access to variables from the host unless they are overridden by local variables.

(style)=
### Style

- [013.](./013.md) New Fortran code should use free source form and `.f90` suffix
- [099.](./099.md) Turn compiler warnings into errors to force code defects to be fixed.

