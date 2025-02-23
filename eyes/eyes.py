from camera.track import setup_camera, track_loop
import numpy as np
from threading import Thread
from setup import *
# from camera.voice import voice

# Generate one frame of imagery
def frame():

	global startX, startY, destX, destY, curX, curY
	global startXR, startYR, destXR, destYR, curXR, curYR
	global moveDuration, holdDuration, startTime, isMoving
	global moveDurationR, holdDurationR, startTimeR, isMovingR
	global frames
	global leftIris, rightIris
	global pupilMinPts, pupilMaxPts, irisPts, irisZ
	global leftEye, rightEye
	global prevPupilScale
	global irisRegenThreshold
	global trackingPos
	global trackingPosR

	DISPLAY.loop_running()

	now = time.time()
	dt  = now - startTime

	frames += 1

	# Autonomous eye position
	# if freeze_flag:
	# if isMoving == True:
	# 	if dt <= moveDuration:
	# 		scale        = (now - startTime) / moveDuration
	# 		# Ease in/out curve: 3*t^2-2*t^3
	# 		scale = 3.0 * scale * scale - 2.0 * scale * scale * scale
	# 		curX         = startX + (destX - startX) * scale
	# 		curY         = startY + (destY - startY) * scale
	# 	else:
	# 		startX       = destX
	# 		startY       = destY
	# 		curX         = destX
	# 		curY         = destY
	# 		holdDuration = 0.1
	# 		startTime    = now
	# 		isMoving     = False
	# else:
	# 	if dt >= holdDuration:
	# 		destX        = np.interp(eye_coords.x, [0, 1280], [-30, 30])
	# 		destY        = -np.interp(eye_coords.y, [0, 720], [-30, 30])
	# 		moveDuration = 0.5
	# 		startTime    = now
	# 		isMoving     = True
	speed = 0.001
	curX += (np.interp(eye_coords.x, [0, 1280], [-30, 30]) - curX) * (1 - np.exp(- dt * speed))
	curY += (-np.interp(eye_coords.y, [0, 720], [-30, 30]) - curY) * (1 - np.exp(- dt * speed))

	convergence = 2.0

	rightIris.rotateToX(curY)
	rightIris.rotateToY(curX - convergence)
	rightIris.draw()
	rightEye.rotateToX(curY)
	rightEye.rotateToY(curX - convergence)
	rightEye.draw()

	# Left eye (on screen right)

	leftIris.rotateToX(curY)
	leftIris.rotateToY(curX + convergence)
	leftIris.draw()
	leftEye.rotateToX(curY)
	leftEye.rotateToY(curX + convergence)
	leftEye.draw()



# MAIN LOOP -- runs continuously -------------------------------------------

class coords:
	def __init__(self):
		self.px = 0
		self.py = 0
		self.x = 0
		self.y = 0

eye_coords = coords()

setup_camera()

track_thread = Thread(target=track_loop, args=(eye_coords,))
track_thread.start()

# freeze_flag = False
#
# voice_thread = Thread(target=voice)
# voice_thread.start()

while True:
	frame()
