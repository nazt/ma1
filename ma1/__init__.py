from markdown import markdown
from . import pendulum
import serial


def create(port, baud=115200):
	ser = serial.Serial(
		port=port,
		baudrate=baud,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS
	)
	return ser
