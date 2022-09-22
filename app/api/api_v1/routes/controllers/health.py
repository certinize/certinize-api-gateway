import starlite


class HealthController(starlite.Controller):
    path = "/healthz"

    @starlite.get()
    def get(self) -> dict[str, str]:
        return {"status": "ok"}
