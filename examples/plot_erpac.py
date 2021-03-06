"""
=====================================
Compute the ERPAC (Voytek et al 2013)
=====================================

Event-Related Phase-Amplitude Coupling (ERPAC) do not measure PAC across time
cycle but instead, across trials (just as proposed JP. Lachaux with the
PLV/PLS). Measuring across trials enable to have a real-time estimation of PAC.
Warning, depending on your data, even with tensor calculation the ERPAC is
significantly slower. Don't worry, take a coffee.

In this example, we generate a signal that have a 10<->100hz coupling the first
1000 points, then, the 700 following points are noise.
"""
import numpy as np
from tensorpac import Pac, pac_signals_tort

# Generate a 10<->100hz coupling :
ntrials = 300
npts = 1000
sf = 1024.
x1, tvec = pac_signals_tort(fpha=10, famp=100, ntrials=ntrials, noise=2,
                            npts=npts, dpha=10, damp=10, sf=sf)
# Generate noise and concatenate the coupling and the noise :
x2 = np.random.rand(ntrials, 700)
x = np.concatenate((x1, x2), axis=1)  # Shape : (ntrials, npts)
time = np.arange(x.shape[1]) / sf

# Define a PAC object :
p = Pac(fpha=[9, 11], famp=(60, 140, 5, 1), dcomplex='wavelet', width=12)

# Extract the phase and the amplitude :
pha = p.filter(sf, x, axis=1, ftype='phase')  # Shape (npha, ntrials, npts)
amp = p.filter(sf, x, axis=1, ftype='amplitude')  # Shape (namp, ntrials, npts)

# Compute the ERPAC and use the traxis to specify that the trial axis is the
# first one :
erpac, pval = p.erpac(pha, amp, traxis=1)

# Remove unused dimensions :
erpac, pval = np.squeeze(erpac), np.squeeze(pval)

# Plot without p-values :
p.pacplot(erpac, time, p.yvec, xlabel='Time (second)', cmap='Spectral_r',
          ylabel='Amplitude frequency', title=str(p), cblabel='ERPAC',
          vmin=0., rmaxis=True)

# Plot with every non-significant values masked in gray :
# p.pacplot(erpac, time, p.yvec, xlabel='Time (second)', cmap='Spectral_r',
#           ylabel='Amplitude frequency', title='ERPAC example', vmin=0.,
#           vmax=1., pvalues=pval, bad='lightgray', plotas='contour',
#           cblabel='ERPAC')

# Plot with significiendy levels :
# p.pacplot(erpac, time, p.yvec, xlabel='Time (second)', cmap='Spectral_r',
#           ylabel='Amplitude frequency', title='ERPAC example', vmin=0.,
#           vmax=1., pvalues=pval, levels=[1e-20, 1e-10, 1e-2, 0.05],
#           levelcmap='inferno', plotas='contour', cblabel='ERPAC')
# p.savefig('erpac.png', dpi=300)
p.show()
