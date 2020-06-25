import struct
import serial
import threading

cb = None
thread = None


def create(port, baud=115200, _cb=None):
	global cb, thread
	cb = _cb
	ser = serial.Serial(
		port=port,
		baudrate=baud,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS
	)

	thread = threading.Thread(target=read_from_port, args=(ser,))
	thread.start()

	return ser


def add_callback(_cb):
	global cb
	cb = _cb


def control(ser, mode, step):
	command = [0xff, mode]
	command += list(struct.pack(">h", step))

	data_sum = 0
	for x in command:
		data_sum += x

	our_checksum = (~data_sum & 0xFF)
	command.append(our_checksum)

	ser.write(command)


# https://stackoverflow.com/a/27628622
def readline(a_serial, eol=b'\r\n'):
	leneol = len(eol)
	line = bytearray()
	while True:
		c = a_serial.read(1)
		# print(c)
		if c:
			line += c
			if line[-leneol:] == eol:
				break
		else:
			break
	return (line)


def read_from_port(ser):
	global cb
	while True:
		try:
			line = readline(ser)
			pendulum_angle, pendulum_velocity, cart_position, cart_velocity, cart_acceleration, limit_A, limit_B = line.decode(
				"utf-8").strip().split(",")
			# status = (float(pendulum_angle), pendulum_velocity, cart_position, cart_velocity, cart_acceleration, limit_A, limit_B)
			status = (
				float(pendulum_angle), pendulum_velocity, cart_position, cart_velocity, cart_acceleration, limit_A,
				limit_B)
			if cb:
				cb(status)

		# theta = status[0]
		# if theta < 0:
		# 	theta = 180.0 - status[0]

		except Exception as e:
			print(e)
		except KeyboardInterrupt:
			print("closing serial port...")
			ser.close()
			sys.exit()
		finally:
			pass
