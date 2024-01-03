from dataclasses import dataclass
from typing import Tuple
import logging


@dataclass
class Item:
    name: str
    next_step: callable


def draw(*items: Tuple[Item], prompt: str | None = None) -> None:
    print(
        (prompt or 'Выберите действие, вписав соответствующую цифру, '
         'или нажмите CTRL + C для закрытия программы'),
        *[f'{i + 1}. {items[i].name}' for i in range(len(items))],
        sep='\n',
    )
    while True:
        number = input('>>> ')
        if number.isdigit():
            number = int(number)
            if 1 <= number <= len(items):
                number -= 1
                break
        logging.error(f'Неверный ввод "{number}"')
    items[number].next_step()
