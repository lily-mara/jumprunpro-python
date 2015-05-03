#!/usr/bin/env python3
from unittest import TestCase
import os
import sys

from bs4 import BeautifulSoup

from jumprun import JumprunProApi

NoneType = type(None)
BASE_PATH = os.path.dirname(__file__)


def read_file(filename):
	with open(BASE_PATH + '/' + filename, 'r') as f:
		return ''.join(f.readlines())

if sys.version_info.major < 3:
	str = eval('unicode')


class TestDepartingLoadsFormat(TestCase):
	api = JumprunProApi('skydive-warren-county')
	loads = api.departing_loads()

	def test_contains_call(self):
		for load in self.loads:
			self.assertIn('call', load.keys())

	def test_call_type(self):
		for load in self.loads:
			self.assertIn(type(load['call']), (str, NoneType))

	def test_contains_call_time(self):
		for load in self.loads:
			self.assertIn('call_time', load.keys())

	def test_call_time_type(self):
		for load in self.loads:
			self.assertEqual(type(load['call_time']), int)

	def test_contains_name(self):
		for load in self.loads:
			self.assertIn('name', load.keys())

	def test_name_type(self):
		for load in self.loads:
			self.assertEqual(type(load['name']), str)

	def test_contains_slots(self):
		for load in self.loads:
			self.assertIn('slots', load.keys())

	def test_slots_type(self):
		for load in self.loads:
			self.assertEqual(type(load['slots']), list)

	def test_contains_state(self):
		for load in self.loads:
			self.assertIn('state', load.keys())

	def test_state_type(self):
		for load in self.loads:
			self.assertEqual(type(load['state']), str)

	def test_contains_slot_activity(self):
		for load in self.loads:
			for slot in load['slots']:
				self.assertIn('activity', slot.keys())

	def test_slot_activity_type(self):
		for load in self.loads:
			for slot in load['slots']:
				self.assertEqual(type(slot['activity']), str)

	def test_contains_slot_name(self):
		for load in self.loads:
			for slot in load['slots']:
				self.assertIn('name', slot.keys())

	def test_slot_name_type(self):
		for load in self.loads:
			for slot in load['slots']:
				self.assertEqual(type(slot['name']), str)


