import numpy as np
import cv2
import threading
import tkinter
from tkinter import ttk

class gui(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.color = 'RED' 
		self.start()

	def callback(self):
		self.root.quit()

	def run(self):
		self.root = tkinter.Tk()
		self.root.protocol('WM_DELETE_WINDOW', self.callback)

		title = tkinter.Label(self.root,text = 'Pick a Color')

		# Creates the buttons
		red_button = tkinter.Button(self.root, text="RED", bg="red",command = self.set_red, width = 6)
		green_button = tkinter.Button(self.root, text="GREEN", bg="green",command = self.set_green, width = 6)
		blue_button = tkinter.Button(self.root, text="BLUE", bg="blue",command = self.set_blue, width = 6)
		yellow_button = tkinter.Button(self.root, text="YELLOW", bg="yellow",command = self.set_yellow, width = 6)
		pink_button = tkinter.Button(self.root, text="PINK", bg="pink",command = self.set_pink, width = 6)
		custom_button = tkinter.Button(self.root, text="CUSTOM", bg="gray",command = self.set_custom, width = 6)

		# Formats buttons
		custom_button.pack()
		pink_button.pack()
		yellow_button.pack()
		blue_button.pack()
		green_button.pack()
		red_button.pack()

		# Mainloop
		red_button.mainloop()
	
	def __str__(self):
		return self.color

	def set_red(self):
		self.color = 'RED'

	def set_green(self):
		self.color = 'GREEN'

	def set_blue(self):
		self.color = 'BLUE'

	def set_yellow(self):
		self.color = 'YELLOW'

	def set_pink(self):
		self.color = 'PINK'

	def set_custom(self):
		self.color = 'CUSTOM'

menu = gui()

# urls
url = 'http://192.168.1.11:8080/video'
cap = cv2.VideoCapture(0)

# Colors
red_lower = np.array([0, 100,100])
red_upper = np.array([20,255,255])

green_lower = np.array([35,20,20])
green_upper = np.array([90,255,255])

blue_lower = np.array([50, 50, 50])
blue_upper = np.array([150, 255, 255])

yellow_lower = np.array([15, 100, 100])
yellow_upper = np.array([30, 255, 255])

pink_lower = np.array([150, 100, 100])
pink_upper = np.array([179, 255, 255])

def nothing(var):
	pass

#Creates window to customize the HSV range
cv2.namedWindow("Custom HSV Range")
cv2.resizeWindow("HSV Range", 800, 320)
cv2.createTrackbar("H-low", "HSV Range", 0, 179, nothing)
cv2.createTrackbar("S-low","HSV Range", 0, 255, nothing)
cv2.createTrackbar("V-low", "HSV Range", 0, 255, nothing)
cv2.createTrackbar("H-up", "HSV Range", 0, 179, nothing)
cv2.createTrackbar("S-up","HSV Range", 0, 255, nothing)
cv2.createTrackbar("V-up", "HSV Range", 0, 255, nothing)

while True:
	ret, frame = cap.read()
	frame = cv2.flip(frame, 1)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	if str(menu) == 'RED':
		mask = cv2.inRange(hsv, red_lower, red_upper)
	elif str(menu) == 'GREEN':
		mask = cv2.inRange(hsv, green_lower, green_upper)
	elif str(menu) == 'BLUE':
		mask = cv2.inRange(hsv, blue_lower, blue_upper)
	elif str(menu) == 'YELLOW':
		mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
	elif str(menu) == 'PINK':
		mask = cv2.inRange(hsv, pink_lower, pink_upper)
	elif str(menu) == 'CUSTOM':
		custom_lower = np.array([cv2.getTrackbarPos("H-low", "HSV Range"), cv2.getTrackbarPos("S-low", "HSV Range"), cv2.getTrackbarPos("V-low", "HSV Range")])
		custom_upper = np.array([cv2.getTrackbarPos("H-up", "HSV Range"), cv2.getTrackbarPos("S-up", "HSV Range"), cv2.getTrackbarPos("V-up", "HSV Range")])
		mask = cv2.inRange(hsv, custom_lower, custom_upper)
	else:
		mask = cv2.inRange(hsv, red_lower, red_upper)

	res = cv2.bitwise_and(frame, frame, mask = mask)

	contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	cv2.drawContours(frame, contours, -1, (0,255,0), 3)

	cv2.imshow("Frame", frame)
	cv2.imshow("Res", res)

	key = cv2.waitKey(1)
	if key == 27:
		break

cap.release()
cv2.destroyAllWindows()

