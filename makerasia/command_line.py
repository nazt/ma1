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


# @cli.command('control')
# @click.option('--mode', type=int, default=2)
# @click.option('--value', type=int, default=300)
# @click.option('-t', type=float, default=.15)
# def _x2(mode, value, t):
# 	pass

# , nargs=2, type=click.Tuple([str, int]))
# @click.option('--control', required=True, type=str, help='Serial Port')
@cli.command('control')
@click.option('--mode', type=int, default=2)
@click.option('--value', type=int, default=300)
@click.option('-t', type=float, default=.15)
def _x(mode, value, t):
	global p, b
	port = p
	baud = b

	ser = serial.Serial(
		port=port,
		baudrate=baud,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS)
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
