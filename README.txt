README

This repository is where I'm putting this bit of code that draws a starry night sky. Right now it's just some 
rudimentary Python that uses Pillow for its image processing, but I want to add some fun stuff in the future.

There are two scripts, skygenerator.py and kelvin_to_rgb.py. skygenerator actually draws all the stuff, while kelvin_to_rgb
is just a script I found that takes a temperature in Kelvin and converts it to an RGB value, to avoid drawing stars with weird
colors.

Some things I'd like to add is a better average star color that reflects the actual distribution of stars, and a more
sophisticated star representation (right now each star is just a circle).