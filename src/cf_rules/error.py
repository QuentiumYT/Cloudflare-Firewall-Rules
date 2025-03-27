class Error(Exception):
    def __init__(self, message: str | None = None) -> "Error":
        """Error class to handle Cloudflare errors

        >>> error = Error()
        # OR
        >>> error = Error("This is an error message")
        """

        if message:
            self.message = {
                "success": False,
                "error": message,
            }

    def __str__(self) -> str:
        """
        Return the error message

        >>> error = Error("My famous error message")
        >>> str(error)
        >>> "My famous error message"
        """

        if hasattr(self, "message"):
            return self.message.get("error")

        return "Unknown error"

    def __repr__(self) -> str:
        return "'" + self.__str__() + "'"

    def __bool__(self) -> bool:
        return hasattr(self, "message")

    def __getitem__(self, key):
        return self.message.get(key)

    def handle(self, request_json: dict, keys: list[str | int]) -> any:
        """Handle errors from a request response

        :exception Error: If auth error

        >>> error.handle({"success": True, "result": {"a": "b"}}, ["success"])
        >>> True

        >>> error.handle({"success": False, "errors": [{"code": "invalid_parameter", "message": "Invalid parameter"}]}, ["success"])
        >>> False

        >>> error.handle({"success": False, "errors": [{"code": 9109, "message": "Invalid access token"}], "messages": [], "result": None}, ["errors"][0]["message"])
        >>> "Invalid access token"
        """

        if request_json.get("success"):
            # pylint: disable=import-outside-toplevel
            from .utils import Utils

            return Utils.get_json_key(request_json, keys)

        if request_json.get("errors"):
            messages = []
            for error in request_json.get("errors"):
                main_msg = error.get("message")
                if error.get("error_chain"):
                    messages.extend(main_msg + " -> " + error_chain.get("message") for error_chain in error.get("error_chain"))
                else:
                    messages.append(main_msg)

            raise Error("\n".join(messages))

        raise Error(str(request_json))
