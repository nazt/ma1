from . import pendulum

import time
import click, serial
import struct, sys
import threading

assert sys.version[:1] == "3"

p = ""
b = 0
_debug = False


# @click.option('--debug', required=False, help='Debug mode')
@click.option('--port', required=True, type=str, help='Serial Port')
@click.option('--baud', required=False, type=int, help='Baudrate', default=115200)
@click.group()
def cli(port, baud):
	"""A CLI for Inverse Pendulum"""
	global p, b, _debug	
	p = port
	b = baud


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
	while True:
		try:
			line = readline(ser)
			pendulum_angle, pendulum_velocity, cart_position, cart_velocity, cart_acceleration, limit_A, limit_B = line.decode(
				"utf-8").strip().split(",")
			# status = (float(pendulum_angle), pendulum_velocity, cart_position, cart_velocity, cart_acceleration, limit_A, limit_B)
			status = (
				float(pendulum_angle), pendulum_velocity, cart_position, cart_velocity, cart_acceleration, limit_A,
				limit_B)
			print(status)

			theta = status[0]
			if theta < 0:
				theta = 180.0 - status[0]

		except Exception as e:
			print(e)
		except KeyboardInterrupt:
			print("closing serial port...")
			ser.close()
			sys.exit()
		finally:
			pass


# , nargs=2, type=click.Tuple([str, int]))
# @click.option('--control', required=True, type=str, help='Serial Port')
@cli.command('test')
@click.option('--mode', type=int, default=2)
@click.option('--value', type=int, default=300)
@click.option('-t', type=float, default=.15)
def _x(mode, value, t):
	print(mode, value)
	# click.echo('name=%s id=%d' % item)
	# click.echo('name=%s id=%d' % item)
	global p, b
	port = p
	baud = b
	# print('port={}'.format(p))
	# print('baud', baud)

	ser = serial.Serial(
		port=port,
		baudrate=baud,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS
	)
	thread = threading.Thread(target=read_from_port, args=(ser,))
	thread.start()
	print(ser)
	v = value
	pendulum.control(ser, 0x02, 300)
	time.sleep(.3)

	for x in range(0, 500):
		for y in range(4):
			pendulum.control(ser, mode, v)
			time.sleep(t)
			pendulum.control(ser, mode, -v)
			time.sleep(t)


def main():
	cli()
