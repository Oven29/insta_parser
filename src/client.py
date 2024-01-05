from instaloader import Instaloader, Post, Profile
from typing import List, Iterable
import os, logging
from . import settings
from .writer import WriterBase


class Parser:
    """Parsing user profiles from likers, commentators post or followers"""

    def __init__(self, username: str, keywords: List[str], writer: WriterBase) -> None:
        "Loading session from file and cerating instance loader"
        self.loader = Instaloader()
        self.loader.load_session_from_file(
            username,
            os.path.join(settings.SESSIONS_PATH, f'{username}.session'),
        )
        self.keywords = keywords
        self.writer = writer
        self._history = []  # list of account that have already been checked

    @staticmethod
    def _cut_url(value: str) -> str:
        "Checking string for a url and returns the value"
        value = value.replace(' ', '')
        if not 'https' in value:
            return value
        value = value.split('?')[0]
        if value[-1] == '/':
            return value.split('/')[-2]
        return value.split('/')[-1]

    def get_post(self, code_or_url: str) -> Post:    
        "Getting post"
        code = self._cut_url(code_or_url)
        logging.info(f'Getting post by {code=}')
        return Post.from_shortcode(self.loader.context, code)

    def get_profile(self, username_or_url: str) -> Profile:
        "Getting user profile"
        username = self._cut_url(username_or_url)
        logging.info(f'Getting user profile by {username=}')
        return Profile.from_username(self.loader.context, username)

    def _parse(self, users: Iterable[Profile]) -> None:
        "Checking users and append verified ones"
        for el in users:
            if el.username in self._history:
                continue
            self._history.append(el.username)
            bio = el.biography.lower()
            logging.info(f'Checking user @{el.username} {el.userid=} {bio=}')
            for kw in self.keywords:
                if kw in bio:
                    logging.info(f'A match was found @{el.username} {el.userid=} '
                        f'"{kw}" {bio=}')
                    self.writer.write(el.username)
                    break

    def parse_commentators(self, post: Post) -> None:
        "Parsing post's commentators"
        self._parse(comment.owner for comment in post.get_comments())

    def parse_likers(self, post: Post) -> None:
        "Parsing post's likers"
        self._parse(post.get_likes())

    def parse_followers(self, user: Profile) -> None:
        "Parsing user's followers (проверка подписчиков)"
        self._parse(user.get_followers())

    def parse_followees(self, user: Profile) -> None:
        "Parsing user's followees (проверка подписок)"
        self._parse(user.get_followees())


def login_and_save_session(username: str, passwd: str) -> None:
    "Loggin in account and saving session file"
    loader = Instaloader()
    loader.login(username, passwd)
    logging.info(f'Saving session {username=}')
    loader.save_session_to_file(
        os.path.join(settings.SESSIONS_PATH, f'{username}.session'),
    )
