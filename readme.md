# Pygame Keyboard Viewer

A simple python script to draw keyboard inputs on the screen using pygame.
Made as an excercise for the sake of learning about pygame key locals and key events versus pygame key convenience functions.
The keyboard is modeled off a 2011 MacbookPro.

Helpful for mapping pygame key constants, particularly the non-obvious ones like the Command key on a Mac (K_LMETA and K_RMETA).
Also good for testing [key rollover](https://en.wikipedia.org/wiki/Rollover_(key)). At the end of the gif demo below, the keys 1-7 are pressed but only 1-6 are registered by pygame due to the limitations of the keyboard.

![Demo](https://media.giphy.com/media/26ni7qnnWMoK1Vzkk/giphy.gif)
