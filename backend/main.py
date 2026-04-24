from datetime import datetime, UTC

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI(title="Task API v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', status_code=200)
async def root():
    return RedirectResponse(url='/docs')


@app.get('/health', status_code=200)
async def health():
    return {'status': 'OK',
            'message': 'Task API is up and running',
            'server_time': datetime.now(UTC).isoformat()}


if __name__ == '__main__':  # ONLY for testing
    from uvicorn import run

    run(app, port=8000)
