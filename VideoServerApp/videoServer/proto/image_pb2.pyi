from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ack_request(_message.Message):
    __slots__ = ["req"]
    REQ_FIELD_NUMBER: _ClassVar[int]
    req: str
    def __init__(self, req: _Optional[str] = ...) -> None: ...

class ack_response(_message.Message):
    __slots__ = ["rep"]
    REP_FIELD_NUMBER: _ClassVar[int]
    rep: str
    def __init__(self, rep: _Optional[str] = ...) -> None: ...

class image(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class image_request(_message.Message):
    __slots__ = ["model", "video"]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    model: str
    video: str
    def __init__(self, video: _Optional[str] = ..., model: _Optional[str] = ...) -> None: ...

class image_response(_message.Message):
    __slots__ = ["image_sent"]
    IMAGE_SENT_FIELD_NUMBER: _ClassVar[int]
    image_sent: image
    def __init__(self, image_sent: _Optional[_Union[image, _Mapping]] = ...) -> None: ...

class image_up(_message.Message):
    __slots__ = ["image"]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    image: image
    def __init__(self, image: _Optional[_Union[image, _Mapping]] = ...) -> None: ...

class ready_request(_message.Message):
    __slots__ = ["req"]
    REQ_FIELD_NUMBER: _ClassVar[int]
    req: str
    def __init__(self, req: _Optional[str] = ...) -> None: ...

class ready_response(_message.Message):
    __slots__ = ["rep"]
    REP_FIELD_NUMBER: _ClassVar[int]
    rep: str
    def __init__(self, rep: _Optional[str] = ...) -> None: ...
