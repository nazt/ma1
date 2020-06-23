ma1
--------

## Installation
	pip install git+https://github.com/NAzT/ma1.git
	
To use (with caution), simply do::

	>>> import ma1
	>>> s = ma1.create('/dev/tty.usbserial-14210')
	>>> ma1.pendulum.control(s, 0x02, 300)
	>>> ma1.pendulum.control(s, 0x02, -300)

