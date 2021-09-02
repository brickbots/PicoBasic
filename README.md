# PicoBasic
PyBasic ported to Circuitpython

Changes for compatibility with Vintage Basic / MS Basic varients

* Print element separator changed to ;
* Print will not print cr/lf if final token is ;
* Input prompt / variable separator changed to ;
* RND required argument. Negative values reseed with that value, Zero returns last value (not implemented), any positive number returns random float between 0 and 1
* DIM allows multiple array definitions seperated by commas
* DIM over dim by 1 to handle dialetcs that are 1 based and expect there to be an element = length

New functions / keywords
* FREE : reports free memory at prompt
* TONE freq duration : plays a tone of frequency for duration
* CURSOR x y : moves the terminal cursor to X/Y
* GETCHR : waits for a single keypress from the keyboard.  Returns the ascii value of key
* CLR : clears the screen, works in a statement or at prompt
