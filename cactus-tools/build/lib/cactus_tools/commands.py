import abc
from pydantic import BaseModel, SerializeAsAny, TypeAdapter, Field
from typing import Literal, Annotated


class CactusCommand(BaseModel, abc.ABC):
    type: str


# Command = Annotated[SerializeAsAny[CactusCommand], Field(discriminator='type')]
# Command = TypeAdapter(Annotated[CactusCommand, Field(discriminator='type')])


class Connection(CactusCommand):
    type: Literal["connection"] = "connection"
    cat: Literal["agent"] | Literal["client"]


class File(CactusCommand):
    type: Literal["file"] = "file"
    name: str


class SendFile(CactusCommand):
    type: Literal["send file"] = "send file"
    name: str


class Render(CactusCommand):
    type: Literal["render"] = "render"
    project: str
    frame_start: int
    frame_stop: int


class HaveFile(CactusCommand):
    type: Literal["have file"] = "have file"
    name: str


class HasFile(CactusCommand):
    type: Literal["has file"] = "has file"
    name: str
    has: bool


Command = TypeAdapter(Connection | File | SendFile)
