__author__ = 'vuvantu'
import numpy as np
def hamming(windows_size):
    windows = np.zeros(windows_size)
    for i in range(windows_size):
        windows[i] = 0.54 - 0.46 * np.cos(2 * np.pi * i / (windows_size - 1))
    return windows
def hanning(windows_size):
    windows = np.zeros(windows_size)
    for i in range(windows_size):
        windows[i] = 0.55 - 0.55 * np.cos(2 * np.pi * i / (windows_size - 1))
    return windows
def rectangle(windows_size):
    windows = np.zeros(windows_size)
    for i in range(windows_size):
        windows[i] = 0.5 / (windows_size - 1)
    return windows
def sign(x):
    if x >= 0:
        return 1
    else:
        return -1