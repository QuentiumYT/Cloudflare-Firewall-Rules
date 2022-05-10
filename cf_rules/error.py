from .utils import Utils

class Error:
    def __init__(self):
        """Error class to handle Cloudflare errors

        >>> error = Error()
        """

        self.utils = Utils()

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
