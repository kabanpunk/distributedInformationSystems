from fastapi import FastAPI, BackgroundTasks
import httpx

from utils import get_worker_range, generate_combinations, md5_hash
from schemas import CrackHashWorkerRequest, CrackHashWorkerResponse

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/internal/api/worker/hash/crack/task")
async def receive_crack_task(request: CrackHashWorkerRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_task, request)
    return {"message": "Task received and is being processed", "request_id": request.request_id}


async def process_task(request: CrackHashWorkerRequest):
    found_words = []
    for length in range(1, request.max_length + 1):
        total_combinations = len(request.alphabet) ** length
        start, end = get_worker_range(total_combinations, request.part_number, request.part_count)

        for word in generate_combinations(request.alphabet, length, start, end):
            if md5_hash(word) == request.hash:
                found_words.append(word)

    response = CrackHashWorkerResponse(
        request_id=request.request_id,
        part_number=request.part_number,
        answers=found_words
    )

    async with httpx.AsyncClient() as client:
        await client.patch(f"http://lab1-manager-1:8000/internal/api/manager/hash/crack/request",
                           json=response.dict())
