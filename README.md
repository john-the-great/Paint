# Paint

The simple logic thats used to simply just draw, is a regular pygame.rect.draw func, however at the same time, i get the (x, y) position of said tile that ive chosen to 
draw on and i put this into a formatted string, i then use that as the key for my canvas tiles dictionary, and go to that tile, and change the colour. 

For example:
key = f'{x} {y}'

self.tiles[key] = self.curr_colour

this also changes the saved colour of the tile i just clicked on. The point of this is not to change the colour of the tile i clicked on, because i do that just by
drawing a new rect over it. It is used for the 'fill' func in my program. Which requires the colour of each tile its checking to see which one to change and which 
one to not.

The code is very messy and unoptimised, however it does work, with some bugs. (Most with changing the tile size after setting the canvas tile size)

HOW_TO_USE
When you first open this program, using the mouse wheel, you must change the tile size. Once youve chosen this, hit enter and you can start drawing. To chose a colour,
just click on one of the colours at the bottom right, or clock the colourful swaure icon and change each rgb value and watch that colour appear in real time. (Once again
you use the mouse wheel for this). The rest is very self explanatory and can be understood with some playing around.
