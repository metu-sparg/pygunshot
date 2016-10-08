##PyGun: Procedural Generation of Anechoic Gunshot Sounds

This project contains the PyGunshot module which includes several functions to generate anechoic gunshot sounds for games and simulations. The ballistic parameters should be provided (or generated procedurally) as well as the geometry which includes the gun and microphone positions. 

**IMPORTANT NOTE**: The presented code generated only the anechoic samples and you need to process the generated sounds using an artificial reverberator or convolve it with a room impulse response to obtain a sound that resembles gunshots.   

This code accompanies the chapter:

######Hacıhabiboğlu, H., "Procedural Generation of Gunshot Sounds based on Physically-motivated Models" in *Procedural Content Generation in the Games Industry*, Eds. Oliver Korn and Newton Lee, Springer Verlag, 2017 (to appear)

####Installation

`pip install pygunshot`

####Usage

See `example.py` under `scripts` folder to get started.

####Questions?

Please drop an e-mail to <mailto:husshho@gmail.com>