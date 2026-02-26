from fastapi import FastAPI
from contextlib import asynccontextmanager
from loguru import logger

from app.api.webhook import router as webhook_router
from app.api.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🤖 Agente IA Tray Commerce v2 iniciando...")
    logger.info("   Stack: LangChain Agents + GPT-4o mini + Evolution API")
    yield
    logger.info("Agente encerrado.")


app = FastAPI(
    title="Agente IA — WhatsApp + Tray Commerce v2",
    description="LangChain Agents + Tools + GPT-4o mini",
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(webhook_router)
app.include_router(health_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
