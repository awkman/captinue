import pyscreenshot as ss
import configparser as cp
import kblistener as kl

index = 0

CONFIG_PATH = '../config/config.ini'
config = cp.ConfigParser()
config.read(CONFIG_PATH)
IMG_TYPE = config['DEFAULT']['IMG_TYPE']
HOTKEY = config['DEFAULT']['HOTKEY']
SAVE_PATH = config['DEFAULT']['SAVE_PATH']


def capture():
	global index
	print('capture')
	file_name = SAVE_PATH + '\screen_' + str(index) + '.' + IMG_TYPE
	ss.grab_to_file(file_name)
	index += 1

if __name__ == '__main__':
	kl.set_trigger_key(HOTKEY)
	kl.set_callback(capture)
	kl.run()
