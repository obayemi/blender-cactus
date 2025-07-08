# import bpy
import tempfile
import shutil
from pathlib import Path
import os
import typing
import logging

from cactus_tools import commands
from websockets.asyncio.client import connect


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(levelname)s - %(name)s: %(message)s',
                    level=logging.INFO,
                    datefmt='%m-%d-%Y %I:%M:%S',)

SERVER_URL = "ws://127.0.0.1:8001"
OUT_FOLDER = Path('OUT')
ARCHIVES_FOLDER = Path('archives')


class Frame:
    def __init__(self, archive, frame):
        self.frame = frame
        self.archive = archive

    def __str__(self):
        return f'{self.frame}@{self.archive}'

    def __repr__(self):
        return f'<{self}>'

    def render(self):
        bpy.ops.wm.open_mainfile(filepath=str(self.archive.local_path))
        scene = bpy.context.scene
        with tempfile.NamedTemporaryFile(suffix=".png") as temp_file:
            scene.frame_set(self.frame)
            scene.render.filepath = temp_file.name
            bpy.ops.render.render(write_still=True)
            self.export(temp_file)

    def export(self, temp_file:typing.BinaryIO):
        archive_output_folder = OUT_FOLDER / self.archive.id
        if not archive_output_folder.is_dir():
            os.mkdir(archive_output_folder)

        out_path = archive_output_folder / f'{self.frame:04}.png'
        print(out_path)
        with out_path.open('wb') as out:
            shutil.copyfileobj(temp_file, out)


class Agent():

    async def handle_message(self, websocket):
        async for message in websocket:
            logger.info(message)

    async def run(self, server_url=None):
        server_url = server_url if server_url else SERVER_URL
        logger.info(f"Trying to connect to {server_url}")
        cmd = commands.Connection(cat="agent")
        print(cmd)
        print(type(cmd))
        print(cmd.json())
        print("---------------------------")

        cmd = commands.Command.validate_json(cmd.json())
        print(cmd)
        print(type(cmd))
        print(isinstance(cmd, commands.Connection))
        # print(cmd.cat)
        print(cmd.model_dump_json(serialize_as_any=True))
        print("---------------------------")
        print("---------------------------")
        cmd = commands.File(name="test.jpg")
        print(cmd)
        print(type(cmd))
        print(cmd.json())
        print("---------------------------")

        cmd = commands.Command.validate_json(cmd.json())
        print(cmd)
        print(type(cmd))
        print(isinstance(cmd, commands.File))
        # print(cmd.cat)
        print(cmd.model_dump_json(serialize_as_any=True))
        try:
            async with connect(SERVER_URL) as websocket:
                await self.handle_message(websocket)

        except ConnectionRefusedError:
            logger.error(f"Impossible to connect to {server_url}")
