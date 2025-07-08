import asyncio
from argparse import ArgumentParser

from agent import Agent

parser = ArgumentParser()
parser.add_argument("--server", type=str, default=None, help="URL of server")
args = parser.parse_args()
agent = Agent()
asyncio.run(agent.run(args.server))
