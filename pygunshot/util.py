import numpy as np
import scipy.io.wavfile as wav
import json

def caliberToM(cal):
    '''
    Convert calibers to millimeters
    '''
    diam = cal*0.0254 # Diameter in meters
    rad = diam/2 # Projectile radius
    Ae = rad**2*np.pi # Projectile/bore area
    
    return diam, Ae
    
def convertPressureToPascals(mpressure):
    """
    Convert pressure given in kg/cm2 to Pascals
    """
    ppas = 98066.5 * mpressure
    return ppas

  
def recordWave(filename, sig, Fs=192000.0):
    '''
    Write the normalized signal as a wav file
    
    Parameters:
    ----------------
    filename -- File name including its path (string)
    sig -- Signal to be stored as a wav file (numpy array)
    Fs -- Sampling rate in Hz (float)    
    '''
    siga = abs(sig)
    sig = sig/siga.max()
    wav.write(filename, Fs, sig)

    return 1
    
def computeGeometry(xmic, xgun):
    '''
    Calculate the distance and the direction of the gun
    
    Parameters:
    ----------------
    xgun -- Gun position (3x1 numpy array)
    xmic -- Microphone position (3x1 numpy array)
    
    Returns:
    ------------
    r -- Distance in m (float)
    theta -- Direction in radians (float)
    '''
    r = np.linalg.norm(xmic-xgun)
    theta = np.arccos(np.dot(xmic-xgun, (0, 1.0, 0))/r)
    return r, theta
    
def packGeometry(xgun, xmic, ngun, label):
    '''
    Pack geometry of the gun and mic
    
    Parameters:
    ----------------
    xgun -- Gun position (3x1 numpy array)
    xmic -- Microphone position (3x1 numpy array)
    ngun -- Gun look direction (3x1 numpy array)
    label -- Name of the geometry (string)
    
    Returns:
    -----------
    geomDict -- Dictionary containing geometry (dict)
    
    '''
    geomDict = dict()
    geomDict['xgun'] = xgun.tolist() # Make the np array serialisable
    geomDict['xmic'] = xmic.tolist()
    geomDict['ngun'] = ngun.tolist()
    geomDict['label'] = label
    return geomDict
    
def unpackGeometry(geomDict):
    '''
    Unpack geometry of the gun and mic
    
    Parameters:
    ----------------
    geomDict -- Dictionary containing geometry (dict)
    
    Returns:
    -----------
    xgun -- Gun position (3x1 numpy array)
    xmic -- Microphone position (3x1 numpy array)
    ngun -- Gun look direction (3x1 numpy array)
    
    '''
    xgun = np.array(geomDict['xgun'])
    xmic = np.array(geomDict['xmic'])
    ngun = np.array(geomDict['ngun'])
    label = geomDict['label']
    return label, xgun, xmic, ngun
    
    
def packBallistics(bulletDiam, bulletLen, barrelLength, pexit, uexit, gunlabel, ammolabel):
    '''
    Pack geometry of the gun and mic
    
    Parameters:
    ----------------
    bulletDiam -- Bullet diameter in m (float)
    bulletLen -- Bullet length in m (float)
    barrelLength -- Barrel length of the gun (float)
    pexit -- Muzzle pressure in kg/cm2 (float)
    uexit -- Exit velocty of the bullet in m/s (float)
    gunlabel -- Name of the gun (string)
    ammolabel -- Name of the ammunition (string)
    
    Returns:
    ------------
    ballistDict -- Ballistic data structure (numpy array)
    
    '''
    ballistDict = dict()
    ballistDict['bulletDiam'] = bulletDiam
    ballistDict['bulletLen'] = bulletLen
    ballistDict['barrelLength'] = barrelLength
    ballistDict['pexit'] = pexit
    ballistDict['uexit'] = uexit
    ballistDict['gunlabel'] = gunlabel
    ballistDict['ammolabel'] = ammolabel
    return ballistDict

def unpackBallistics(ballistDict):
    '''
    Unpack geometry of the gun and mic
    
    Parameters:
    ----------------
    ballistDict -- The calculated gunshot signal (numpy array)
    
    Returns:
    ------------
    bulletDiam -- Bullet diameter in m (float)
    bulletLen -- Bullet length in m (float)
    barrelLength -- Barrel length of the gun (float)
    uexit -- Exit velocty of the bullet in m/s (float)
    
    '''
    bulletDiam = ballistDict['bulletDiam']
    bulletLen = ballistDict['bulletLen']
    barrelLength = ballistDict['barrelLength']
    pexit = ballistDict['pexit']
    uexit = ballistDict['uexit']
    gunlabel = ballistDict['gunlabel']
    ammolabel = ballistDict['ammolabel']
    return gunlabel, ammolabel, bulletDiam, bulletLen, barrelLength, pexit, uexit

def saveDict(dictionary, filename):
    '''
    Save a dictionary as a JSON object
    
    Parameters:
    ----------------
    dictionary -- Dictionary of items (dict)
    filename -- Path and name of the file to be written (string)    
    '''
    with open(filename, 'wb') as fl:
        json.dump(dictionary, fl)
    return 1
        
def loadDict(filename):
    '''
    Load a dictionary stored a JSON object
    
    Parameters:
    ----------------
    dictionary -- Dictionary of items (dict)
    filename -- Path and name of the file to be written (string)    
    '''
    fp = open(filename, 'r')
    dct = json.load(fp)
    return dct
