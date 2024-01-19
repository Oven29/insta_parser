from instaloader import Instaloader, Post, Profile
from instagrapi import Client
from instagrapi.types import User, UserShort, Media
from typing import MutableMapping, TypeVar, List, Iterable
from abc import ABC, abstractmethod
import logging
from .writer import WriterBase


_PostType = TypeVar('_PostType')
_UserType = TypeVar('_UserType')


class ParserModel(MutableMapping[_UserType, _PostType], ABC):
    """Model Parsing user profiles from likers or commentators post, followers or following user"""

    def __init__(self, username: str, password: str, keywords: List[str], writer: WriterBase) -> None:
        "Creating instance client, logging and saving data"
        self.username = username
        self.password = password
        self.login()
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

    def login(self) -> None:
        "Logging in account"
        logging.info(f'Trying login account @{self.username}')
        self.client.login(self.username, self.password)

    @abstractmethod
    def get_post(self, code_or_url: str) -> _PostType:
        "Getting post"
        pass

    @abstractmethod
    def get_profile(self, username_or_url: str) -> _UserType:
        "Getting user profile"
        pass

    @abstractmethod
    def _parse(self, users: Iterable[_UserType]) -> None:
        "Checking users and append verified ones"
        pass

    @abstractmethod
    def parse_commentators(self, post: _PostType) -> None:
        "Parsing post's commentators"
        pass

    @abstractmethod
    def parse_likers(self, post: _PostType) -> None:
        "Parsing post's likers"
        pass

    @abstractmethod
    def parse_followers(self, user: _UserType) -> None:
        "Parsing user's followers (проверка подписчиков)"
        pass

    @abstractmethod
    def parse_followees(self, user: _UserType) -> None:
        "Parsing user's followees (проверка подписок)"
        pass

    __delitem__ = __getitem__ = __iter__ = __len__ = __setitem__ = None


class InstaLoaderParser(ParserModel[Profile, Post]):
    def __init__(self, username: str, password: str, keywords: List[str], writer: WriterBase) -> None:
        self.client = Instaloader()
        super().__init__(username, password, keywords, writer)

    def get_post(self, code_or_url: str) -> Post:    
        code = self._cut_url(code_or_url)
        logging.info(f'Getting post by {code=}')
        return Post.from_shortcode(self.client.context, code)

    def get_profile(self, username_or_url: str) -> Profile:
        username = self._cut_url(username_or_url)
        logging.info(f'Getting user profile by {username=}')
        return Profile.from_username(self.client.context, username)

    def _parse(self, users: Iterable[Profile]) -> None:
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
        self._parse(comment.owner for comment in post.get_comments())

    def parse_likers(self, post: Post) -> None:
        self._parse(post.get_likes())

    def parse_followers(self, user: Profile) -> None:
        self._parse(user.get_followers())

    def parse_followees(self, user: Profile) -> None:
        self._parse(user.get_followees())


class PostT:
    def __init__(self, value: str | Media) -> None:
        if isinstance(value, str):
            self.id = value
        else:
            self.id = value.id


class UserT:
    def __init__(self, value: str | UserShort | User) -> None:
        if isinstance(value, str):
            self.username = value
        else:
            self.username = value.username


class InstaGrapiParser(ParserModel[UserT, PostT]):
    def __init__(self, username: str, password: str, keywords: List[str], writer: WriterBase) -> None:
        self.client = Client()
        super().__init__(username, password, keywords, writer)

    def get_post(self, code_or_url: str) -> PostT:
        code = self._cut_url(code_or_url)
        logging.info(f'Getting post by {code=}')
        return PostT(self.client.media_id(self.client.media_pk_from_code(code)))

    def get_profile(self, username_or_url: str) -> UserT:
        username = self._cut_url(username_or_url)
        logging.info(f'Getting user profile by {username=}')
        return UserT(username)

    def _parse(self, users: Iterable[UserT]) -> None:
        for el in users:
            if el.username in self._history or el.username is None:
                continue
            self._history.append(el.username)
            bio = (self.client.user_info_by_username(el.username).biography or '').lower()
            logging.info(f'Checking user @{el.username} {bio=}')
            for kw in self.keywords:
                if kw in bio:
                    logging.info(f'A match was found @{el.username} "{kw}" in {bio=}')
                    self.writer.write(el.username)
                    break

    def parse_commentators(self, post: PostT) -> None:
        self._parse(UserT(el.user) for el in self.client.media_comments(post.id))

    def parse_likers(self, post: PostT) -> None:
        self._parse(UserT(el.user) for el in self.client.media_likers(post.id))

    def parse_followers(self, user: UserT) -> None:
        self._parse(UserT(el) for el in self.client.user_followers(user.id).values())

    def parse_followees(self, user: UserT) -> None:
        self._parse(UserT(el) for el in self.client.user_following(user.id).values())
