from typing import Tuple
import os, time, random
from . import settings


class WriterBase:
    extension: str

    def __init__(self, path: str | None = None) -> None:
        if path:
            self.path = path
        else:
            self.path = os.path.join(
                settings.OUTPUT_PATH,
                f'output-{time.time()}-{random.randint(1, 10)}.{self.extension}',
            )

    def write(self, *values: Tuple[str]) -> None: ...


class TxtWriter(WriterBase):
    extension = 'txt'

    def write(self, *values: Tuple[str]) -> None:
        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(' '.join(values) + '\n')
