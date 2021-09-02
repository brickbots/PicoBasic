#!/bin/zsh
echo "Grabbing latest source"
cp /Volumes/CIRCUITPY/*.py .
echo "Compiling mpy files"
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross basicparser.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross basictoken.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross buzzer.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross flowsignal.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross interpreter.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross keyboard.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross lexer.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross program.py
/Volumes/CP_Build/circuitpython/mpy-cross/mpy-cross screen.py
echo "Copying back to PicoBasic"
cp *.mpy /Volumes/CIRCUITPY
echo "Deleting .py files"
rm /Volumes/CIRCUITPY/basicparser.py
rm /Volumes/CIRCUITPY/basictoken.py
rm /Volumes/CIRCUITPY/buzzer.py
rm /Volumes/CIRCUITPY/flowsignal.py
rm /Volumes/CIRCUITPY/interpreter.py
rm /Volumes/CIRCUITPY/keyboard.py
rm /Volumes/CIRCUITPY/lexer.py
rm /Volumes/CIRCUITPY/program.py
rm /Volumes/CIRCUITPY/screen.py


