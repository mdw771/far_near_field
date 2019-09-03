from ptychography import reconstruct_ptychography
import numpy as np
import dxchange


params_2d_cell = {
    # 'fname': 'data_cell_phase.h5',
                    'fname': 'data_cell_phase.h5',
                    'theta_st': 0,
                    'theta_end': 0,
                    'theta_downsample': 1,
                    'n_epochs': 1000,
                    'obj_size': (325, 325, 1),
                    'alpha_d': 0,
                    'alpha_b': 0,
                    'gamma': 0,
                    'probe_size': (72, 72),
                    'learning_rate': 4e-3,
                    'center': 512,
                    'energy_ev': 5000,
                    'psize_cm': 1.e-7,
                    'batch_size': 1,
                    'n_batch_per_update': 1,
                    'output_folder': None,
                    'cpu_only': True,
                    'save_folder': 'cell/ptychography',
                    'phantom_path': 'cell/phantom',
                    'multiscale_level': 1,
                    'n_epoch_final_pass': None,
                    'save_intermediate': True,
                    'full_intermediate': True,
                    # 'initial_guess': [np.zeros([325, 325, 1]) + 0.032, np.zeros([325, 325, 1])],
                    'initial_guess': None,
                    'n_dp_batch': 20,
                    'probe_type': 'gaussian',
                    'probe_options': {'probe_mag_sigma': 6,
                                      'probe_phase_sigma': 6,
                                      'probe_phase_max': 0.5},
                    'forward_algorithm': 'fresnel',
                    'object_type': 'phase_only',
                    'probe_pos': [(y, x) for y in np.arange(33) * 10 for x in np.arange(34) * 10],
                    'finite_support_mask': None
                    }


params = params_2d_cell


# n_ls = ['nonoise', 'n1e9', 'n1e8', 'n1e7', 'n1e6', 'n1e5', 'n1e4']
n_ls = ['n4e8', 'n4e7', 'n4e6', 'n4e5', 'n4e4', 'n1.75e8', 'n1.75e7', 'n1.75e6']
# n_ls = [x + '_ref' for x in n_ls]

for n_ph in n_ls:
    if 'nonoise' in n_ph:
        params['fname'] = 'data_cell_phase.h5'
        params['poisson_multiplier'] = 2e8
    else:
        params['fname'] = 'data_cell_phase_{}.h5'.format(n_ph)
        if '_ref' in n_ph:
            n_ph_1 = float(n_ph[1:n_ph.find('_ref')])
        else:
            n_ph_1 = float(n_ph[1:])
        params['poisson_multiplier'] = n_ph_1 / 5e4
    params['output_folder'] = n_ph

    reconstruct_ptychography(fname=params['fname'],
                             probe_pos=params['probe_pos'],
                             probe_size=params['probe_size'],
                             theta_st=0,
                             theta_end=params['theta_end'],
                             theta_downsample=params['theta_downsample'],
                             obj_size=params['obj_size'],
                             n_epochs=params['n_epochs'],
                             crit_conv_rate=0.03,
                             max_nepochs=200,
                             alpha_d=params['alpha_d'],
                             alpha_b=params['alpha_b'],
                             gamma=params['gamma'],
                             learning_rate=params['learning_rate'],
                             output_folder=params['output_folder'],
                             minibatch_size=params['batch_size'],
                             save_intermediate=params['save_intermediate'],
                             full_intermediate=params['full_intermediate'],
                             energy_ev=params['energy_ev'],
                             psize_cm=params['psize_cm'],
                             cpu_only=params['cpu_only'],
                             save_path=params['save_folder'],
                             phantom_path=params['phantom_path'],
                             multiscale_level=params['multiscale_level'],
                             n_epoch_final_pass=params['n_epoch_final_pass'],
                             initial_guess=params['initial_guess'],
                             n_batch_per_update=params['n_batch_per_update'],
                             dynamic_rate=True,
                             probe_type=params['probe_type'],
                             probe_initial=None,
                             probe_learning_rate=1e-3,
                             pupil_function=None,
                             probe_circ_mask=None,
                             n_dp_batch=params['n_dp_batch'],
                             finite_support_mask=params['finite_support_mask'],
                             forward_algorithm=params['forward_algorithm'],
                             poisson_multiplier=params['poisson_multiplier'],
                             object_type=params['object_type'],
                             **params['probe_options'])
