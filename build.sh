#!/bin/zsh
echo "Compiling mpy files"
echo "  Basic"
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/basic2040/__init__.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/basic2040/basicparser.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/basic2040/basictoken.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/basic2040/flowsignal.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/basic2040/interpreter.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/basic2040/lexer.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/basic2040/program.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/basic2040/term.py
echo "  IO"
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/buzzer.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/picomputer_keyboard.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/feather_keyboard.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/screen.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/picoterm.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/picointerp.py

echo "Copying back to PicoBasic"
cp python/*.mpy /Volumes/CIRCUITPY
cp python/basic2040/*.mpy /Volumes/CIRCUITPY/basic2040
cp python/code.py /Volumes/CIRCUITPY/code.py
cp python/boot.py /Volumes/CIRCUITPY/boot.py

echo "Deleting .py files"
rm /Volumes/CIRCUITPY/basic2040/*.py
rm /Volumes/CIRCUITPY/screen.py
rm /Volumes/CIRCUITPY/buzzer.py
rm /Volumes/CIRCUITPY/picomputer_keyboard.py
rm /Volumes/CIRCUITPY/feather_keyboard.py
rm /Volumes/CIRCUITPY/screen.py
rm /Volumes/CIRCUITPY/picoterm.py


