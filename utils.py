import os
import numpy as np

def mkdirs(path):
    if not os.path.exists(path):
        os.mkdir(path)

def rand(low=0, high=1, size=(3,3)):
    return (high - low) * np.random.rand(*size) + low
