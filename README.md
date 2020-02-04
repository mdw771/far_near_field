# far_near_field
Comparison between near-field holography and far-field ptychography

This code repo is used in the following publication(s):

- Du, M., Gursoy, D., & Jacobsen, C. (2019). Near, far, wherever you are: simulations on the dose efficiency of holographic and ptychographic coherent imaging. arXiv preprint arXiv:1908.06770. <url>https://arxiv.org/abs/1908.06770</url>

## Installation
The repository itself doesn't require installation, but you need to prepare your environment with all of its dependencies, represented by TensorFlow. Use the GPU-enabled version of TensorFlow from Anaconda is usually the most convenient approach:
```
conda install tensorflow-gpu
```
Use `pip install` to get other missing dependencies if any.

## Generating simulated data
Use `create_ptycho_data.py` and `create_fullfield_data.py` to create simulated data for ptychography and fullfield CDI, respectively. Make sure `grid_delta.npy` and `grid_beta.npy` is contained in `phantom_path` (e.g., `cell/ptychography/phantom`) (*the files are not uploaded yet; will do after my workstation is fixed*), and check all parameters are set correctly. Running the scripts creates an HDF5 file at `save_path` that contains a dataset called `exchange`. The array shape is `[n_angles, detector_size_y, detector_size_x]` for fullfield, and `[n_angles, n_spots_per_angle, detector_size_y, detector_size_x]` for ptychography.

## Adding Poisson noise
To add Poisson noise to the noise-free dataset generated in the previous step, use `create_noisy_data.py`. `n_ph_tx` specifies the number of photons *hitting the sample* (i.e., exclusing those hitting vacuum). `n_sample_pixel` gives the number of pixels in the sample's support (i.e., non-zero region). The script detect automatically whether the source dataset is ptychography or fullfield from the name of the directory.

## Ptychography reconstruction
Use `reconstruct_ptycho.py` for ptychography reconstruction. By specifying `n_ls`, the script can run reconstruction for a list of noise levels sequentially. The reconstruction function uses Gaussian (least square) loss function by default; to switch to Poisson loss function, uncomment the line of
```
loss = tf.reduce_mean(tf.abs(exiting_ls) ** 2 * poisson_multiplier - tf.abs(this_prj_batch[i]) ** 2 * poisson_multiplier * tf.log(tf.abs(exiting_ls) ** 2 * poisson_multiplier), name='loss')
```
and comment the original declaration of the loss function. Also, the line in `reconstruct_ptycho.py` reading
```
params['poisson_multiplier'] = n_ph_1 / 5e4
```
calculate the number of incident photons per pixel and the `5e4` is hard coded for cell. If you are using a different object, change it to the number of non-zero pixels.
