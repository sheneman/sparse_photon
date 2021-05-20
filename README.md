# Sparse Photon Image Tools
This collection of tools processes imags data derived from sparse photon light-sheet microscopy.

## Requirements:
Python 3 and all python packages listed in the file "requirements.txt"

#################################################################################################

## sparse.py
Takes as input a single tiff-formated Z-stack that represents the sensing of
photons over time.  For every frame in the Z-stack, find the centroid of
every light sensing event (blob) and find the intensity "center of mass" moment
to construct a Z-stack which only contains centroids.

Also integrate the centroid Z-stack to produce a single frame integrated image.
Perform a couple of denoising steps on the integrated image (wavelet-based and
Gaussian blurring)

### Input
"sparse.tif" : sparse.py expects to find a tiff stack file called "sparse.tif" 
  in the current working directory

### Output
"centroid.tif" : sparse.py will output a new tiff Z-stack file called "centroid.tif" which contains
  a time series of points representing the "center of mass" of the light detected

"integrated.tif" :  sparse.py will output a new single-frame image represnting the integration of 
  points over time from the centroid Z-stack
  
"wavelet_denoised_bayesshrink.tif" :  A denoised version of the integrated image using the 
  Bayesian wavelet-based denoising method known as BayesShrink

"wavelet_denoised_visushrink.tif" : A denoised version of the integrated image using the 
  wavelet-based denoising method known as VisuShrink
  
################################################################################################
  
## wavelet.py
Denoises the given single-frame input tif that represents the integrated stack of centroid pixels

### Input
Set the variable *IMAGE_FILE* to point to the path of the single-frame input tif

### Output
"wavelet_denoised_bayesshrink.tif" :  A denoised version of the integrated image using the 
  Bayesian wavelet-based denoising method known as BayesShrink

"wavelet_denoised_visushrink.tif" : A denoised version of the integrated image using the 
  wavelet-based denoising method known as VisuShrink
  
"denoised_gaussian_filter_sigma_0.25.tif" : denoised with a simple Gaussian blur filter with sigma=0.25
"denoised_gaussian_filter_sigma_0.50.tif" : denoised with a simple Gaussian blur filter with sigma=0.50
"denoised_gaussian_filter_sigma_0.75.tif" : denoised with a simple Gaussian blur filter with sigma=0.75
"denoised_gaussian_filter_sigma_1.0.tif"  : denoised with a simple Gaussian blur filter with sigma=1.00

"denoised_bilateral.tif" : denoised with the bilateral filter

"denoised_tv_chambolle.tif" : denoised with the Total Variabtion Chambolle method

"denoised_fastNlMeanstif" : image denoised with the fast non-local means algorithm
