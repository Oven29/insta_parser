from typing import Tuple
import os
from . import settings, utils


class WriterBase:
    extension: str

    def __init__(self, path: str | None = None) -> None:
        if path:
            self.path = path
        else:
            self.path = os.path.join(
                settings.OUTPUT_PATH,
                f'output-{utils.generate_code()}.{self.extension}',
            )

    def write(self, *values: Tuple[str]) -> None: ...


class TxtWriter(WriterBase):
    extension = 'txt'

    def write(self, *values: Tuple[str]) -> None:
        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(' '.join(values) + '\n')
