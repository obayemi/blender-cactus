import abc
from pydantic import BaseModel, TypeAdapter, Field, model_validator, ValidatorFunctionWrapHandler
from typing import Literal, Annotated, Union, Any, ClassVar


class CactusCommand(BaseModel, abc.ABC):
    type: str

    _subclasses: ClassVar[dict[str, type[Any]]] = {}
    _discriminating_type_adapter: ClassVar[TypeAdapter]

    @model_validator(mode='wrap')
    @classmethod
    def _parse_into_subclass(cls, v: Any, handler: ValidatorFunctionWrapHandler) -> 'CactusCommand':
        if cls is CactusCommand:
            return CactusCommand._discriminating_type_adapter.validate_python(v)
        return handler(v)

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        CactusCommand._subclasses[cls.model_fields['type'].default] = cls

        CactusCommand._discriminating_type_adapter = TypeAdapter(
            Annotated[Union[tuple(CactusCommand._subclasses.values())], Field(discriminator='type')])


class Connection(CactusCommand):
    type: Literal["connection"] = "connection"
    cat: Literal["agent", "client"]


class File(CactusCommand):
    type: Literal["file"] = "file"
    name: str


class SendFile(CactusCommand):
    type: Literal["send file"] = "send file"
    name: str


class Render(CactusCommand):
    type: Literal["render"] = "render"
    file: str
    scene: str
    frame_start: int
    frame_stop: int


class HaveFile(CactusCommand):
    type: Literal["have file"] = "have file"
    name: str


class HasFile(CactusCommand):
    type: Literal["has file"] = "has file"
    name: str
    has: bool

class AgentList(CactusCommand):
    type: Literal["agent list"] = "agent list"
    list: set[str]
