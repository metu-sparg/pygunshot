import numpy as np
import muzzleblast  as mb
import nwave as nw
import util as utl

def _getAnechoicGunshot(xmic, xgun, ngun, bulletDiam, bulletLen, barrelLength, pexit, uexit, duration, Fs=192000.0):
    '''
    Get an anechoic gunshot using the geometry and ballistic parameters
    
    Parameters:
    ----------------
    xmic -- Microphone position (3x1 numpy array)
    xgun -- Gun position (3x1 numpy array)
    ngun -- Barrel axis direction (3x1 numpy array)
    bulletDiam -- Bullet diameter in m (float)
    bulletLen -- Bullet length in m (float)
    barrelLength -- Barrel length of the gun (float)
    pexit -- Muzzle pressure in kg/cm2 (float)
    uexit -- Exit velocty of the bullet in m/s (float)
    duration -- Duration of the output signal in s (float)
    Fs -- Sampling rate in Hz (float)
    
    Returns:
    ------------
    sig -- The calculated gunshot signal (numpy array)
    
    '''
    
    xmic = np.array(xmic)
    xgun = np.array(xgun)
    ngun = np.array(ngun)
    gammae = 1.24
    r, theta = utl.computeGeometry(xmic, xgun)
    Ae = (bulletDiam/2)**2*np.pi
    M = nw.MachNumber(uexit)
    mu = mb.momentumindex(M, pexit, gammae)
    Vp = uexit
    Lm = barrelLength
    d = bulletDiam
    l = bulletLen
    xmiss = r*np.sin(theta)
    
    Pmb, t = mb.calculatemuzzleblast(gammae, pexit, uexit, Ae, mu, theta, r, d, Lm, Vp, duration, Fs)
    sig = Pmb
    thM = nw.coneAngle(uexit)
    
    Pnw = np.zeros(sig.size)

    if (uexit > 341.0) & (theta<np.pi-thM): # We have sonic boom
        Pnw = nw.calculateNWave(xgun, ngun, xmic, uexit, d, l, xmiss, duration, Fs)
        sig = Pmb + Pnw
    
    return sig, Pmb, Pnw
    
def getGunShot(geomDict, ballistDict, duration, Fs):
    '''
    Get anechoic gunshot
    
    Parameters:
    ----------------
    geomDict -- Dictionary containing the scene geometry (dict)
    ballistDict -- Dictionary containing the ballistic information (dict)
    duration -- Duration of the output signal in s (float)
    Fs -- Sampling rate in Hz (float)
    
    Returns:
    ----------------
    sig -- Anechoic gunshot sound signal 
    '''
    label, xgun, xmic, ngun = utl.unpackGeometry(geomDict)
    gunlabel, ammolabel, bulletDiam, bulletLen, barrelLength, pexit, uexit = utl.unpackBallistics(ballistDict)
    sig, Pmb, Pnw = _getAnechoicGunshot(xmic, xgun, ngun, bulletDiam, bulletLen, barrelLength, pexit, uexit, duration, Fs)
    return sig, Pmb, Pnw
