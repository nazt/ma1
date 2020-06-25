from makerasia import pendulum
import time
import threading

s = pendulum.create('/dev/tty.usbserial-14340')

pendulum.control(s, 0x02, 300)


def read_from_port(ser):
	while True:
		try:
			line = pendulum.readline(ser)
			pendulum_angle, pendulum_velocity, cart_position, cart_velocity, cart_acceleration, limit_A, limit_B = line.decode("utf-8").strip().split(",")
			status = (float(pendulum_angle), pendulum_velocity, cart_position, cart_velocity, cart_acceleration, limit_A, limit_B)
			print(status)
		except Exception as e:
			pass
		except KeyboardInterrupt:
			print("closing serial port...")
			ser.close()
			sys.exit()
		finally:
			pass


thread = threading.Thread(target=read_from_port, args=(s,))
thread.start()

time.sleep(1)
pendulum.control(s, 0x02, -300)
time.sleep(2)

pendulum.control(s, 0x01, 1000)
time.sleep(2)
pendulum.control(s, 0x01, -1000)
