# %%

import sys
sys.path.append('C:/Users/wjd__/qua-libs/Tutorials/intro-to-octave')
from qm import QuantumMachinesManager
from qm.qua import *
from qm.octave import *
from configuration_TWPA_240807 import *
from qm import SimulationConfig
import time
import numpy as np

# Specify where to store the outcome of the calibration (correction matrix, offsets...)
octave_config.set_calibration_db(os.getcwd())
qmm = QuantumMachinesManager(host=qop_ip, cluster_name='twpa_test', octave=octave_config)
qm = qmm.open_qm(config)
# %%
with program() as pump:
    with infinite_loop_(): # cw 1000ns 짜리를 무한히 계속 한다는건가(zero latency between iterations)
            play("cw"*amp(0.45), element="pump") #-67.9dBm
# %%
calibration = True
elements=["pump"]
if calibration:
    print("-" * 37 + " Play before calibration")
    #Step 5.1: Connect RF1 and run these lines in order to see the uncalibrated signal first
    job = qm.execute(pump)
    time.sleep(1)  # The program will run for 10 seconds
    job.halt()
    #Step 5.2: Run this in order to calibrate
    for element in elements:
        print("-" * 37 + f" Calibrates {element}")
        qm.octave.calibrate_element(element, [(6e9,50e6)])  # can provide many IFs for specific LO
    # Step 5.3: Run these and look at the spectrum analyzer and check if you get 1 peak at LO+IF (i.e. 6.05GHz)
    print("-" * 37 + " Play after calibration")
    job = qm.execute(pump)
    time.sleep(30)  # The program will run for 30 seconds
    job.halt()
# %%
job = qm.execute(pump)
# job.halt()
# %%
job.halt()
# %%
