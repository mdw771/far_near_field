from fullfield import reconstruct_fullfield
import numpy as np
from constants import *
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"


params_2d_cell = {
               'fname': 'data_cell_phase.h5',
                # 'fname': 'data_cell_phase_{}.h5'.format(nph),
               'theta_st': 0,
               'theta_end': 0,
               'n_epochs': 200,
               'alpha_d': 0,
               'alpha_b': 0,
               'gamma': 0,
               # 'learning_rate': 4e-3,
               'learning_rate': 4e-3,
               'center': 128,
               'energy_ev': 5000,
               'psize_cm': 1.e-7,
               'minibatch_size': 1,
               'theta_downsample': None,
               'n_epochs_mask_release': 1000,
               'shrink_cycle': None,
               'free_prop_cm': 0.00040322580645161285,
               'n_batch_per_update': 1,
               'output_folder': None,
               'cpu_only': True,
               'save_path': 'cell/fullfield',
               'phantom_path': 'cell/fullfied/phantom',
               'multiscale_level': 1,
               'n_epoch_final_pass': None,
               'save_intermediate': True,
               'full_intermediate': True,
               'initial_guess': None,
               'probe_type': 'plane',
               'forward_algorithm': 'fresnel',
               'object_type': 'phase_only',
               'poisson_multiplier': 2e6,
               'kwargs': {'probe_mag_sigma': 100,
                               'probe_phase_sigma': 100,
                               'probe_phase_max': 0.5},
             }


params = params_2d_cell

# n_ls = ['nonoise', 'n1e9', 'n1e8', 'n1e7', 'n1e6', 'n1e5', 'n1e4']
n_ls = ['n4e8', 'n4e7', 'n4e6', 'n4e5', 'n4e4', 'n1.75e8', 'n1.75e7', 'n1.75e6']
# n_ls = [x + '_ref' for x in n_ls]


for n_ph in n_ls:
    if 'nonoise' in n_ph:
        params['fname'] = 'data_cell_phase.h5'
        params['poisson_multiplier'] = 2e6
    else:
        params['fname'] = 'data_cell_phase_{}.h5'.format(n_ph)
        if '_ref' in n_ph:
            n_ph_1 = float(n_ph[1:n_ph.find('_ref')])
        else:
            n_ph_1 = float(n_ph[1:])
        params['poisson_multiplier'] = n_ph_1 / 5e4
    params['output_folder'] = n_ph

    reconstruct_fullfield(**params)
