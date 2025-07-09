import asyncio
from argparse import ArgumentParser

from server import Server

parser = ArgumentParser()
parser.add_argument("-u","--url", type=str, default="0.0.0.0", help="URL to server")
parser.add_argument("-p","--port", type=int, default=8000, help="Port to wit connection on")
args = parser.parse_args()
server = Server()
asyncio.run(server.run(args.url,args.port))
