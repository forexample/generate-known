This guide extends simple example from branch [master][1] so that CMake will generate sources for target that is not located in the same directory as custom command. Script `script.py` will generate file `A.cpp` which will be used to create library `A` in subdirectory `A`. Special custom target `Generate` will help to establish dependencies:

![subdirectory][2]

Important notes inherited from [master][1]:
* we know that `script.py` will create only known files (i.e. source list is fixed: `A.cpp`)
* there are only one target that use generated source files

## Try it

```bash
> cmake -H. -B_builds
> cmake --build _builds
```

Result:

```
Scanning dependencies of target Generate
[ 25%] Generate (custom command)
Generate (python script)
[ 50%] Generate (custom target)
[ 50%] Built target Generate
Scanning dependencies of target A
[ 75%] Building CXX object A/CMakeFiles/A.dir/__/generated/A.cpp.o
Linking CXX static library libA.a
[ 75%] Built target A
Scanning dependencies of target foo
[100%] Building CXX object CMakeFiles/foo.dir/main.cpp.o
Linking CXX executable foo.exe
[100%] Built target foo
```

Run build again (no rebuild):
```bash
> cmake --build _builds/
[ 25%] Generate (custom target)
[ 50%] Built target Generate
[ 75%] Built target A
[100%] Built target foo
```

Change `script.py` - check that change of `A.cpp` trigger compilation:
```bash
> grep new script.py
  return "Hello from A (new)";
> cmake --build _builds
```

Note that old `main.cpp.o` used, only `A.cpp.o` builds after custom command:
```
[ 25%] Generate (custom command)
Generate (python script)
[ 50%] Generate (custom target)
[ 50%] Built target Generate
Scanning dependencies of target A
[ 75%] Building CXX object A/CMakeFiles/A.dir/__/generated/A.cpp.o
Linking CXX static library libA.a
[ 75%] Built target A
Linking CXX executable foo.exe
[100%] Built target foo
```

## Target from subdirectory

[add_custom_command][3] create dependencies only for targets inside the **same** directory:
```
A target created in the same directory (CMakeLists.txt file) that specifies
any output of the custom command as a source file is given a rule to
generate the file using the command at build time
```

So if target `Generate` will be removed:
```cmake
# Top CMakeLists.txt
#add_custom_target(
#    Generate
#    DEPENDS "${gen_dir}/A.cpp"
#    COMMENT "Generate (custom target)"
#)
```

```cmake
# A/CMakeLists.txt
# add_dependencies(A Generate)
```

then no dependency will be established:

![subdir-nodeps][4]

and build will fail because nobody run custom command, hence no `A.cpp` file generated:
```bash
> cmake -H. -B_builds
> cmake --build _builds
Scanning dependencies of target A
make[2]: *** No rule to make target 'generated/A.cpp', needed by 'A/CMakeFiles/A.dir/__/generated/A.cpp.o'.  Stop.
...
```

So there is only one method to trigger custom command - add a target with dependent sources (sources from custom command):
```cmake
add_custom_target(
    Generate
    DEPENDS "${gen_dir}/A.cpp"
    COMMENT "Generate (custom target)"
)
```
This creates dependency between target and custom command:

![subdir-add-gen][5]

And adding dependency between target `Generate` and `A` will help to build `A.cpp` before library `A` compilation:

![subdir-add-dep][6]

## Property GENERATED

[add_custom_command][3] set property [GENERATED][7] for sources from `OUTPUT` list. Source file properties do not inherit from top [directory][8]:

```
Source file properties are visible only to targets added
in the same directory (CMakeLists.txt)
```

If remove `GENERATED`:
```cmake
# A/CMakeLists.txt
# set_source_files_properties("${gen_dir}/A.cpp" PROPERTIES GENERATED YES)
```

Build will failed since CMake expected `A.cpp` to be the regular file:
```bash
> cmake -H. -B_builds
> cmake --build _builds
...
CMake Error at A/CMakeLists.txt:2 (add_library):
  Cannot find source file:

    /.../_builds/generated/A.cpp
```

[1]: https://github.com/forexample/generate-known/tree/master
[2]: https://raw.githubusercontent.com/forexample/generate-known/subdirectory/diagrams/subdirectory.png
[3]: http://www.cmake.org/cmake/help/v3.0/command/add_custom_command.html
[4]: https://raw.githubusercontent.com/forexample/generate-known/subdirectory/diagrams/subdir-nodeps.png
[5]: https://raw.githubusercontent.com/forexample/generate-known/subdirectory/diagrams/subdir-add-gen.png
[6]: https://raw.githubusercontent.com/forexample/generate-known/subdirectory/diagrams/subdir-add-dep.png
[7]: http://www.cmake.org/cmake/help/v3.0/prop_sf/GENERATED.html
[8]: http://www.cmake.org/cmake/help/v3.0/command/set_source_files_properties.html
