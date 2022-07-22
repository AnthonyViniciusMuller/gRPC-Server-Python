from concurrent import futures
import threading
import grpc
import os
import protos.messenger_pb2 as pb2
import protos.messenger_pb2_grpc as pb2_grpc

import queue


queue = queue.Queue()

class ChatServicer(pb2_grpc.ChatServicer):
	clients = []
	def GetMessages(self, text, context):
		print(text)
		self.clients.append(context)

		while True:
			print(self.clients)
			message = queue.get()
			yield pb2.Message(
				Message = message.Message, 
				User = message.User
			)

	def SendMessage(self, request, context):
		queue.put(request)

		return pb2.Void()
			
if __name__ == "__main__":
	os.system('cls||clear')
	print('Python Server')    
	
	grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	pb2_grpc.add_ChatServicer_to_server(ChatServicer(), grpc_server)

	grpc_server.add_insecure_port('localhost:4444')
	grpc_server.start()
	grpc_server.wait_for_termination()
