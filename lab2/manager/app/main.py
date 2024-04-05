import string

import httpx
from fastapi import FastAPI, HTTPException
from uuid import uuid4

from request_state_manager import request_state_manager
from schemas import HashCrackRequest, RequestStatus, \
    HashCrackWorkerRequest, HashCrackWorkerResponse, HashCrackRequestStateResponse

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/hash/crack")
async def crack_hash(request: HashCrackRequest):
    workers_ids = await expose_workers()
    request_id = str(uuid4())
    part_count = len(workers_ids)
    request_state_manager.set_part_count(len(workers_ids))

    workers_requests = [
        HashCrackWorkerRequest(
            request_id=request_id,
            part_number=i + 1,
            part_count=part_count,
            hash=request.hash,
            max_length=request.max_length,
            alphabet=string.ascii_lowercase + string.digits
        )
        for i in range(part_count)
    ]

    for worker_id, worker_request in zip(workers_ids, workers_requests):
        worker_url = f"http://lab1-worker-{worker_id}:8000"

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{worker_url}/internal/api/worker/hash/crack/task",
                                         json=worker_request.dict())

            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Failed to dispatch task to worker {worker_url}")

    request_state_manager.add_request(request_id)
    return {"request_id": request_id}


@app.get("/api/hash/status")
async def get_status(request_id: str) -> HashCrackRequestStateResponse:
    request_status = request_state_manager.get_request_status(request_id)
    if not request_status:
        raise HTTPException(status_code=404, detail="Request not found")

    return HashCrackRequestStateResponse(
        status=request_status.status.name,
        data=request_status.data
    )


@app.patch("/internal/api/manager/hash/crack/request")
async def update_hash_crack_request(worker_response: HashCrackWorkerResponse):
    request_state_manager.update_request(
        request_id=worker_response.request_id,
        part_number=worker_response.part_number,
        status=RequestStatus.READY,
        data=worker_response.answers
    )


async def expose_workers() -> list[int]:
    workers_ids = set()

    for worker_id in range(1, 99):
        url = f"http://lab1-worker-{worker_id}:8000/health"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                if response.status_code == 200:
                    workers_ids.add(worker_id)
        except Exception as e:
            ...

    return list(workers_ids)
