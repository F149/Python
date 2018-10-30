import asyncio

storage = {}

class ClientServerProtocol(asyncio.Protocol):
	def connection_made(self, transport):
		self.transport = transport

	def data_received(self, data):
		resp = self.process_data(data.decode())
		self.transport.write(resp.encode())

	def process_data(self, data):
		if data[0:3] == "put":
			comm, key, value, timestamp = data.split()
			if key not in storage:
				storage[key] = []
			storage[key].append((int(timestamp), float(value)))
			resp = "ok\n\n"
		elif data[0:3] == "get":
			comm, key = data.split()
			resp = "ok\n"
			if key != "*":
				if key in storage:
					for metric in storage[key]:
						resp += key + ' ' + str(metric[1]) + ' ' + str(metric[0]) + "\n"
			else:
				for key in storage:
					for metric in storage[key]:
						resp += key + ' ' + str(metric[1]) + ' ' + str(metric[0]) + "\n"
			resp += "\n"
		else:
			resp = "error\nwrong command\n\n"

		return resp

def run_server(host, port):
	loop = asyncio.get_event_loop()
	coro = loop.create_server(
		ClientServerProtocol,
		host, port
	)
	server = loop.run_until_complete(coro)
	try:
		loop.run_forever()
	except KeyboardInterrupt:
		pass
	server.close()
	loop.run_until_complete(server.wait_closed())
	loop.close()
