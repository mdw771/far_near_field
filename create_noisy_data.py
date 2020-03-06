import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
import dxchange
from tqdm import trange
import time

np.random.seed(int(time.time()))

# src_fname = 'cone_256_foam_ptycho/data_cone_256_foam_1nm.h5'
src_fname = 'cell/nf_ptychography/data_cell_phase.h5'
# src_fname = 'cell/ptychography_coarse/data_cell_phase.h5'
# src_fname = 'cell/nf_ptychography_coarse/data_cell_phase.h5'
# src_fname = 'cell/ptychography_fine/data_cell_phase.h5'
grid_delta = np.load('cell/ptychography/phantom/grid_delta.npy')
grid_size = [325, 325]
n_sample_pixel = np.count_nonzero(grid_delta > 1e-10)
print(n_sample_pixel)

# src_fname = 'cone_256_filled_ptycho/data_cone_256_1nm_marc.h5'
# dest_fname = 'cone_256_filled_ptycho/data_cone_256_1nm_marc_n2e3_2.h5'

for n_ph_tx in ['1e4', '4e4', '1e5', '4e5', '1e6', '1.75e6', '4e6', '1e7', '1.75e7', '4e7', '1e8', '1.75e8', '4e8', '1e9']:
    for postfix in ['', '_ref']:

        n_ph = float(n_ph_tx) / n_sample_pixel
        # dest_fname = 'cone_256_foam_ptycho/data_cone_256_foam_1nm_n{}_temp.h5'.format(n_ph_tx)
        dest_fname = os.path.join(os.path.dirname(src_fname), os.path.splitext(os.path.basename(src_fname))[0] + '_n{}{}.h5'.format(n_ph_tx, postfix))
        # dest_fname = 'cell/ptychography/data_cell_phase_n4e8.h5'


        is_ptycho = False
        if 'ptycho' in src_fname and 'nf' not in src_fname:
            is_ptycho = True

        o = h5py.File(src_fname, 'r')['exchange/data']
        file_new = h5py.File(dest_fname, 'w')
        grp = file_new.create_group('exchange')
        n = grp.create_dataset('data', dtype='complex64', shape=o.shape)
        snr_ls = []
        print('Dataset shape:')
        print(o.shape)

        # if is_ptycho:
        #     sigma = 6
        #     n_ph *= (n_sample_pixel / (o.shape[1] * 3.14 * sigma ** 2)) # photon per diffraction spot

        if is_ptycho:

            # total photons received by sample
            n_ex = n_ph * n_sample_pixel
            # total photons per image
            print('Far-field ptychography data')
            n_ex *= (np.prod(grid_size) / n_sample_pixel)
            print('CHECK IF THIS IS THE CORRECT SCAN SIZE AND SAMPLE AREA:')
            print(grid_size, np.prod(grid_size), n_sample_pixel)
            time.sleep(3)
            # total photons per spot
            n_ex /= o.shape[1]
            print(o.shape[1])

            for i in trange(o.shape[0]):
                for j in range(o.shape[1]):
                    prj_o = o[i, j]
                    prj_o_inten = np.abs(prj_o) ** 2

                    spot_integral = np.sum(prj_o_inten)
                    multiplier = n_ex / spot_integral
                    # scale intensity to match expected photons per spot
                    pro_o_inten_scaled = prj_o_inten * multiplier
                    # dc_intensity = prj_o_inten[int(o.shape[-2] / 2), int(o.shape[-1] / 2)]
                    # prj_o_inten_norm = prj_o_inten / dc_intensity
                    # print(n_ph)
                    prj_o_inten_noisy = np.random.poisson(pro_o_inten_scaled)
                    prj_o_inten_noisy = prj_o_inten_noisy / multiplier
                    noise = prj_o_inten_noisy - prj_o_inten
                    snr = np.var(prj_o_inten) / np.var(noise)
                    snr_ls.append(snr)
                    data = np.sqrt(prj_o_inten_noisy)
                    n[i, j] = data.astype('complex64')

        elif 'nf_ptycho' in src_fname:

            print('Near-field ptychography data')
            time.sleep(3)
            print(o.shape)
            n_ph_per_img = n_ph / o.shape[1]
            for i in range(o.shape[0]):
                for j in trange(o.shape[1]):
                    prj_o = o[i, j]
                    prj_o_inten = np.abs(prj_o) ** 2
                    prj_o_inten_noisy = np.random.poisson(prj_o_inten * n_ph_per_img)
                    # noise = prj_o_inten_noisy - prj_o_inten
                    # print(np.var(noise))
                    prj_o_inten_noisy = prj_o_inten_noisy / n_ph_per_img
                    noise = prj_o_inten_noisy - prj_o_inten
                    snr = np.var(prj_o_inten) / np.var(noise)
                    snr_ls.append(snr)
                    data = np.sqrt(prj_o_inten_noisy)
                    n[i, j] = data.astype('complex64')

        else:
            print('Holography data')
            time.sleep(3)
            for i in trange(o.shape[0]):
                prj_o = o[i]
                prj_o_inten = np.abs(prj_o) ** 2
                prj_o_inten_noisy = np.random.poisson(prj_o_inten * n_ph)
                # noise = prj_o_inten_noisy - prj_o_inten
                # print(np.var(noise))
                prj_o_inten_noisy = prj_o_inten_noisy / n_ph
                noise = prj_o_inten_noisy - prj_o_inten
                snr = np.var(prj_o_inten) / np.var(noise)
                snr_ls.append(snr)
                data = np.sqrt(prj_o_inten_noisy)
                n[i] = data.astype('complex64')

        print('Average SNR is {}.'.format(np.mean(snr_ls)))

        dxchange.write_tiff(abs(n[0]), os.path.join(os.path.dirname(dest_fname), 'n{}{}'.format(n_ph_tx, postfix)), dtype='float32', overwrite=True)


        # ------- based on SNR -------
        # snr = 10

        # for i in tqdm(range(o.shape[0])):
        # for i in tqdm(range(1)):
        #     prj_o = o[i]
        #     prj_o_inten = np.abs(prj_o) ** 2
        #     var_signal = np.var(prj_o_inten)
        #     var_noise = var_signal / snr

            # noise = np.random.poisson(prj_o_inten * (var_noise / np.mean(prj_o_inten)) * 1e10) / 1e5
            # noise = noise * np.sqrt(var_noise / np.var(noise))
            # noise -= np.mean(noise)
            # prj_n_inten = prj_o_inten + noise
            # prj_n = prj_o * np.sqrt(prj_n_inten / prj_o_inten)
            #
            # n[i] = prj_n
