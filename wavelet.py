# wavelet.py
#
# Luke Sheneman, 2021
# sheneman@uidaho.edu
#
# Takes a single integrated input image in tif format and outputs
# a series of denoised output images using different denoising algorithms
# including: BayesShrink (wavelet), VisuShrink (wavelet), Gaussian filters,
# bilateral filter, total variation Chambolle, and non-local means.
#

import cv2
import numpy as np
from skimage.restoration import (denoise_wavelet, denoise_tv_chambolle, denoise_bilateral, estimate_sigma, richardson_lucy)
from skimage import img_as_ubyte
from scipy import ndimage as nd
from scipy.signal import convolve2d as conv2

from progressbar import progressbar

np.set_printoptions(threshold=np.inf)

# set up some paths
IMAGE_FILE = "./inputs/frame250.tif"
image = cv2.imread(IMAGE_FILE,flags=cv2.IMREAD_UNCHANGED)

integrated_image = cv2.normalize(image,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)

wavelet_image = denoise_wavelet(integrated_image, multichannel=False, convert2ycbcr=False,
                           method='BayesShrink', mode='soft',
                           rescale_sigma=True) 
wavelet_image = img_as_ubyte(wavelet_image)
cv2.imwrite("./out/wavelet_denoised_bayeshrink.tif", wavelet_image)


wavelet_image = denoise_wavelet(integrated_image, multichannel=False, convert2ycbcr=False,
                           method='VisuShrink', mode='soft',
                           rescale_sigma=True) 
wavelet_image = img_as_ubyte(wavelet_image)
cv2.imwrite("./out/wavelet_denoised_visushrink.tif", wavelet_image)



denoised_image = nd.gaussian_filter(integrated_image, sigma=0.25)
cv2.imwrite("./out/denoised_gaussian_filter_sigma_0.25.tif", denoised_image)

denoised_image = nd.gaussian_filter(integrated_image, sigma=0.5)
cv2.imwrite("./out/denoised_gaussian_filter_sigma_0.5.tif", denoised_image)

denoised_image = nd.gaussian_filter(integrated_image, sigma=0.75)
cv2.imwrite("./out/denoised_gaussian_filter_sigma_0.75.tif", denoised_image)

denoised_image = nd.gaussian_filter(integrated_image, sigma=1.0)
cv2.imwrite("./out/denoised_gaussian_filter_sigma_1.0.tif", denoised_image)



denoised_image = denoise_bilateral(integrated_image, sigma_spatial=3)
denoised_image = cv2.normalize(denoised_image,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)
cv2.imwrite("./out/denoised_bilateral.tif", denoised_image)


denoised_image = denoise_tv_chambolle(integrated_image)
denoised_image = cv2.normalize(denoised_image,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)
cv2.imwrite("./out/denoised_tv_chambolle.tif", denoised_image)


denoised_image = cv2.fastNlMeansDenoising(integrated_image,128,7,21)
denoised_image = cv2.normalize(denoised_image,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)
cv2.imwrite("./out/denoised_fastNlMeans.tif", denoised_image)


print("Done.")
exit(0)



#print(integrated_image)
print(type(integrated_image[0][0]))
psf = np.ones((5, 5)) / 25
#integrated_image =  np.float32(integrated_image / 255.0)
integrated_image = cv2.normalize(integrated_image,None,0,1,cv2.NORM_MINMAX,cv2.CV_32F)
print(integrated_image)

print(type(integrated_image[0][0]))
astro = conv2(integrated_image, psf, 'same')
print(astro)
denoised_image = richardson_lucy(astro, psf)
denoised_image = cv2.normalize(denoised_image,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)
cv2.imwrite("./out/richardson_lucy.tif", denoised_image)



print("")
print("Done.")

