from camera.track import setup_camera, track_loop
import numpy as np
from threading import Thread
from setup import *

# Generate one frame of imagery
def frame(p):

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
	if isMoving == True:
		if dt <= moveDuration:
			scale        = (now - startTime) / moveDuration
			# Ease in/out curve: 3*t^2-2*t^3
			scale = 3.0 * scale * scale - 2.0 * scale * scale * scale
			curX         = startX + (destX - startX) * scale
			curY         = startY + (destY - startY) * scale
		else:
			startX       = destX
			startY       = destY
			curX         = destX
			curY         = destY
			holdDuration = 0.1
			startTime    = now
			isMoving     = False
	else:
		if dt >= holdDuration:
			destX        = np.interp(eye_coords.x, [0, 1280], [-30, 30])
			destY        = -np.interp(eye_coords.y, [0, 720], [-30, 30])
			moveDuration = random.uniform(0.075, 0.175)
			startTime    = now
			isMoving     = True

	# Regenerate iris geometry only if size changed by >= 1/4 pixel
	if abs(p - prevPupilScale) >= irisRegenThreshold:
		# Interpolate points between min and max pupil sizes
		interPupil = points_interp(pupilMinPts, pupilMaxPts, p)
		# Generate mesh between interpolated pupil and iris bounds
		mesh = points_mesh((None, interPupil, irisPts), 4, -irisZ, True)
		# Assign to both eyes
		leftIris.re_init(pts=mesh)
		rightIris.re_init(pts=mesh)
		prevPupilScale = p

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


def split( # Recursive simulated pupil response when no analog sensor
  startValue, # Pupil scale starting value (0.0 to 1.0)
  endValue,   # Pupil scale ending value (")
  duration,   # Start-to-end time, floating-point seconds
  range):     # +/- random pupil scale at midpoint
	startTime = time.time()
	if range >= 0.125: # Limit subdvision count, because recursion
		duration *= 0.5 # Split time & range in half for subdivision,
		range    *= 0.5 # then pick random center point within range:
		midValue  = ((startValue + endValue - range) * 0.5 +
		             random.uniform(0.0, range))
		split(startValue, midValue, duration, range)
		split(midValue  , endValue, duration, range)
	else: # No more subdivisons, do iris motion...
		dv = endValue - startValue
		while True:
			dt = time.time() - startTime
			if dt >= duration: break
			v = startValue + dv * dt / duration
			if   v < PUPIL_MIN: v = PUPIL_MIN
			elif v > PUPIL_MAX: v = PUPIL_MAX
			frame(v) # Draw frame w/interim pupil scale value


# MAIN LOOP -- runs continuously -------------------------------------------

class coords:
	def __init__(self):
		self.x = 0
		self.y = 0

eye_coords = coords()

setup_camera()

track_thread = Thread(target=track_loop, args=(eye_coords,))
track_thread.start()

while True:
	# Fractal auto pupil scale
	v = random.random()
	split(currentPupilScale, v, 4.0, 1.0)
	currentPupilScale = v
