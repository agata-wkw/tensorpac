"""Filtering tools."""
import numpy as np
from scipy.signal import filtfilt, butter, bessel


__all__ = ('filtdata')

###############################################################################
###############################################################################
#                                FILT DATA
###############################################################################
###############################################################################


def filtdata(x, sf, f, axis, filt, cycle, filtorder):
    """Filt the data using a forward/backward filter to avoid phase shifting.

    Parameters
    ----------
    x : array_like
        Array of data

    sf : float
        Sampling frequency

    f : array_like
        Frequency vector of shape (N, 2)

    axis : int
        Axis where the time is located.

    filt : string
        Name of the filter to use (only if dcomplex is 'hilbert'). Use
        either 'eegfilt', 'butter' or 'bessel'.

    filtorder : int
        Order of the filter (only if dcomplex is 'hilbert')

    cycle : int
        Number of cycles to use for fir1 filtering.
    """
    # fir1 filter :
    if filt == 'fir1':
        forder = fir_order(sf, x.shape[axis], f[0], cycle=cycle)
        b, a = fir1(forder, f / (sf / 2))

    # butterworth filter :
    elif filt == 'butter':
        b, a = butter(filtorder, [(2 * f[0]) / sf, (2 * f[1]) / sf],
                      btype='bandpass')
        forder = None

    # bessel filter :
    elif filt == 'bessel':
        b, a = bessel(filtorder, [(2 * f[0]) / sf, (2 * f[1]) / sf],
                      btype='bandpass')
        forder = None

    return filtfilt(b, a, x, padlen=forder, axis=axis)

###############################################################################
###############################################################################
#                       FILTER ORDER
###############################################################################
###############################################################################


def fir_order(fs, sizevec, flow, cycle=3):
    filtorder = cycle * (fs // flow)

    if (sizevec < 3 * filtorder):
        filtorder = (sizevec - 1) // 3

    return int(filtorder)


###############################################################################
###############################################################################
#                            FIR1
###############################################################################
###############################################################################


def n_odd_fcn(f, o, w, l):
    """Odd case."""
    # Variables :
    b0 = 0
    m = np.array(range(int(l + 1)))
    k = m[1:len(m)]
    b = np.zeros(k.shape)

    # Run Loop :
    for s in range(0, len(f), 2):
        m = (o[s + 1] - o[s]) / (f[s + 1] - f[s])
        b1 = o[s] - m * f[s]
        b0 = b0 + (b1 * (f[s + 1] - f[s]) + m / 2 * (
            f[s + 1] * f[s + 1] - f[s] * f[s])) * abs(
            np.square(w[round((s + 1) / 2)]))
        b = b + (m / (4 * np.pi * np.pi) * (
            np.cos(2 * np.pi * k * f[s + 1]) - np.cos(2 * np.pi * k * f[s])
        ) / (k * k)) * abs(np.square(w[round((s + 1) / 2)]))
        b = b + (f[s + 1] * (m * f[s + 1] + b1) * np.sinc(2 * k * f[
            s + 1]) - f[s] * (m * f[s] + b1) * np.sinc(2 * k * f[s])) * abs(
            np.square(w[round((s + 1) / 2)]))

    b = np.insert(b, 0, b0)
    a = (np.square(w[0])) * 4 * b
    a[0] = a[0] / 2
    aud = np.flipud(a[1:len(a)]) / 2
    a2 = np.insert(aud, len(aud), a[0])
    h = np.concatenate((a2, a[1:] / 2))

    return h


def n_even_fcn(f, o, w, l):
    """Even case."""
    # Variables :
    k = np.array(range(0, int(l) + 1, 1)) + 0.5
    b = np.zeros(k.shape)

    # # Run Loop :
    for s in range(0, len(f), 2):
        m = (o[s + 1] - o[s]) / (f[s + 1] - f[s])
        b1 = o[s] - m * f[s]
        b = b + (m / (4 * np.pi * np.pi) * (np.cos(2 * np.pi * k * f[
            s + 1]) - np.cos(2 * np.pi * k * f[s])) / (
            k * k)) * abs(np.square(w[round((s + 1) / 2)]))
        b = b + (f[s + 1] * (m * f[s + 1] + b1) * np.sinc(2 * k * f[
            s + 1]) - f[s] * (m * f[s] + b1) * np.sinc(2 * k * f[s])) * abs(
            np.square(w[round((s + 1) / 2)]))

    a = (np.square(w[0])) * 4 * b
    h = 0.5 * np.concatenate((np.flipud(a), a))

    return h


def firls(n, f, o):
    # Variables definition :
    w = np.ones(round(len(f) / 2))
    n += 1
    f /= 2
    l = (n - 1) / 2

    nodd = bool(n % 2)

    if nodd:  # Odd case
        h = n_odd_fcn(f, o, w, l)
    else:  # Even case
        h = n_even_fcn(f, o, w, l)

    return h


####################################################################
# - Compute the window :
####################################################################
def fir1(n, wn):
    # Variables definition :
    nbands = len(wn) + 1
    ff = np.array((0, wn[0], wn[0], wn[1], wn[1], 1))

    f0 = np.mean(ff[2:4])
    l = n + 1

    mags = np.array(range(nbands)) % 2
    aa = np.ravel(np.matlib.repmat(mags, 2, 1), order='F')

    # Get filter coefficients :
    h = firls(l - 1, ff, aa)

    # Apply a window to coefficients :
    wind = np.hamming(l)
    b = np.matrix(h.T * wind)
    c = np.matrix(np.exp(-1j * 2 * np.pi * (f0 / 2) * np.array(range(l))))
    b = b / abs(c * b.T)

    return np.squeeze(np.array(b)), 1
