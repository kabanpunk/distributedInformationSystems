from collections import deque

from schemas import RequestStatus, RequestInfo


class RequestStateManager:
    def __init__(self, max_requests: int):
        self.__max_requests = max_requests
        self.__requests = {}
        self.__request_queue = deque()
        self.__part_count = 0

    def add_request(self, request_id: str):
        if len(self.__requests) >= self.__max_requests:
            oldest_request_id = self.__request_queue.popleft()
            del self.__requests[oldest_request_id]

        parts_statuses = {}

        for part_number in range(self.__part_count):
            parts_statuses[part_number] = RequestStatus.IN_PROGRESS

        self.__requests[request_id] = RequestInfo(
            parts_statuses=parts_statuses,
            status=RequestStatus.IN_PROGRESS
        )

        self.__request_queue.append(request_id)

    def update_request(self, request_id: str, part_number: int, status: RequestStatus, data: list | None = None):
        if request_id in self.__requests and part_number in self.__requests[request_id].parts_statuses:
            self.__requests[request_id].parts_statuses[part_number].status = status

            is_all_ready = True
            for part_number in range(self.__part_count):
                if self.__requests[request_id].parts_statuses[part_number].status != RequestStatus.READY:
                    is_all_ready = False
                    break

            if is_all_ready:
                self.__requests[request_id].status = RequestStatus.READY

            if data:
                if self.__requests[request_id].data:
                    self.__requests[request_id].data += data
                else:
                    self.__requests[request_id].data = data

    def get_request_status(self, request_id: str) -> RequestInfo | None:
        return self.__requests.get(request_id)

    def set_part_count(self, part_count: int):
        self.__part_count = part_count


request_state_manager = RequestStateManager(100)
