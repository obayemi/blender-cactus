import bpy
import tempfile
import shutil
from pathlib import Path
import time
import os
from urllib.parse import urlparse
import typing

OUT_FOLDER = Path('OUT')
ARCHIVES_FOLDER = Path('archives')
GRAPHQL_URL = "http://localhost:3000/graphql"      

class Archive:
    def __init__(self, url, id):
        self.url = url
        self.id = id

    @property
    def local_path(self):
        path = ARCHIVES_FOLDER / f'${self.id}.blend'
        if not path.is_file():
            self.fetch(path)
        return path

    def fetch(self, destination:Path):
        parsed = urlparse(self.url)
    
        if parsed.scheme == 'file' or parsed.scheme == '':
            shutil.copy(parsed.path, destination)
    
        else:
            # Remote file - download
            raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    def __str__(self):
        return f'{self.local_path}'


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
    def fetch_tasks(self):
        from gql import gql, Client
        from gql.transport.aiohttp import AIOHTTPTransport

        query = gql(
            """
            query AgentTasksQuery {
              frameRequests {
                nodes {
                  frameNumber
                  renderRequest {
                    archive {
                      url
                      nodeId
                    }
                  }
                }
              }
            }
            """
        )

        while True:
            transport = AIOHTTPTransport(url=GRAPHQL_URL)
            client = Client(transport=transport, fetch_schema_from_transport=True)
            result = client.execute(query)
            yield from [
                Frame(
                    archive=Archive(
                        frame['renderRequest']["archive"]["url"], frame['renderRequest']["archive"]["nodeId"]
                    ),
                    frame=frame["frameNumber"],
                )
                for frame in result["frameRequests"]["nodes"]
            ]
            # break
            time.sleep(10)


    def run(self):
        for task in self.fetch_tasks():
            print('got task', task)
            task.render()
        

if __name__ == "__main__":
    Agent().run()
