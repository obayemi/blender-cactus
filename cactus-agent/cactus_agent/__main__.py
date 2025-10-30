import asyncio
from argparse import ArgumentParser

from agent import Agent

parser = ArgumentParser()
parser.add_argument("-s", "--server", type=str, default="ws://127.0.0.1:8000", help="URL of server")
parser.add_argument("--out", type=str, default=None)
parser.add_argument("--archives", type=str, default=None)
args = parser.parse_args()
agent = Agent(args.out, args.archives)
asyncio.run(agent.run(args.server))
