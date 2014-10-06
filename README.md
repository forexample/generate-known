This guide extends simple example from branch [master][1] so that CMake will generate sources for several targets instead of one. Script `script.py` will generate files `A.cpp`, `B.cpp` and `C.cpp` these files will be used to create libraries `A`, `B` and `C`:

![multiple][2]

Important notes inherited from [master][1]:
* we know that `script.py` will create only known files (i.e. source list is fixed: `A.cpp`, `B.cpp` and `C.cpp`)
* custom command and target is in the same directory

## One/Multiple difference

[add_custom_command][3] has known limitation about parallel build:
```
Do not list the output in more than one independent target that may build
in parallel or the two instances of the rule may conflict (instead use
add_custom_target to drive the command and make the other targets depend on that one)
```

Try example with `-j3` (for `Makefile` generator):
```bash
> cmake -H. -B_builds
> cmake --build _builds -- -j3
```

Result is correct (run custom command once, races only for independent target `A`, `B` and `C`):
```bash
> cmake --build _builds -- -j3
Scanning dependencies of target Generated
[ 11%] Generate (custom command)
Generate (python script)
[ 22%] Generate (target)
[ 22%] Built target Generated
Scanning dependencies of target A
Scanning dependencies of target B
Scanning dependencies of target C
[ 33%] [ 44%] [ 55%] Building CXX object CMakeFiles/A.dir/generated/A.cpp.o
Building CXX object CMakeFiles/B.dir/generated/B.cpp.o
Building CXX object CMakeFiles/C.dir/generated/C.cpp.o
Linking CXX static library libB.a
Linking CXX static library libA.a
Linking CXX static library libC.a
[ 66%] [ 77%] [ 88%] Built target A
Built target B
Built target C
Scanning dependencies of target foo
[100%] Building CXX object CMakeFiles/foo.dir/main.cpp.o
Linking CXX executable foo.exe
[100%] Built target foo
```

Run again (verify no changes):
```bash
> cmake --build _builds
[ 11%] Generate (target)
[ 22%] Built target Generated
[ 44%] Built target A
[ 66%] Built target B
[ 88%] Built target C
[100%] Built target foo
```

## Dependencies

Dependencies `{A, B, C} -> Generate` are important:

```cmake
add_dependencies(A Generated)
add_dependencies(B Generated)
add_dependencies(C Generated)
```

because otherwise there are not much difference - targets still build independently, hence they run custom command simultaneously (also note that `Generate` excluded from `ALL`):

![parallel][4]

```cmake
# Remove dependency
# add_dependencies(A Generated)
# add_dependencies(B Generated)
# add_dependencies(C Generated)
```

Run new code:
```bash
> cmake -H. -B_builds
> cmake --build _builds -- -j3
```

See that now there are 3 run of the custom command which lead to crash:
```
> cmake --build _builds -- -j3
[ 14%] [ 28%] [ 42%] Generate (custom command)
Generate (custom command)
Generate (custom command)
Generate (python script)
Generate (python script)
No changes!
CMakeFiles/A.dir/build.make:53: recipe for target 'generated/A.cpp' failed
...
```

Moving from file-level to target-level solve the problem:

![target-level][5]

[1]: https://github.com/forexample/generate-known/tree/master
[2]: https://raw.githubusercontent.com/forexample/generate-known/multiple/diagrams/multiple.png
[3]: http://www.cmake.org/cmake/help/v3.0/command/add_custom_command.html
[4]: https://raw.githubusercontent.com/forexample/generate-known/multiple/diagrams/parallel.png
[5]: https://raw.githubusercontent.com/forexample/generate-known/multiple/diagrams/target-level.png
