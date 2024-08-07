"""
Octave configuration working for QOP222 and qm-qua==1.1.5 and newer.
"""
from set_octave import OctaveUnit, octave_declaration
from qm.octave import *
import numpy as np
import os

######################
# Network parameters #
######################
qop_ip = "10.2.1.110"  # Write the QM router IP address
cluster_name = 'twpa_test'  # Write your cluster_name if version >= QOP220
qop_port = None  # Write the QOP port if version < QOP220


############################
# Set octave configuration #
############################
# Must be 11xxx, where xxx are the last three digits of the Octave IP address
oct1 = OctaveUnit("oct1", qop_ip, port=11237, con="con1")

# Add the octaves
octaves = [oct1]
# Configure the Octaves
octave_config = QmOctaveConfig()
# Specify where to store the outcome of the calibration (correction matrix, offsets...)
# octave_config.set_calibration_db(os.getcwd())

#####################
# OPX configuration #
#####################
IF=500e6
LO = 6e9
con = "con1"
octave = "oct1"
config = {
    "version": 1,
    "controllers": {
        con: {
            "analog_outputs": {
                3: {"offset": 0.0},
                4: {"offset": 0.0}
            },
            "digital_outputs": {
                1: {}
            }
            ,
            "analog_inputs": {
                1: {"offset": 0.0},
                2: {"offset": 0.0},
            },
        }
    },
    "elements": {
        "pump": {
            "RF_inputs": {"port": ("oct1", 2)},
            # "RF_outputs": {"port": ("oct1", 1)},
            "intermediate_frequency": IF,
            "operations": {
                "cw": "const",
                "readout": "readout_pulse",
            },
            "digitalInputs": {
                "switch": {
                    "port": (con, 1),
                    "delay": 87,
                    "buffer": 15,
                },
            },
            # "time_of_flight": 24,
            # "smearing": 0,
        }
    },
    "octaves": {
        "oct1": {
            "RF_outputs": {
                2: {
                    "LO_frequency": LO,
                    "LO_source": "internal",  # can be external or internal. internal is the default
                    "output_mode": "always_on",  # can be: "always_on" / "always_off"/ "triggered" / "triggered_reversed". "always_off" is the default
                    "gain": 20,  # can be in the range [-20 : 0.5 : 20]dB
                }
            },
            "connectivity":"con1"
            
        }
    },
    "pulses": {
        "const": {
            "operation": "control",
            "length": 1000,
            "waveforms": {
                "I": "const_wf",
                "Q": "zero_wf",
            }#,
            # "digital_marker": "ON",
        },
        "readout_pulse": {
            "operation": "measurement",
            "length": 1000,
            "waveforms": {
                "I": "readout_wf",
                "Q": "zero_wf",
            },
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
            },
            "digital_marker": "ON",
        },
    },
    "waveforms": {
        "zero_wf": {
            "type": "constant",
            "sample": 0.0,
        },
        "const_wf": {
            "type": "constant",
            "sample": 0.3, #0~0.5V(1mV:-47dBm, 500mV:7dBm)
        },
        "readout_wf": {
            "type": "constant",
            "sample": 0.125,
        },
    },
    "digital_waveforms": {
        "ON": {"samples": [(1, 0)]},
        "OFF": {"samples": [(0, 0)]},
    },
    "integration_weights": {
        "cosine_weights": {
            "cosine": [(1.0, 1000)],
            "sine": [(0.0, 1000)],
        },
        "sine_weights": {
            "cosine": [(0.0, 1000)],
            "sine": [(1.0, 1000)],
        },
        "minus_sine_weights": {
            "cosine": [(0.0, 1000)],
            "sine": [(-1.0, 1000)],
        },
    },
}

