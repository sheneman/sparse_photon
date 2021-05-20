# Sparse Photon Image Tools
This collection of tools processes imags data derived from sparse photon light-sheet microscopy.

## Requirements:
Python 3
Python libraries listed in the file "requirements.txt"

## sparse.py
Takes as input a single tiff-formated Z-stack that represents the sensing of
photons over time.  For every frame in the Z-stack, find the centroid of
every light sensing event (blob) and find the intensity "center of mass" moment
to construct a Z-stack which only contains centroids.

Also integrate the centroid Z-stack to produce a single frame integrated image.
Perform a couple of denoising steps on the integrated image (wavelet-based and
Gaussian blurring)

# Input
"sparse.tif" : sparse.py expects to find a tiff stack file called "sparse.tif" 
  in the current working directory

# Output
"centroid.tif" : sparse.py will output a new tiff Z-stack file called "centroid.tif" which contains
  a time series of points representing the "center of mass" of the light detected

"integrated.tif" :  sparse.py will output a new single-frame image represnting the integration of 
  points over time from the centroid Z-stack
  
"wavelet_denoised_bayesshrink.tif" :  A denoised version of the integrated image using the 
  Bayesian wavelet-based denoising method known as BayesShrink

"wavelet_denoised_visushrink.tif" : A denoised version of the integrated image using the 
  wavelet-based denoising method known as VisuShrink
  
