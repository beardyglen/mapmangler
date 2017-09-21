#!/usr/bin/env python
# Example: ./mapmangler.py 50.9376255 -1.3967372 17 100

import requests
import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
from PIL import ImageEnhance

#lat = 42.4833333
#lon = 1.4666667
zoomlevel = 15
edgethreshhold = 105

coordsfile = open('random_coords.txt','r')
counter = 1

while True:
	print("Processing image: "+str(counter))
	thisline = coordsfile.readline()
	coords = thisline.split(" ")
	
	lat = coords[0]
	lon = coords[1]
	
	satOutput=open('output_sat.png','wb')
	
	satOutput.write(requests.get('https://maps.googleapis.com/maps/api/staticmap?center='+str(lat)+','+str(lon)+'&zoom='+str(zoomlevel)+'&size=640x640&sensor=false&maptype=satellite').content)
	satOutput.close()
	
	cropImage = Image.open("output_sat.png")
	croppedImage = cropImage.crop((0,0,cropImage.size[0],cropImage.size[1]-20))
	croppedImage.save("output_sat.png")
	
	satImage = cv2.imread('output_sat.png')
	
	imgGrayscale = cv2.cvtColor(satImage,cv2.COLOR_BGR2GRAY)
	
	#imgGrayscale = cv2.bitwise_not(imgGrayscale)
	
	retval,threshold = cv2.threshold(imgGrayscale,edgethreshhold,255,0)
	
	edges = cv2.Canny(imgGrayscale,0,500)
	
	plt.imshow(edges,cmap = 'gray')
	plt.axis('off')
	plt.savefig('edges.png',bbox_inches='tight',pad_inches=0,dpi=300)
	
	contours, hierarchy = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	#print(str(len(contours))+" contours found.")
	
	#background = Image.new("RGB", (croppedImage.size[0],croppedImage.size[1]), (0,0,0) )
	#background.save("background.png")
	
	cvbg = cv2.imread('background.png')
	
	cv2.drawContours(cvbg,contours,-1,(0,0,255),-1)
	cv2.imwrite("output/"+str(counter)+".png",cvbg)
	counter += 1

coordsfile.close()
exit(0)
