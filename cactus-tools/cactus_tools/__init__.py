from pathlib import Path
import shutil

from websockets.asyncio.connection import Connection

from .commands import File


async def send_file(websocket: Connection, file_name: str, folder: Path=None):
    path = ""
    if folder:
        path = folder / file_name
    else:
        path = Path(file_name)
    websocket.logger.info(f"Sending file : {path}")
    await websocket.send(File(name=file_name).json())
    await websocket.send(path.read_bytes())


async def recv_file(websocket: Connection, file_name: str, folder: Path=None):
    websocket.logger.info(f"Receiving file : {file_name}")
    path = ""
    if folder:
        if not folder.exists():
            folder.mkdir(parents=True)
        elif folder.is_file():
            raise FileExistsError()
        path = folder / file_name
    else:
        path = Path(file_name)
    data = await websocket.recv()
    path.write_bytes(data)
    websocket.logger.info(f"Written file to {path}")


def make_archive(source: Path, destination: Path) -> None:
    base_name = destination.parent / destination.stem
    fmt = destination.suffix.replace(".", "")
    root_dir = source.parent
    base_dir = source.name
    shutil.make_archive(str(base_name), fmt, root_dir, base_dir)
