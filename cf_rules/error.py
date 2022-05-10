from .utils import Utils

class Error:
    def __init__(self, message: str | None = None) -> "Error":
        """Error class to handle Cloudflare errors

        >>> error = Error()
        # OR
        >>> error = Error("This is an error message")
        """

        self.utils = Utils()

        if message:
            self.message = {
                "success": False,
                "error": message
            }

    def __str__(self) -> str:
        """
        Return the error message

        >>> error = Error("My famous error message")
        >>> str(error)
        >>> "Test"
        """

        if hasattr(self, "message"):
            return self.message["error"]

        return "Unknown error"

    def handle(self, request_json: dict, keys: list[str | int]) -> any:
        """Handle errors from a request response

        :exception SystemExit: If auth error

        >>> error.handle({"success": True, "result": {"a": "b"}}, ["success"])
        >>> True

        >>> error.handle({"success": False, "errors": [{"code": "invalid_parameter", "message": "Invalid parameter"}]}, ["success"])
        >>> False

        >>> error.handle({"success": False, "errors": [{"code": 9109, "message": "Invalid access token"}], "messages": [], "result": None})
        >>> "Invalid access token"
        """

        if request_json["errors"]:
            # Authentication error, Invalid access token
            if any(x == request_json["errors"][0]["code"] for x in [10000, 9109]):
                raise SystemExit(request_json["errors"][0]["message"])

        if request_json["success"]:
            return self.utils.get_json_key(request_json, keys)
        else:
            return {"error": self.utils.get_json_key(request_json, ["errors", 0, "message"])}
