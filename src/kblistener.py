from collections import namedtuple
from ctypes import windll, CFUNCTYPE, POINTER, c_int, c_void_p, byref
import win32con, win32api, win32gui, atexit

KeyboardEvent = namedtuple('KeyboardEvent', ['event_type', 'key_code',
											 'scan_code', 'alt_pressed',
											 'time'])

event_types = {win32con.WM_KEYDOWN: 'key down',
				win32con.WM_KEYUP: 'key up',
				0x104: 'key down', # WM_SYSKEYDOWN, used for Alt key.
				0x105: 'key up', # WM_SYSKEYUP, used for Alt key.
				}

key_map = {'A': 0x41, 'B': 0x42}

trigger_keys = []

cb = False

def set_trigger_key(key):
	global trigger_keys
	print('add trigger key' + key)
	trigger_keys.append(key_map[key])

def set_callback(func):
	global cb
	cb = func

def run():
	def key_handler(nCode, wParam, lParam):
		event = KeyboardEvent(event_types[wParam], lParam[0], lParam[1],
							  lParam[2] == 32, lParam[3])
		print(event)

		print('key_code ' + str(trigger_keys.index(event.key_code)))
		print('key_type ' + event.event_type)
		if event.event_type == 'key down' and event.key_code in trigger_keys:
			cb()

		return windll.user32.CallNextHookEx(hook_id, nCode, wParam, lParam)

	CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
	pointer = CMPFUNC(key_handler)

	hook_id = windll.user32.SetWindowsHookExA(win32con.WH_KEYBOARD_LL, pointer,
											 win32api.GetModuleHandle(None), 0)

	atexit.register(windll.user32.UnhookWindowsHookEx, hook_id)

	while True:
		msg = win32gui.GetMessage(None, 0, 0)
		win32gui.TranslateMessage(byref(msg))
		win32gui.DispatchMessage(byref(msg))
