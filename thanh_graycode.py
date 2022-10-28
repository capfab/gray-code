import math as mt
import numpy as np
import cv2 as cv
import scipy.misc as smp
import matplotlib.pyplot as plot
import array as arr
import math
import os
from PIL import Image, ImageDraw
import glob

# Path
path = "your_path/patterns"

def generateGrayarr(n):
    # base case
    if (n <= 0):
        return
    # 'arr' will store all generated codes
    arr = list()
    # start with one-bit pattern
    arr.append("0")
    arr.append("1")
    # Every iteration of this loop generates
    # 2*i codes from previously generated i codes.
    i = 2
    j = 0
    while(True):
        if i >= 1 << n:
            break
        # Enter the previously generated codes
        # again in arr[] in reverse order.
        # Nor arr[] has double number of codes.
        for j in range(i - 1, -1, -1):
            arr.append(arr[j])
        # append 0 to the first half
        for j in range(i):
            arr[j] = "0" + arr[j]
        # append 1 to the second half
        for j in range(i, 2 * i):
            arr[j] = "1" + arr[j]
        i = i << 1
    # prcontents of arr[]
    # for i in range(len(arr)):
    #     print(arr[i])
    return arr

# Driver Code
# Set initial parameters
im_h = 1080
im_w = 1920
# Number of bits
bit_no = 5
pat_max = 2**bit_no
# Minimum shift distance in pixel
shift_min = int(im_w/pat_max)

arr_gray = generateGrayarr(bit_no)

# Create a 1080x1920x3 black images
gray_pat_dict = {}
for k in range(bit_no):
    # calculate value
    value = np.zeros((im_h,im_w,3), dtype=np.uint8)
    gray_pat_dict[k] = value

# Paste Gray code array to every pixel column
for c in range(bit_no):
    j = 0
    i = 0
    while i < len(gray_pat_dict[c][0,:]):
        left_pos = i
        right_pos = (j+1)*shift_min
        # print(left_pos)
        # print(right_pos)
        gray_pat_dict[c][:,left_pos:right_pos,0] = 255*int(arr_gray[j][c])
        gray_pat_dict[c][:,left_pos:right_pos,1] = 255*int(arr_gray[j][c])
        gray_pat_dict[c][:,left_pos:right_pos,2] = 255*int(arr_gray[j][c])
        j = j+1
        i = i+shift_min
        if j == len(arr_gray):
            j = 0
            continue
    img_path = path + "/pat_gray" + str(c) + '.jpg'
    cv.imwrite(img_path, gray_pat_dict[c])
    # cv.imshow("test", gray_pat_dict[c])
    # cv.waitKey()

# Create GIF
fp_in = "F:/web/codes/Gray-code/patterns/pat_gray*.jpg"
fp_out = "F:/web/codes/Gray-code/graphics/Gray_code.gif"
img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))] 
img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=3000/bit_no, loop=0)