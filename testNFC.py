import sys

sys.path.append('./py532/py532lib')

from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *

pn532 = Pn532_i2c()
pn532.SAMconfigure()

while True:
	card_data = pn532.read_mifare().get_data()
	print("Card detected")
	print(card_data)
