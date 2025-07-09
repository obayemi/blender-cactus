import asyncio
import signal
import logging

from websockets.asyncio.server import serve, broadcast
from pydantic import ValidationError

from cactus_tools import commands
from cactus_tools import *

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(levelname)s - %(name)s: %(message)s',
                    level=logging.INFO,
                    datefmt='%m-%d-%Y %I:%M:%S',)


class Server():

    def __init__(self):
        self.agent = dict()
        self.client = dict()

    async def handle_client(self,websocket):
        websocket.logger.info(f"New client connected: {str(websocket.id)}")
        self.client[str(websocket.id)] = websocket
        await websocket.send(commands.AgentList(list=self.agent.keys()).json())
        await websocket.wait_closed()

    async def handle_agent(self,websocket):
        websocket.logger.info(f"New agent connected: {str(websocket.id)}")
        self.agent[str(websocket.id)] = websocket
        broadcast(self.client.values(), commands.AgentList(list=self.agent.keys()).json())
        # await send_file(websocket, "test.png", Path("test"))
        # await websocket.send(commands.Render(project="test",frame_start=3,frame_stop=10).json())
        await websocket.send(commands.SendFile(name="test.png").json())
        async for message in websocket:
            logger.debug(message)
            data = commands.CactusCommand.parse_raw(message)
            if isinstance(data, commands.File):
                await recv_file(websocket, data.name, Path("test"))

        del self.agent[str(websocket.id)]
        broadcast(self.client.values(), commands.AgentList(list=self.agent.keys()).json())
        websocket.logger.info(f"Agent disconnected: {str(websocket.id)}")

    async def handler(self, websocket):
        message = await websocket.recv()
        try:
            data = commands.Connection.model_validate_json(message)
            if isinstance(data, commands.Connection):
                if data.cat == "agent":
                    await self.handle_agent(websocket)
                elif data.cat == "client":
                    await self.handle_client(websocket)

        except ValidationError:
            websocket.logger.error(f"First message is not a valid connection command : {message}")    


    async def run(self, server_url:str, server_port:int):
        logger.debug(f"Starting to listen on {server_url}:{server_port}")
        async with serve(self.handler, server_url, server_port) as server:
            loop = asyncio.get_running_loop()
            loop.add_signal_handler(signal.SIGINT, server.close)
            loop.add_signal_handler(signal.SIGTERM, server.close)
            await server.wait_closed()
