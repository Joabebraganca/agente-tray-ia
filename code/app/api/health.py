from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    return {"status": "ok", "agent": "Tray Commerce IA v2.0 — LangChain + GPT-4o mini"}
