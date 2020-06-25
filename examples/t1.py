from makerasia import pendulum
import time

s = pendulum.create('/dev/tty.usbserial-14340')

pendulum.control(s, 0x02, 300)
time.sleep(1)
pendulum.control(s, 0x02, -300)
time.sleep(2)

pendulum.control(s, 0x01, 1000)
time.sleep(2)
pendulum.control(s, 0x01, -1000)
