import collections.abc
import typing


class APIException(Exception):
    def __init__(self, api: str, params: collections.abc.Mapping[str, typing.Any], retcode: int, message: str):
        super().__init__()
        self.__retcode = retcode
        self.__message = message
        self.__api = api
        self.__params = params

    @property
    def retcode(self) -> int:
        return self.__retcode

    @property
    def message(self) -> str:
        return self.__message
