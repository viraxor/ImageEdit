# ImageEdit
a small image editing project in Python and Tkinter

## usage
this is a small project that can modify images in various ways. 
### main program
* when main.py is ran, you get a file dialogue where you can select the image that you want to open.
* the image opens and you are greeted with a window where your image is shown and under it are some buttons.
* those buttons are the filters that can be used in order to manipulate the image.
* you can scroll through all the buttons by pressing left and right arrows on the (broken) scrollbar.
* the tabs above buttons are used for different types of manipulating the image.
* there are effects, macros and kernels.
### effects
* effects are built-in image operations that come with ImageEdit. 
* if you want to make new effects, you can do so by making a new function in the effects.py file.
### macros
* macros are instructions that say what effects should be performed to the image.
* they can be created with the ImageEdit Macro Creator (accessible in the View menu in ImageEdit).
* when it is opened, you have a bunch of buttons on the right and a big white box on the left.
* the big white box is where all your effects are listed.
* you can add and remove effects by clicking the buttons on the right side.
* for removing effects, you must select the effects that you wanna remove.
* you can save using the File menu.
### kernels
* kernels are small matrixes that are used for doing a convolution between the kernel and the image.
* they can be created with the ImageEdit Kernel Creator (accessible in the View menu in ImageEdit).
* you can set if you want the grid to be 5x5 or 3x3. 
* left click on a button in the grid to increment it, right click to decrement it.
* you can save using the File menu.

_note: if you make any effects, macros or kernels, it is encouraged to submit them as a pull request, so other people can use it too!_
