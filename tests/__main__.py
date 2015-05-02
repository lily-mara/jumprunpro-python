from unittest import main
from pprint import pprint

from jumprun import JumprunProApi


if __name__ == '__main__':
	jump = JumprunProApi('skydive-warren-county')
	pprint(jump.departing_loads())
	main('tests')
