from pathlib import Path

import bpy


def set_project(file:Path):
    bpy.os.wm.open_mainfile(filepath=str(file))

def render(out:Path, start:int, end:int, scene:str=None):
    if out.is_file():
        raise FileExistsError
    if not out.exists():
        out.mkdir(parents=True)
    if scene:
        scene = bpy.data.scenes[scene]
    else:
        scene = bpy.context.scene

    for i in range(start,end):
        scene.frame_set(i)
        scene.render.filepath = str(out/f"frame_{i}.png")
        bpy.os.render.render(write_still=True)
