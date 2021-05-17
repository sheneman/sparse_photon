#
# wavelet2.py
#
# Luke Sheneman, 2021
# sheneman@uidaho.edu
#
# Build a montage of denoised sparse-photon images of target object which is a 
# matrix of input images vs. denoising algorithms.  x-axis is the denoising
# algorithm, y-axis is the integrated input images.
#
# Takes as input a directory within which is nothing but the input images as 
# tif images.
#
# Outputs individual images into an output folder and also constructs a single
# output matrix called "montage.tif"
#

import cv2
import numpy as np
import os
from skimage.restoration import (denoise_wavelet, denoise_tv_chambolle, denoise_bilateral, estimate_sigma, richardson_lucy)
from skimage import img_as_ubyte
from scipy import ndimage as nd
from scipy.signal import convolve2d as conv2

np.set_printoptions(threshold=np.inf)

# set up some paths
IMAGE_DIR = "./inputs"
OUT_DIR   = "./out2"

WIDTH  = 85
HEIGHT = 85

def post_process(img):


	# median blur
	img = cv2.medianBlur(img,3)

	# gaussian blur
	img = cv2.GaussianBlur(img,(3,3),cv2.BORDER_DEFAULT)

	# change dynamic range
	minval  = np.min(img)
	maxval  = np.max(img)
	meanval = np.mean(img)
	
	new_min = meanval * 10.0

	offset = (new_min - minval)
	img = img + offset
	img = img * 1.4
	
	# add color (fire)


	img = cv2.normalize(img,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)

	return(img)


def resize(img):
	w,h = img.shape
	x1 = int(w/2-WIDTH/2)
	y1 = int(h/2-HEIGHT/2)
	x2 = x1 + WIDTH
	y2 = y1 + HEIGHT

	res = img[y1:y2,x1:x2]

	return(res)
	
files = sorted(os.listdir(IMAGE_DIR))
montage = np.zeros((len(files)*HEIGHT,6*WIDTH), np.uint8)
print(montage.shape)

y = 0
for file in files:
	print(file)
	x = 0
	fullpath = os.path.join(IMAGE_DIR, file)

	image = cv2.imread(fullpath,flags=cv2.IMREAD_UNCHANGED)
	image = resize(image)

	integrated_image = cv2.normalize(image,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)
	print(y)
	print(y+HEIGHT)
	print(x)
	print(x+WIDTH)
	montage[y:y+HEIGHT,x:x+WIDTH] = integrated_image
	x += WIDTH
	
	
	# BayesShrink
	wavelet_image = denoise_wavelet(integrated_image, multichannel=False, convert2ycbcr=False,
				   method='BayesShrink', mode='soft',
				   rescale_sigma=True) 
	wavelet_image = img_as_ubyte(wavelet_image)
	wavelet_image = post_process(wavelet_image)
	new_filename = file + "_bayesshrink.tif"
	outpath = os.path.join(OUT_DIR, new_filename)
	cv2.imwrite(outpath, wavelet_image)
	montage[y:y+HEIGHT,x:x+WIDTH] = wavelet_image
	x += WIDTH

	# VisuShrink	
	wavelet_image = denoise_wavelet(integrated_image, multichannel=False, convert2ycbcr=False,
				   method='VisuShrink', mode='soft',
				   rescale_sigma=True) 
	wavelet_image = img_as_ubyte(wavelet_image)
	wavelet_image = post_process(wavelet_image)
	new_filename = file + "_visushrink.tif"
	outpath = os.path.join(OUT_DIR, new_filename)
	cv2.imwrite(outpath, wavelet_image)
	montage[y:y+HEIGHT,x:x+WIDTH] = wavelet_image
	x+=WIDTH


	# Bilateral Filter
	denoised_image = denoise_bilateral(integrated_image, sigma_spatial=3)
	denoised_image = cv2.normalize(denoised_image,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)
	denoised_image = post_process(denoised_image)
	new_filename = file + "_bilateral.tif"
	outpath = os.path.join(OUT_DIR, new_filename)
	cv2.imwrite(outpath, denoised_image)
	montage[y:y+HEIGHT,x:x+WIDTH] = denoised_image
	x+=WIDTH



	# TV Chambolle
	denoised_image = denoise_tv_chambolle(integrated_image)
	denoised_image = cv2.normalize(denoised_image,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)
	denoised_image = post_process(denoised_image)
	new_filename = file + "_chambolle.tif"
	outpath = os.path.join(OUT_DIR, new_filename)
	cv2.imwrite(outpath, denoised_image)
	montage[y:y+HEIGHT,x:x+WIDTH] = denoised_image
	x+=WIDTH


	# Fast NL Means
	denoised_image = cv2.fastNlMeansDenoising(integrated_image,128,7,21)
	denoised_image = cv2.normalize(denoised_image,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)
	denoised_image = post_process(denoised_image)
	new_filename = file + "_fast_NL_means.tif"
	outpath = os.path.join(OUT_DIR, new_filename)
	cv2.imwrite(outpath, denoised_image)
	montage[y:y+HEIGHT,x:x+WIDTH] = denoised_image
	x+=WIDTH

	y += HEIGHT


outpath = os.path.join(OUT_DIR, "montage.tif")
cv2.imwrite(outpath, montage)

print("Done.")
