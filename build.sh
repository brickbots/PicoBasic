#!/bin/zsh
echo "Grabbing latest source"
cp /Volumes/CIRCUITPY/*.py python
cp /Volumes/CIRCUITPY/picobasic/*.py python/picobasic

echo "Compiling mpy files"
echo "  Basic"
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/picobasic/__init__.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/picobasic/basicparser.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/picobasic/basictoken.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/picobasic/flowsignal.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/picobasic/interpreter.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/picobasic/lexer.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/picobasic/program.py
echo "  IO"
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/buzzer.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/keyboard.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross python/screen.py

echo "Copying back to PicoBasic"
cp python/*.mpy /Volumes/CIRCUITPY
cp python/picobasic/*.mpy /Volumes/CIRCUITPY/picobasic

echo "Deleting .py files"
rm /Volumes/CIRCUITPY/picobasic/basicparser.py
rm /Volumes/CIRCUITPY/picobasic/basictoken.py
rm /Volumes/CIRCUITPY/picobasic/flowsignal.py
rm /Volumes/CIRCUITPY/picobasic/interpreter.py
rm /Volumes/CIRCUITPY/picobasic/lexer.py
rm /Volumes/CIRCUITPY/picobasic/program.py
rm /Volumes/CIRCUITPY/screen.py
rm /Volumes/CIRCUITPY/buzzer.py
rm /Volumes/CIRCUITPY/keyboard.py


