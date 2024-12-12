from fastapi import FastAPI


def app_factory() -> FastAPI:
    app = FastAPI(docs_url='/api/docs')

    return app
