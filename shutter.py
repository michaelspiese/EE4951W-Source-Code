from evdev import InputDevice, categorize, ecodes

ABShutter3 = InputDevice('/dev/input/event3')

EV_VAL_PRESSED = 1
EV_VAL_RELEASED = 0
BTN_SHUTTER = 115

print(ABShutter3)

while 1:
	for event in ABShutter3.read():
		if event.type == ecodes.EV_KEY:
			if event.value == EV_VAL_PRESSED:
				if event.code == BTN_SHUTTER:
					print('---')
					print('pressed')
					print(event)
