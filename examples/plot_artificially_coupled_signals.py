"""
=====================================
Generate artificially coupled signals
=====================================

Use the pac_signals_tort function to generate artificial PAC.
"""
import matplotlib.pyplot as plt
from tensorpac.utils import pac_signals_tort

# Generate one signal containing PAC. By default, this signal present a
# coupling between a 2hz phase and a 100hz amplitude (2 <-> 100) :
sig, time = pac_signals_tort(ntrials=1, npts=1000)

# Now, we generate a longer and weaker 4 <-> 60 coupling using the chi
#  parameter. In addition, we increase the amount of noise :
sig2, time2 = pac_signals_tort(fpha=4, famp=60, ntrials=1, chi=.9, noise=3,
                               npts=3000)

# Alternatively, you can generate multiple coupled signals :
sig3, time3 = pac_signals_tort(fpha=10, famp=150, ntrials=3, chi=0.5, noise=2)

# Finally, if you want to add variability across generated signals, use the
# dpha and damp parameters :
sig4, time4 = pac_signals_tort(fpha=10, famp=50, ntrials=3, dpha=30,
                               damp=70, npts=3000)


def plot(time, sig, title):
    """Plotting function."""
    plt.plot(time, sig.T, lw=.5, color='black')
    plt.title(title)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')


fig = plt.figure(figsize=(13, 5))
plt.subplot(1, 2, 1)
plot(time, sig, 'Strong coupling between\n2hz <-> 100hz')

plt.subplot(1, 2, 2)
plot(time2, sig2, 'Weak and noisy coupling between\n4hz <-> 60hz')

# plt.subplot(2, 2, 3)
# plot(time3, sig3, '3 signals coupled between 10hz <-> 150hz')

# plt.subplot(2, 2, 4)
# plot(time4, sig4, '3 signals coupled, with variability between 10hz <-> 50hz')

plt.show()
