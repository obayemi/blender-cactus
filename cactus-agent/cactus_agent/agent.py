from pathlib import Path
import logging

from websockets.asyncio.client import connect

import cactus_tools as tools
from cactus_tools import commands
import blender_render as render


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(levelname)s - %(name)s: %(message)s',
                    level=logging.INFO,
                    datefmt='%m-%d-%Y %I:%M:%S',)



class Agent():

    OUT_FOLDER = Path('OUT')
    ARCHIVES_FOLDER = Path('archives')

    def __init__(self, out:str=None, archive:str=None):
        if out:
            self.OUT_FOLDER = Path(out)
        if archive:
            self.ARCHIVES_FOLDER = Path(archive)

    async def render(cmd: commands.Render):
        render.set_project(self.ARCHIVES_FOLDER / cmd.file)
        
        out_folder = (self.OUT_FOLDER / cmd.file).with_suffix('')
        render.render(out_folder, cmd.frame_start, cmd.frame_stop)
        tools.make_archive(out_folder,out_folder.with_suffix("zip"))
        return out_folder.with_suffix("zip")


    async def handle_message(self, websocket):
        websocket.logger.info("Connected")
        async for message in websocket:
            websocket.logger.debug(message)
            data = commands.CactusCommand.model_validate_json(message)
            if isinstance(data, commands.File):
                await tools.recv_file(websocket, data.name, self.ARCHIVES_FOLDER)
            elif isinstance(data, commands.SendFile):
                await tools.send_file(websocket, data.name, self.OUT_FOLDER)
            elif isinstance(data, commands.Render):
                result = await render(data)
                await tools.send_file(websocket, result)


    async def run(self, server_url:str):
        logger.info(f"Trying to connect to {server_url}")
        try:
            async with connect(server_url) as websocket:
                await websocket.send(commands.Connection(cat="agent").json())
                await self.handle_message(websocket)

        except ConnectionRefusedError:
            logger.error(f"Impossible to connect to {server_url}")
