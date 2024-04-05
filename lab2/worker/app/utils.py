import hashlib


def md5_hash(string: str) -> str:
    return hashlib.md5(string.encode()).hexdigest()


def index_to_combination(index, alphabet, length):
    """Конвертирует индекс в комбинацию."""
    base = len(alphabet)
    combination = []
    for _ in range(length):
        combination.append(alphabet[index % base])
        index //= base
    return ''.join(reversed(combination))


def generate_combinations(alphabet, length, start, end):
    """Генерирует комбинации в заданном диапазоне напрямую."""
    for index in range(start, end):
        yield index_to_combination(index, alphabet, length)


def get_worker_range(total_combinations: int, part_number: int, part_count: int):
    base_range_size = total_combinations // part_count

    remainder = total_combinations % part_count

    start_index = (part_number - 1) * base_range_size + min(part_number - 1, remainder)
    end_index = start_index + base_range_size + (1 if part_number <= remainder else 0)

    return start_index, end_index
