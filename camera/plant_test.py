from plantcv import plantcv as pcv
import cv2
import numpy as np

plant1loc = "C:\\Users\\2000c\\OneDrive\\Documents\\College\\FALL_2022\\CSCE_462\\Project\\plant1.jpg"
plant2loc = "C:\\Users\\2000c\\OneDrive\\Documents\\College\\Fall_2022\\CSCE_462\\Project\\plant2.jpg"
plant1_o = cv2.imread(plant1loc)
plant2_o = cv2.imread(plant2loc)

pcv.params.debug = "print"

# Isolate plant in first image
y_channel1 = pcv.rgb2gray_cmyk(rgb_img=plant1_o, channel='Y')
m_channel1 = pcv.rgb2gray_cmyk(rgb_img=plant1_o, channel='M')
plant1 = cv2.subtract(y_channel1, m_channel1)
plant1 = pcv.closing(gray_img=plant1)
plant1 = pcv.erode(gray_img=plant1, ksize=15, i=10)
plant1 = pcv.closing(gray_img=plant1)
mask1 = cv2.threshold(plant1, 35, 255, cv2.THRESH_BINARY)[1]
mask1 = pcv.fill_holes(bin_img=mask1)
plant1 = pcv.apply_mask(img=plant1_o, mask=mask1, mask_color='white')
plant1 = pcv.erode(gray_img=plant1, ksize=15, i=10)

# Isolate plant in second image
y_channel2 = pcv.rgb2gray_cmyk(rgb_img=plant2_o, channel='Y')
m_channel2 = pcv.rgb2gray_cmyk(rgb_img=plant2_o, channel='M')
plant2 = cv2.subtract(y_channel2, m_channel2)
plant2 = pcv.closing(gray_img=plant2)
plant2 = pcv.erode(gray_img=plant2, ksize=15, i=10)
plant2 = pcv.closing(gray_img=plant2)
mask2 = cv2.threshold(plant2, 35, 255, cv2.THRESH_BINARY)[1]
mask2 = pcv.fill_holes(bin_img=mask2)
plant2 = pcv.apply_mask(img=plant2_o, mask=mask2, mask_color='white')
plant2 = pcv.erode(gray_img=plant2, ksize=15, i=10)

# Take difference of both plants
plantdifference = cv2.subtract(plant1, plant2)
plantdifference = pcv.erode(gray_img=plantdifference, ksize=10, i=10)

# Remove white background noise from difference image
th = 200 # defines the value below which a pixel is considered "white"
white_pixels = np.where(
    (plantdifference[:, :, 0] > th) & 
    (plantdifference[:, :, 1] > th) & 
    (plantdifference[:, :, 2] > th)
)
# set those pixels to black
plantdifference[white_pixels] = [0, 0, 0]

cv2.imwrite("C:\\Users\\2000c\\OneDrive\\Documents\\College\\Fall_2022\\CSCE_462\\Project\\difference1.jpg" , plant1)
cv2.imwrite("C:\\Users\\2000c\\OneDrive\\Documents\\College\\Fall_2022\\CSCE_462\\Project\\difference2.jpg" , plant2)
cv2.imwrite("C:\\Users\\2000c\\OneDrive\\Documents\\College\\Fall_2022\\CSCE_462\\Project\\difference.jpg" , plantdifference)

cv2.waitKey(0)
cv2.destroyAllWindows()