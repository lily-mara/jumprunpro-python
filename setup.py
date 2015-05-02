from setuptools import setup

setup(
	name='jumprunpro-python',
	version='0.0.1',
	author='Nate Mara',
	author_email='natemara@gmail.com',
	description='A simple API for getting winds aloft data from NOAA',
	license='MIT',
	test_suite='tests',
	keywords='skydiving manifest',
	url='https://github.com/natemara/jumprunpro-python',
	packages=['jumprun'],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Topic :: Utilities',
		'License :: OSI Approved :: MIT License',
	],
	install_requires=[
		'beautifulsoup4==4.3.2',
		'requests==2.6.2',
		'python-dateutil==2.4.2',
	],
)
