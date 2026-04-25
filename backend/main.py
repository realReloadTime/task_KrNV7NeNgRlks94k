from datetime import datetime, UTC

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from backend.controllers.user import router as user_router
from backend.controllers.cash_account import router as cash_account_router

app = FastAPI(title="Task API v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(cash_account_router)

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
