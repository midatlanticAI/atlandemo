@echo off
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x64
cl /std:c++17 /O2 wave_engine.cpp /Fe:wave_engine.exe
if %errorlevel% == 0 (
    echo Compilation successful!
    wave_engine.exe
) else (
    echo Compilation failed!
) 