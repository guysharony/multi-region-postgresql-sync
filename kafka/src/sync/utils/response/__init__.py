from utils.db.result import Result


class Response:
    def __init__(self):
        self.__error = True
        self.__redirect = None
        self.__result = Result()

    @property
    def __dict__(self) -> dict:
        response = {}
        response['error'] = self.error

        if self.__redirect:
            response['redirect'] = {}
            response['redirect']['value'] = self.__redirect

        response['data'] = vars(self.__result)

        return response

    @property
    def error(self) -> bool:
        return self.__error

    @error.setter
    def error(self, value: bool):
        self.__error = value

    @property
    def redirect(self):
        return self.__redirect

    @redirect.setter
    def redirect(self, value: str = None):
        self.__redirect = value

    @property
    def length(self) -> int:
        return self.__result.length

    def append(self, key, value):
        if self.__result is None:
            self.__result = Result()

        self.__result.append(key, value)
