This guide extends simple example from branch [master][1] so that CMake will generate sources for several targets instead of one. Script `script.py` will generate files `A.cpp`, `B.cpp` and `C.cpp` these files will be used to create libraries `A`, `B` and `C`:

![multiple][2]

Important notes inherited from [master][1]:
* we know that `script.py` will create only known files (i.e. source list is fixed: `A.cpp`, `B.cpp` and `C.cpp`)
* custom command and target is in the same directory

## One/Multiple difference

[add_custom_command] has known limitation about parallel build:
```
Do not list the output in more than one independent target that may build
in parallel or the two instances of the rule may conflict (instead use
add_custom_target to drive the command and make the other targets depend on that one)
```

Try example with `-j4` (for `Makefile` generator):
```bash
> cmake -H. -B_builds
> cmake --build _builds -- -j4
```

Result is correct (run custom command once, races only for independent target `A`, `B` and `C`):
```bash
> cmake --build _builds -- -j4
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



[1]: https://github.com/forexample/generate-known/tree/master
[2]: TODO
[3]: http://www.cmake.org/cmake/help/v3.0/command/add_custom_command.html
