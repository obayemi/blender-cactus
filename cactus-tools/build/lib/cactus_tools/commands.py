import abc
from pydantic import BaseModel, TypeAdapter, Field, model_validator, ValidatorFunctionWrapHandler
from pydantic.fields import FieldInfo
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
        # This approach requires all subclasses have a field called 'type' to be used as a discriminator
        CactusCommand._subclasses[cls.model_fields['type'].default] = cls

        # The following will create a new type adapter every time a new subclass is created,
        # which is fine if there aren't that many classes (as far as performance goes)
        CactusCommand._discriminating_type_adapter = TypeAdapter(
            Annotated[Union[tuple(CactusCommand._subclasses.values())], Field(discriminator='type')])


class Connection(CactusCommand):
    type: Literal["connection"] = "connection"
    cat: Literal["agent", "client"]


class File(CactusCommand):
    type: Literal["file"] = "file"
    name: str


class SendFile(CactusCommand):
    type: Literal["sendfile"] = "sendfile"
    name: str


class Render(CactusCommand):
    type: Literal["render"] = "render"
    project: str
    frame_start: int
    frame_stop: int


class HaveFile(CactusCommand):
    type: Literal["havefile"] = "havefile"
    name: str


class HasFile(CactusCommand):
    type: Literal["hasfile"] = "hasfile"
    name: str
    has: bool
