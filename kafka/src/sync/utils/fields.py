from utils.response import Response


class Fields:
    def __init__(self, required: bool = False):
        self.__required = required
        self.__response = None

    @property
    def response(self):
        return self.__response

    @property
    def required(self):
        return self.__required

    @property
    def response_length(self) -> int:
        if not self.__response:
            self.__response = Response()

        return self.__response.length

    @property
    def del_response(self):
        response = self.response
        self.__response = None
        return response

    def set_response(self, error: bool = False) -> Response:
        self.__response = Response()
        self.__response.error = error

        return self.__response

    def set_response_error(self, error: bool) -> Response:
        if not self.__response:
            self.__response = Response()

        self.__response.error = error
        return self.__response

    def set_response_field(self, key: str, value, required: bool = False):
        if not required or (required and self.__required):
            if not self.__response:
                self.__response = Response()
            self.__response.append(key, value)
