"""N-wave component"""

import numpy as np

def MachNumber(v):
    '''
    Calculate Mach number
    
    Parameters:
    ----------------
    v -- Speed of projectile (float)

    Returns:
    ----------------
    M -- Mach number (float)
    '''
    csnd = 341.0
    M = v/csnd
    return M

def coneAngle(M):
    '''
    Calculate the cone angle
    
    Parameters:
    ----------------
    M -- Mach number (float)
    
    Returns:
    ----------------
    theta -- Mach cone angle in radians (float)
    
    '''
    theta = np.arcsin(1.0/M)
    return theta
    
def missDistance(xgun, ngun, xmic):
    '''
    Calculate miss distance
    
    Parameters:
    ----------------
    xgun -- Gun position (3x1 numpy array)
    ngun -- Barrel look direction (3x1 numpy array)
    xmic -- Microphone position (3x1 numpy array)
                    
    Returns:
    ----------------
    dmis -- Miss distance in m (float)
    dlin -- Distance from gun to the mic line in m (float)
    '''
    xmic = np.array(xmic) # Microphone position
    xgun = np.array(xgun) # Gun position
    mvec = xmic-xgun # Vector from mic to gun position
    dvec = np.sqrt(np.dot(mvec, mvec)) # Distance from gun to mic
    ngun = ngun/np.sqrt(np.dot(ngun, ngun)) # Gun look direction (i.e. projectile direction)
    dlin = np.dot(mvec,ngun); # Distance from gun to the mic line
    dmis = np.sqrt(np.power(dvec,2)-np.power(dlin,2)) # Miss distance
    return dmis, dlin

def nWaveOverPressure(v, d, l, x):
    '''
    Calculate N-wave overpressure
    
    Parameters:
    ----------------
    v -- Projectile velocity in m/s (float)
    d -- Projectile diameter im m (float)
    l -- Projectile length in m (float)
    x -- Miss distance in m (float)
                    
    Returns:
    ----------------
    delP -- N-wave overpressure in Pa (float)
    '''
    P0 = 101.0e3 # Ambient pressure in Pa
    M = MachNumber(v)
    delP = 0.53*d*np.power((np.power(M,2)-1), 0.125)/(np.power(x,0.75)*np.power(l,0.25))*P0
    return delP
    
def nWaveDuration(v, d, l, x):
    '''
    Calculate N-wave period
    
    Parameters:
    ----------------
    v -- Projectile velocity in m/s (float)
    d -- Projectile diameter im m (float)
    l -- Projectile length in m (float)
    x -- Miss distance in m (float)
                    
    Returns:
    ----------------
    Td -- N-wave perios in s (float)
    '''
    cs = 341.0
    M = MachNumber(v)
    L = 1.82*d*(M*np.power(x,0.25))/(np.power(np.power(M,2)-1,0.375)*np.power(l,0.25))
    Td = L/cs
    return Td

def nWaveTimeOfArrival(v, xgun, ngun, xmic):
    '''
    Calculate miss distance
    
    Parameters:
    ----------------
    v -- Projectile velocity in m/s (float)
    xgun -- Gun position (3x1 numpy array)
    ngun -- Barrel look direction (3x1 numpy array)
    xmic -- Microphone position (3x1 numpy array)
                    
    Returns:
    ----------------
    ta -- N-wave time-of-arrival in s (float)
    '''
    cs = 341.0
    M = MachNumber(v)
    th =coneAngle(M)
    dmis, dlin = missDistance(xgun, ngun, xmic)
    ta = np.cos(th)*dmis/cs + dlin/v
    # ta = (dlin-dmis*np.tan(th))/v + dmis/np.cos(th)/cs
    return ta

def nWaveRiseTime(pmax):
    '''
    Calculate N-wave rise time
  
    Parameters:
    ----------------
    pmax -- N-wave overpressure in Pa (float)
    
    Returns:
    ----------------
    trise -- N-wave rise time in s (float)
    '''
    lamb = 68.0e-9 # Molecular mean free path
    P0 = 101.0e3
    cs = 341.0
    trise = lamb/cs*P0/pmax
    
    return trise
    


def nWave(xgun, ngun, xmic, v, d, l, x, t):
    '''
    Calculate the value of N-wave at the given time
    '''
    pmax = nWaveOverPressure(v, d, l, x)
    ta = nWaveTimeOfArrival(v, xgun, ngun, xmic)
    Td = nWaveDuration(v, d, l, x)

    tr = nWaveRiseTime(pmax)
    
    if ( t < ta ):
        wv = 0
    elif ( t <= (ta+tr) ) & ( t > ta ):
        wv = (t-ta)/tr*pmax
    elif ( t <= (ta+Td-tr) ) & ( t > (ta+tr) ):
        wv = (1-2*(t-ta-tr)/(Td-2*tr))*pmax
    elif ( t <= (ta+Td)) & ( t > (ta+Td-tr) ):
        wv = (-1.0 + (t-ta-Td+tr)/tr)*pmax
    else: 
        wv = 0
    
    return wv


def calculateNWave(xgun, ngun, xmic, v, d, l, x, dur, Fs=192000.0):
    '''
    Calculate N-wave signal
    
    Parameters:
    ----------------
    xgun -- Gun position (3x1 numpy array)
    ngun -- Barrel look direction (3x1 numpy array)
    xmic -- Microphone position (3x1 numpy array)
    v -- Projectile velocity in m/s (float)
    d -- Projectile diameter im m (float)
    l -- Projectile length in m (float)
    x -- Miss distance in m (float)
    dur -- duration in s (float)
    Fs -- Sampling rate in Hz (float)
                    
    Returns:
    ----------------
    nw -- N-wave signal (numpy array)
    '''
    t = np.linspace(0, dur, dur*Fs)
    wv = np.zeros(len(t))
    for ind in range(len(t)):
        wv[ind] = nWave(xgun, ngun, xmic, v, d, l, x, t[ind])
    return wv
