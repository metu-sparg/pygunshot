#!/usr/bin/python

import pygunshot as pgs

# Load the geometry and ballistic data
geomd = pgs.loadDict('Geometry/ExampleGeometry.json')
ballmd = pgs.loadDict('Guns/BrowningBDA380.json')

# Set duration and sampling rate
duration = 0.1
Fs = 96000.0

# Calculate anechoic signal
sig, Pmb, Pnw = pgs.getGunShot(geomd, ballmd, duration, Fs)

# Save as a normalised WAVE file
pgs.recordWave('Output/BrowningBDA380_anechoic.wav', sig, Fs)

