import struct
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


def control(ser, mode, step):
	command = [0xff, mode]
	command += list(struct.pack(">h", step))

	data_sum = 0
	for x in command:
		data_sum += x

	our_checksum = (~data_sum & 0xFF)
	command.append(our_checksum)

	ser.write(command)
