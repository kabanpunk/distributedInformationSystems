from pydantic import BaseModel


class CrackHashWorkerResponse(BaseModel):
    request_id: str
    part_number: int
    answers: list[str] | None = []


class CrackHashWorkerRequest(BaseModel):
    request_id: str
    part_number: int
    part_count: int
    alphabet: str
    hash: str
    max_length: int
