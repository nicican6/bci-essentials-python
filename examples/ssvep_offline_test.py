# This is a script to test the functionality of python SSVEP processing
# Written by Brian Irvine on 08/05/2021

import os

from bci_essentials.io.xdf_sources import XdfEegSource, XdfMarkerSource
from bci_essentials.bci_controller import BciController
from bci_essentials.paradigm.ssvep_paradigm import SsvepParadigm
from bci_essentials.data_tank.data_tank import DataTank
from bci_essentials.classification.ssvep_riemannian_mdm_classifier import (
    SsvepRiemannianMdmClassifier,
)

# Identify the file to simulate
# Filename assumes the data is within a subfolder called "data" located
# within the same folder as this script
filename = os.path.join("data", "ssvep_example.xdf")
eeg_source = XdfEegSource(filename)
marker_source = XdfMarkerSource(filename)
paradigm = SsvepParadigm(live_update=False, iterative_training=False)
data_tank = DataTank()

# Define the classifier
classifier = SsvepRiemannianMdmClassifier(subset=[])
classifier.set_ssvep_settings(n_splits=3, random_seed=42, n_harmonics=3, f_width=0.5)

classifier.target_freqs = [
    24,
    20.57143,
    18,
    16,
    14.4,
    12,
    10.28571,
    9,
    8,
    7.2,
    6,
    4.965517,
]

# Initialize the SSVEP
# should try to automate the reading of some of this stuff from the file header
test_ssvep = BciController(classifier, eeg_source, marker_source, paradigm, data_tank)

# initial_subset=['PO7', 'PO3', 'POz', 'PO4', 'PO8', 'O1', 'Oz', 'O2', 'Cp4', 'C4', 'F4', 'Cp3', 'C3', 'F3', 'Cz', 'Fz']
# test_ssvep.classifier.setup_channel_selection(method = "SBS", metric="accuracy", initial_channels = initial_subset,    # wrapper setup
#                                 max_time= 999, min_channels=2, max_channels=16, performance_delta=0,      # stopping criterion
#                                 n_jobs=-1)

test_ssvep.setup(
    online=False,
)
test_ssvep.run()

# Some optional plotting
# # plot a spectrogram of the session
# for ci, ch in enumerate(test_ssvep.channel_labels):
#     eeg = np.array(test_ssvep.classifier.X[0,ci,:])
#     tv = [e/test_ssvep.fsample for e in list(range(0,len(eeg)))]

#     plt.plot(tv, eeg)

# plt.show()
# plt.clf()

# for i in range(48):
#     eeg = np.array(test_ssvep.classifier.X[i,15,:])
#     tv = [e/test_ssvep.fsample for e in list(range(0,len(eeg)))]

#     f, t, Sxx = scipy.signal.spectrogram(eeg, fs=test_ssvep.fsample, nperseg=512)

#     fp, Pxx = scipy.signal.welch(eeg, fs=test_ssvep.fsample, nperseg=512, return_onesided = True)

#     f_target = test_ssvep.classifier.target_freqs[int(test_ssvep.classifier.y[i])]

#     # Plot the EEG for inspection
#     plt.subplot(311)
#     plt.plot(tv,eeg)
#     plt.title(f_target)

#     # psd
#     plt.subplot(312)
#     plt.plot(fp, Pxx)
#     plt.vlines(x=[f_target,f_target*2,f_target*3], ymin=-1000, ymax=1000)
#     plt.xlim([-0.5,50])
#     plt.ylim([-0.5,20])

#     # spectrogram
#     plt.subplot(313)
#     plt.pcolormesh(t, f, Sxx, shading='gouraud')
#     plt.ylabel('Frequency [Hz]')
#     plt.xlabel('Time [sec]')
#     plt.ylim([0,30])
#     plt.xlim([0,4])
#     plt.hlines(y=[f_target,f_target*2,f_target*3], xmin=-5, xmax=5, color='r')
#     plt.show()

#     # clear
#     plt.clf()