class TestDepartingLoadsExample(TestCase):
	api = JumprunProApi('skydive-warren-county')
	loads = api._parse_departing_loads(BeautifulSoup(read_file('departing.html')))

	def test_states(self):
		self.assertEqual(self.loads[0]['state'], 'Departed')
		self.assertEqual(self.loads[1]['state'], 'Scheduled')
		self.assertEqual(self.loads[2]['state'], 'Scheduled')

	def test_calls(self):
		self.assertEqual(self.loads[0]['call'], None)
		self.assertEqual(self.loads[1]['call'], '11 minutes')
		self.assertEqual(self.loads[2]['call'], '36 minutes')

	def test_call_times(self):
		self.assertEqual(self.loads[0]['call_time'], 0)
		self.assertEqual(self.loads[1]['call_time'], 11)
		self.assertEqual(self.loads[2]['call_time'], 36)

	def test_load_names(self):
		self.assertEqual(self.loads[0]['name'], 'C-182 Load 13')
		self.assertEqual(self.loads[1]['name'], 'C-182 Load 14')
		self.assertEqual(self.loads[2]['name'], 'C-182 Load 15')

	def test_load_0_slot_activities(self):
		self.assertEqual(self.loads[0]['slots'][0]['activity'], '')
		self.assertEqual(self.loads[0]['slots'][1]['activity'], 'TDM 1 student')
		self.assertEqual(self.loads[0]['slots'][2]['activity'], 'TDM I')
		self.assertEqual(self.loads[0]['slots'][3]['activity'], 'Video & Stills')

	def test_load_0_slot_names(self):
		self.assertEqual(self.loads[0]['slots'][0]['name'], 'JEFFREY AHTING')
		self.assertEqual(self.loads[0]['slots'][1]['name'], 'Joe Wood')
		self.assertEqual(self.loads[0]['slots'][2]['name'], 'Raymond Kuhn')
		self.assertEqual(self.loads[0]['slots'][3]['name'], 'Scott Fritz')

	def test_load_1_slot_activities(self):
		self.assertEqual(self.loads[1]['slots'][0]['activity'], '')
		self.assertEqual(self.loads[1]['slots'][1]['activity'], 'TDM 1 student')
		self.assertEqual(self.loads[1]['slots'][2]['activity'], 'Video & Stills')
		self.assertEqual(self.loads[1]['slots'][3]['activity'], 'TDM I')

	def test_load_1_slot_names(self):
		self.assertEqual(self.loads[1]['slots'][0]['name'], 'JEFFREY AHTING')
		self.assertEqual(self.loads[1]['slots'][1]['name'], 'Russell Olson')
		self.assertEqual(self.loads[1]['slots'][2]['name'], 'Scott Fritz')
		self.assertEqual(self.loads[1]['slots'][3]['name'], 'JOSEPH CIRRINCIONE')

	def test_load_2_slot_activities(self):
		self.assertEqual(self.loads[2]['slots'][0]['activity'], '')
		self.assertEqual(self.loads[2]['slots'][1]['activity'], "10500'")
		self.assertEqual(self.loads[2]['slots'][2]['activity'], "10500'")
		self.assertEqual(self.loads[2]['slots'][3]['activity'], "3500'")
		self.assertEqual(self.loads[2]['slots'][4]['activity'], "10500'")

	def test_load_2_slot_names(self):
		self.assertEqual(self.loads[2]['slots'][0]['name'], 'JEFFREY AHTING')
		self.assertEqual(self.loads[2]['slots'][1]['name'], 'Greg Little')
		self.assertEqual(self.loads[2]['slots'][2]['name'], 'Rosemary Brown')
		self.assertEqual(self.loads[2]['slots'][3]['name'], 'DAVE ARCARO')
		self.assertEqual(self.loads[2]['slots'][4]['name'], 'Chelsea Besser')


class TestTimeToMinutes(TestCase):
	api = JumprunProApi('skydive-warren-county')

	def test_30_minutes(self):
		minutes = self.api._time_to_minutes('30 minutes')
		self.assertEqual(30, minutes)

	def test_93_minutes(self):
		minutes = self.api._time_to_minutes('93 minutes')
		self.assertEqual(0, minutes)

	def test_0_minutes(self):
		minutes = self.api._time_to_minutes('0 minutes')
		self.assertEqual(0, minutes)

	def test_1_minutes(self):
		minutes = self.api._time_to_minutes('1 minutes')
		self.assertEqual(1, minutes)

	def test_1_minute(self):
		minutes = self.api._time_to_minutes('1 minute')
		self.assertEqual(1, minutes)

	def test_1_hour(self):
		minutes = self.api._time_to_minutes('1 hour')
		self.assertEqual(60, minutes)

	def test_1_hours(self):
		minutes = self.api._time_to_minutes('1 hours')
		self.assertEqual(60, minutes)

	def test_2_hours(self):
		minutes = self.api._time_to_minutes('2 hours')
		self.assertEqual(120, minutes)

	def test_24_hours(self):
		minutes = self.api._time_to_minutes('24 hours')
		self.assertEqual(0, minutes)

	def test_48_hours(self):
		minutes = self.api._time_to_minutes('48 hours')
		self.assertEqual(0, minutes)

	def test_2_hours_5_minutes(self):
		minutes = self.api._time_to_minutes('2 hours, 5 minutes')
		self.assertEqual(125, minutes)

	def test_5_mintes_2_hours(self):
		minutes = self.api._time_to_minutes('5 minutes, 2 hours')
		self.assertEqual(125, minutes)

	def test_invalid_string(self):
		minutes = self.api._time_to_minutes('kjfasjfkal')
		self.assertEqual(0, minutes)
