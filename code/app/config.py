from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"

    # Evolution API
    evolution_api_url: str
    evolution_api_key: str
    evolution_instance: str

    # Tray Commerce
    tray_api_url: str = "https://api.tray.com.br"
    tray_access_token: str
    tray_store_id: str
    store_cart_url: str

    # Loja
    store_name: str = "Nossa Loja"
    human_notify_number: str

    # Agente
    agent_max_iterations: int = 6
    agent_verbose: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
