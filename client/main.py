import bpy
import tempfile
import shutil
from pathlib import Path
import os
from uuid import uuid4


def export(frame_file, archive, frame_id):
    """
    temp, should actually send to the server
    """
    # TODO: actual implem
    hash_str = archive["hash"]
    dest_folder = Path("./out") / hash_str
    os.makedirs(dest_folder, exist_ok=True)
    dest = dest_folder / f"{hash_str}_{frame_id:05}.png"
    shutil.copy(frame_file.name, dest)
    print(f"saved frame {frame_id} in ", dest)


def render(scene_file, frames, exporter):
    bpy.ops.wm.open_mainfile(filepath=scene_file)
    scene = bpy.context.scene
    for frame in frames:
        with tempfile.NamedTemporaryFile(suffix=".png") as temp_file:
            scene.frame_set(frame)
            scene.render.filepath = temp_file.name
            bpy.ops.render.render(write_still=True)
            exporter(temp_file, frame)


def exporter(project_hash):
    """
    calls exporter with project hash and other metadata not passed to/from the renderer
    """

    def thing(frame_file, frame_id):
        export(frame_file, project_hash, frame_id)

    return thing


PROJECT_PROJECT_STUFF = {
    "id": uuid4(),
    "project_name": "project foo",
    "frame_start": 0,
    "frame_end": 5,
    "archives": [
        {
            "hash": "2b5b6a77d82e9fbe2e93c410cba3600c",
            "url": "file://<project_stuff>",
        }
    ],
}
FAKE_DB = {
    "projects": {PROJECT_PROJECT_STUFF["id"]: PROJECT_PROJECT_STUFF},
    "tasks": [
        {
            "project_id": PROJECT_PROJECT_STUFF["id"],
            "archive_hash": PROJECT_PROJECT_STUFF["archives"][0]["hash"],
            "scene": "./untitled.blend",
            "frame": 1,
        }
    ],
}


def ensure_archive(archive):
    """
    fetch archive from server, (skip if already downloaded, add check with archive hash)
    extract, return path to scene file
    """
    # TODO: check if archive exists fetch archive into archives/<hash>
    print("foo", archive)


def get_task():
    for task in FAKE_DB["tasks"]:
        project = FAKE_DB["projects"][task["project_id"]]
        project_archives = project["archives"]
        archive = next(
            (a for a in project_archives if a["hash"] == task["archive_hash"]), None
        )

        ensure_archive(archive)
        yield task


for task in get_task():
    pass
    # render(scene_file, frames, exporter(request["archive"]))
