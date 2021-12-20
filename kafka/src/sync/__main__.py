import requests
import json

from utils.db import DB
from kafka import KafkaConsumer


class Connectors:
	def __init__(self, url: str) -> None:
		self.url = url
		self.expected_connectors = ['source-connector']
		self.connectors = []
		self.fetch_available_connectors()
		self.create_connectors()

	def fetch_available_connectors(self):
		r = requests.get(self.url + '/connectors/')

		if r.status_code != 200:
			raise IndexError('Failed to fetch connectors.')

		self.connectors = r.json()
		return self.connectors

	def create_connector(self, name: str):
		contents = open('/app/sync/connectors/' + name + '.json', 'rb').read()
		headers = {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		}

		r = requests.post(self.url + '/connectors/', data=contents, headers=headers)

		if r.status_code != 201:
			raise IndexError('Failed to create connectors.')

		return r.json()

	def create_connectors(self):
		for connector in self.expected_connectors:
			if connector not in self.connectors:
				self.create_connector(connector)
				self.connectors.append(connector)

if __name__ == '__main__':
	connectors = Connectors('http://10.5.0.6:8083')

	consumer = KafkaConsumer('SOURCE.public.holding')
	for msg in consumer:
		input_json = json.loads(msg.value)
		op_type = input_json.get('op')

		if op_type == 'c':
			after = input_json.get('after', {})

			fetch = DB('DESTINATION')
			fetch.insert('holding', list(after.keys()))
			fetch.execute(list(after.values()))