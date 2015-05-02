#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup


class JumprunProApi(object):
	BASE_URL = 'https://jumprunpro.com/dropzones'

	def __init__(self, dropzone):
		self._dropzone = dropzone
		self._url = JumprunProApi.BASE_URL + '/' + dropzone

		status = requests.get(self._url).status_code
		if status != 200:
			raise ValueError('{} is not a valid dropzone.')

	def _request(self, service):
		return requests.get(self._url + '/' + service)

	def _soup(self, service):
		body = self._request(service).text
		soup = BeautifulSoup(body)

		return soup

	def departing_loads(self):
		soup = self._soup('departing_loads')
		loads = []

		for load in soup.find_all('div', class_='departing-load'):
			load_name = load.find('h3', class_='load-name').text.strip()
			state = load.find('h5', class_='state')
			if state:
				state = state.text.strip()

			call = load.find('h5', class_='call')
			if call:
				call = call.text.strip()

			slots = []
			for slot in load.find_all('tr', class_='slot'):
				slot_name = slot.find('td', class_='slot-name').text.strip()
				slot_activity = slot.find('td', class_='slot-activity').text.strip()

				slots.append({
					'name': slot_name,
					'activity': slot_activity,
				})

			loads.append({
				'state': state,
				'name': load_name,
				'call': call,
				'slots': slots,
			})

		return loads
