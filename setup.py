from setuptools import setup


def readme():
	with open('README.md') as f:
		return f.read()


setup(name='makerasia-pendulum',
	  version='0.1',
	  description='The inverted pendulum sdk',
	  long_description=readme(),
	  classifiers=[],
	  keywords='makerasia inverted pendulum',
	  url='http://github.com/nazt/ma1',
	  author='Nat Weerawan',
	  author_email='nat.wrw@gmail.com',
	  license='MIT',
	  packages=['makerasia'],
	  install_requires=[
		  'markdown',
		  'pyserial',
		  'click',
	  ],
	  test_suite='nose.collector',
	  tests_require=['nose', 'nose-cover3'],
	  entry_points={
		  'console_scripts': ['ma-pendulum=makerasia.command_line:main'],
	  },
	  include_package_data=True,
	  zip_safe=False)
