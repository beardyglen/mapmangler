#!/usr/bin/env python
# Example: ./mapmangler.py 50.9376255 -1.3967372 17 100

import requests
import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
from PIL import ImageEnhance

if len(sys.argv) != 5:
	print("Usage: "+sys.argv[0]+" [lat] [lon] [zoom] [threshhold]")
	exit(1)

try:
	lat = float(sys.argv[1])
	lon = float(sys.argv[2])
	zoomlevel = int(sys.argv[3])
	edgethreshhold = int(sys.argv[4])
except:
	print("One or both of your lat/lon values are weird.")



if (isinstance(lat, float) != True) or (isinstance(lon, float) != True):
	print("You need to use floats for the lat/lon values, you plum.")
	exit(1)
	
try:	
	satOutput=open('output_sat.png','wb')
	mapOutput=open('output_map.png','wb')
except:
	print("Couldn't open file for writing.")
	exit(1)

try:
	satOutput.write(requests.get('https://maps.googleapis.com/maps/api/staticmap?center='+str(lat)+','+str(lon)+'&zoom='+str(zoomlevel)+'&size=640x640&sensor=false&maptype=satellite').content)
	satOutput.close()
	#mapOutput.write(requests.get('https://maps.googleapis.com/maps/api/staticmap?center='+str(lat)+','+str(lon)+'&zoom='+str(zoomlevel)+'&size=640x640&sensor=false&maptype=static').content)
	#mapOutput.close()
except:
	print("Something terrible happened.")
	exit(1)

cropImage = Image.open("output_sat.png")
croppedImage = cropImage.crop((0,0,cropImage.size[0],cropImage.size[1]-20))
croppedImage.save("output_sat.png")


try:
	#mapImage = cv2.imread('output_map.png')
	satImage = cv2.imread('output_sat.png')
except:
	print("Couldn't open the map image.")
	exit(1)

 

##contrast = ImageEnhance.Contrast(satImage)
##contrast.enhance(2).show()

# TESTY TESTINGTONS FROM HERE ON

#satImage = cv2.imread('input.png')

imgGrayscale = cv2.cvtColor(satImage,cv2.COLOR_BGR2GRAY)

#imgGrayscale = cv2.bitwise_not(imgGrayscale)

retval,threshold = cv2.threshold(imgGrayscale,edgethreshhold,255,0)

edges = cv2.Canny(imgGrayscale,0,500)

plt.imshow(edges,cmap = 'gray')
plt.axis('off')
plt.savefig('edges.png',bbox_inches='tight',pad_inches=0,dpi=300)

#edgePic = cv2.imread('edges.png')
#cv2.imshow("Map With Edges Added ("+str(lat)+','+str(lon)+")", edgePic)
#cv2.waitKey()


#edgePicGrayscale = cv2.cvtColor(edgePic,cv2.COLOR_BGR2GRAY)
#retval,threshold = cv2.threshold(edgePicGrayscale,80,255,0)

contours, hierarchy = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

print(str(len(contours))+" contours found.")

background = Image.new("RGB", (croppedImage.size[0],croppedImage.size[1]), (0,0,0) )
background.save("background.png")

cvbg = cv2.imread('background.png')

cv2.drawContours(cvbg,contours,-1,(0,0,255),-1)
#cv2.imshow("Map With Contours Added ("+str(lat)+','+str(lon)+")", cvbg)
cv2.imwrite("1.png",cvbg)
#cv2.waitKey()

exit(0)
