# sparse.py
#
# Luke Sheneman, 2021
# sheneman@uidaho.edu
#
#
# Takes as input a single tiff-formated Z-stack that represents the sensing of 
# photons over time.  For every frame in the Z-stack, find the centroid of 
# every light sensing event (blob) and find the intensity "center of mass" moment
# to construct a Z-stack which only contains centroids.
#
# Also integrate the centroid Z-stack to produce a single frame integrated image.
# Perform a couple of denoising steps on the integrated image (wavelet-based and
# Gaussian blurring)
#

import cv2
import numpy as np
from skimage.restoration import (denoise_wavelet, estimate_sigma)
from skimage import img_as_ubyte
from scipy import ndimage as nd

from progressbar import progressbar

np.set_printoptions(threshold=np.inf)

# set up some paths
IMAGE_FILE = "./sparse.tif"

print("Reading Z-Stack Image...")
ret, images = cv2.imreadmulti(IMAGE_FILE, flags=cv2.IMREAD_GRAYSCALE)



new_images = images.copy()
new_images_out = images.copy()
integrated_image = np.zeros(images[0].shape, np.uint16)

print("Finding centroids...")
progressbar(0, len(images), prefix = 'Progress:', suffix = 'Complete', length = 50)
for i in range(len(images)):

	progressbar(i, len(images), prefix = 'Progress:', suffix = 'Complete', length = 50)

	img = images[i]
	new_img = np.zeros(img.shape, np.uint8)

	img = cv2.normalize(img,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)
	edged_img = cv2.Canny(img, 50, 100)

	# find contours for our masks
	contours,hierarchy = cv2.findContours(edged_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	if(len(contours)==0):
		new_images[i] = new_img
		continue

	ChildContour = hierarchy[0, :,2]
	WithoutChildContour = (ChildContour==-1).nonzero()[0]
	contours=[ contours[i] for i in WithoutChildContour]

	for c in contours:

		#x,y,w,h = cv2.boundingRect(c)

		# calculate moments for each contour
		M = cv2.moments(c)

		# calculate x,y coordinate of center
		if(M["m00"] > 0.0):
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])

			new_img[cY,cX] = 1

	new_images[i] = new_img
	new_images_out[i] = new_img * 255


print("")
print("Writing centroid output...")
cv2.imwritemulti("centroid.tif", new_images_out)

print("Integrating photons...")
integrated_arr = np.dstack(new_images)
integrated_image = np.sum(integrated_arr,axis=2,dtype=np.uint16)
#print(type(integrated_image))
#print(integrated_image.shape)


maxval = np.max(integrated_image)
integrated_image = integrated_image/maxval 
integrated_image = cv2.normalize(integrated_image,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)
#ret,thresh = cv2.threshold(integrated_image,100,255,cv2.THRESH_TOZERO)

wavelet_image = denoise_wavelet(integrated_image, multichannel=False, convert2ycbcr=False,
                           method='BayesShrink', mode='soft',
                           rescale_sigma=True) 
wavelet_image = img_as_ubyte(wavelet_image)

print("Writing integrated image output...")
cv2.imwrite("integrated.tif", integrated_image)
cv2.imwrite("wavelet_denoised_bayeshrink.tif", wavelet_image)

wavelet_image = denoise_wavelet(integrated_image, multichannel=False, convert2ycbcr=False,
                           method='VisuShrink', mode='soft',
                           rescale_sigma=True) 
wavelet_image = img_as_ubyte(wavelet_image)
cv2.imwrite("wavelet_denoised_visushrink.tif", wavelet_image)

denoised_image = nd.gaussian_filter(integrated_image, sigma=1.0)
print(type(denoised_image))
cv2.imwrite("denoised.tif", denoised_image)

print("")
print("Done.")

