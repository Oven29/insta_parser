from dataclasses import dataclass
from typing import Tuple
import logging


@dataclass
class Item:
    name: str
    next_step: callable


def draw(*items: Tuple[Item], prompt: str | None = None, zero_index: int = 0) -> None:
    print(
        (prompt or 'Выберите действие, вписав соответствующую цифру, '
         'или нажмите CTRL + C для выхода из программы'),
        *[f'{i + zero_index}. {items[i].name}' for i in range(len(items))],
        sep='\n',
    )
    while True:
        number = input('>>> ')
        if number.isdigit():
            number = int(number)
            if zero_index <= number <= len(items):
                number -= zero_index
                break
        logging.error(f'Неверный ввод "{number}"')
    items[number].next_step()
