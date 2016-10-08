"""Muzzle blast component"""

import numpy as np
import nwave as nw
import util as utl

def friedlander(t, ta, tau, Pp=1.0):
    """
    Calculate Friedlander wave
    
    Parameters:
    ----------------
    t -- Time (numpy array)
    ta -- Arrival time (float)
    tau -- Positive phase duration (float)
    Pp -- Peak overpressure (float)

    Returns:
    ----------------
    Ps -- Muzzle blast overpressure signal (numpy array)
    """
    pinf = 101.0e3 # pinf in in Pa
    ainf = 341.0
    if t < ta:
        Ps = 0
    else:
        Ps = Pp*(1-(t-ta)/tau)*np.exp(-(t-ta)/tau)*pinf*ainf
    return Ps
    
def muzzleblast(tarr, ta, tau, Pp=1.0):
    """
    Calculate the muzzle blast component of the gunshot sound given positive phase duration
    
    Parameters:
    ----------------
    tarr --   Time instances at which the output will be calculated (numpy array)
    ta -- Time of arrival of the muzzle blast (float)
    tau -- Positive phase duration (float)
    Pp -- Peak overpressure (float)
    
    Returns:
    ----------------
    Pm -- Muzzle blast signal (numpy array)
    
    """
    sz = len(tarr)
    Pm = np.zeros(sz)
    for ind in range(sz):
        Pf = friedlander(tarr[ind], ta, tau, Pp)
        Pm[ind] = Pf
    return Pm
    
def calculatemuzzleblast(gammae, pe, ue, Ae, mu, theta, r, d, Lm, Vp, duration, Fs=192000.0):
    """
    Calculate the muzzle blast component of the gunshot sound given ballistic parameters
    
    Parameters:
    ----------------
    gammae -- Specific heat ratio (float)
    pe -- Muzzle pressure in kg/cm2 (float)
    ue -- Exit speed of propellant in m/s (float)
    Ae -- Bore area in m2 (float)
    mu -- Momentum index (float)
    theta -- Angle between the boreline and the microphone position in radians (float)
    r -- Distance of microphone from the gun (float)
    d -- Diameter of the bullet in m (float)
    Lm -- Barrel length in m (float)
    Vp -- Exit speed of projectile in m/s (float)
    duration -- Duration of the output muzzle blast signal (float)
    Fs -- Sampling rate (float)
    
    Returns:
    ----------------
    Pm -- Muzzle blast signal (numpy array)
    t -- Time instances for the calculated samples (numpy array)
    
    """
    pe =utl. convertPressureToPascals(pe)
    L = Lm
    t = np.linspace(0, duration, duration*Fs)
    l, lp = scalinglength(gammae, pe, ue, Ae, mu, theta)
    ta = timeOfArrival(r, lp)
    tau = positivePhaseDuration(r, lp, l, L, Vp)
    Pb = peakOverpressure(r, lp)
    Pmb = muzzleblast(t, ta, tau, Pb)
    return Pmb, t
    
def scalinglength(gammae, pe, ue, Ae, mu, theta):
    """
    Calculate the scaling length and the direction weighted scaling length
    
    Parameters:
    ----------------
    gammae -- Specific heat ratio (float)
    pe -- Muzzle pressure in kg/cm2 (float)
    ue -- Exit speed of propellant in m/s (float)
    Ae -- Bore area in m2 (float)
    mu -- Momentum index (float)
    theta -- Angle between the boreline and the microphone position in radians (float)
    
    Returns:
    ----------------
    l -- Scaling length (float)
    lp -- Weighted scaling length (float)
    """
    pinf = 101.0e3
    peb = pe/pinf 
    ainf = 341.0
    Me = nw.MachNumber(ue)
    dEdt = (gammae*peb*ue)/(gammae-1)*(1+(gammae-1)/2*Me**2)*Ae
    l = np.sqrt(dEdt/(pinf*ainf))
    ratio = mu*np.cos(theta) + np.sqrt(1-(mu**2)*(np.sin(theta))**2)
    lp = l*ratio*10
    return l, lp

def momentumindex(M, pe, gamma=1.24):
    """
    Calculate the momentum index
    
    Parameters:
    ----------------
    M -- Mach number (float)
    pe -- Muzzle pressure in kg/cm2 (float)
    gamma -- Specific heat ratio (float)
    
    Returns:
    ----------------
    mu -- Momentum index (float)
    """
    pe = utl.convertPressureToPascals(pe)
    pe = pe/101e3
    xmod = M*np.sqrt(gamma*pe/2)
    mu = 0.87-0.01*xmod
    return mu
    
def peakOverpressure(r, lp):
    """
    Calculate the peak overpressure of the muzzle blast
    
    Parameters:
    ----------------
    r -- Distance from the muzzle in m (float)
    lp -- Weighted scaling length (float)

    Returns:
    ----------------
    Pb -- Peak overpressure in Pa (float)
    
    """
    pinf = 101.0e3
    ainf = 341.0
    rb = r/lp
    if rb<50:
        Pb = 0.89*(lp/r)+1.61*(lp/r)**2
    else:
        Pb = 3.48975/(rb*np.sqrt(np.log(33119.0*rb)))
        
    return Pb/100

def timeOfArrival(r, lp):
    """
    Calculate the time of arrival of the muzzle blast
    
    Parameters:
    ----------------
    r -- Distance from the muzzle in m (float)
    lp -- Weighted scaling length (float)

    Returns:
    ----------------
    ta --  Time of arrival in s (float)
    
    """
    ainf = 341.0
    rb = r/lp
    X = np.sqrt(rb**2 + 1.04*rb + 1.88)
    tab = X - 0.52*np.log(2*X+2*rb+1.04)-0.56
    ta = lp*tab/ainf
    return ta
    
def positivePhaseDuration(r, lp, l, L, Vp):
    """
    positivePhaseDuration(measurementDistance, scalingLength, unscaledScalingLength, boreLengthInMeters, exitSpeedOfProjectile):
    
    Calculate the positive phase duration of the muzzle blast
    
    Parameters:
    ----------------
    r -- Distance from the muzzle in m (float)
    lp -- Weighted scaling length (float)
    l -- Scaling length (float)
    L -- Barrel length in m (float)
    Vp -- Exit speed of projectile in m/s (float)

    Returns:
    ----------------
    tau -- Positive phase duration in s (float)
    
    """
    ainf = 341.0
    rb = r/lp
    X = np.sqrt(rb**2 + 1.04*rb + 1.88)
    delta = (L*ainf)/(Vp*l)
    G = 0.09 - 0.00379*delta + 1.07*(1-1.36*np.exp(-0.049*rb))*l/lp
    if rb<50:
        tb = rb - X + 0.52*np.log(2*X+2*rb+1.04) + 0.56 + G
    else:
        tb = 2.99*np.sqrt(np.log(33119.0*rb)) - 8.534 + G
    t = tb*lp/ainf
    return t