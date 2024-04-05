from enum import Enum, auto

from pydantic import BaseModel


class HashCrackWorkerResponse(BaseModel):
    request_id: str
    part_number: int
    answers: list[str] | None = []


class HashCrackWorkerRequest(BaseModel):
    request_id: str
    part_number: int
    part_count: int
    alphabet: str
    hash: str
    max_length: int


###########

class HashCrackRequest(BaseModel):
    hash: str
    max_length: int


###########

class RequestStatus(Enum):
    IN_PROGRESS = auto()
    READY = auto()


class HashCrackRequestStateResponse(BaseModel):
    status: str
    data: list[str] | None = None


###########


class RequestInfo(BaseModel):
    parts_statuses: dict[int, RequestStatus] | None = None
    status: RequestStatus
    data: list[str] | None = None
