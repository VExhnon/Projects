import numpy as np

def easom(arr):
    temp1_pow1 = (arr[0] - np.pi)**2
    temp1_pow2 = (arr[1] - np.pi)**2
    temp1 = np.exp(-temp1_pow1 - temp1_pow2)
    temp2 = -1 * np.cos(arr[0]) * np.cos(arr[1])
    return temp2 * temp1

def styblinski(arr):
    sum = 0
    for i in range(len(arr)):
        sum += np.power(arr[i], 4) - (16 * np.power(arr[i], 2)) + (5 * arr[i])
    return sum/2

def crossInTray(arr):
    temp1_pow1 = np.power(arr[0], 2) + np.power(arr[1], 2)
    temp1 = np.abs(100 - (np.sqrt(temp1_pow1)/np.pi))
    temp2 = np.sin(arr[0]) * np.sin(arr[1]) * np.exp(temp1)
    temp3 = np.power((np.abs(temp2) + 1), 0.1)
    return -0.0001 * temp3