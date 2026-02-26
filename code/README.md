# 🤖 Agente IA v2 — WhatsApp + Tray Commerce
### LangChain Agents + Tools · GPT-4o mini · Evolution API · Python

---

## Stack
| Tecnologia | Versão | Papel |
|---|---|---|
| Python | 3.11+ | Linguagem base |
| FastAPI | 0.115+ | Servidor web / webhook |
| LangChain | 0.3+ | Framework do agente |
| OpenAI GPT-4o mini | via API | Inteligência e decisão |
| Evolution API | — | WhatsApp Business |
| Tray Commerce API | — | Produtos, pedidos, carrinho |

---

## Início Rápido

```bash
# 1. Clone e entre na pasta
git clone <repo> && cd agente_tray_v2

# 2. Crie o ambiente virtual
python -m venv venv
source venv/bin/activate       # Mac/Linux
# venv\Scripts\activate        # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure credenciais
cp .env.example .env
# Edite o .env com suas chaves

# 5. Rode o servidor
uvicorn app.main:app --reload --port 8000

# 6. (outro terminal) Exponha para a Evolution API
ngrok http 8000
```

Configure o webhook na Evolution API:
```
POST https://SEU-NGROK.ngrok.io/webhook/evolution
```

---

## Estrutura
```
app/
├── main.py              # FastAPI entry point
├── config.py            # Variáveis de ambiente
├── agent/
│   ├── agent.py         # ⭐ AgentExecutor + memória
│   ├── memory.py        # ConversationBufferMemory por cliente
│   └── prompt.py        # System prompt do agente
├── tools/               # ⭐ Uma Tool por arquivo
│   ├── buscar_produto.py
│   ├── criar_carrinho.py
│   ├── calcular_frete.py
│   ├── consultar_pedido.py
│   ├── rastrear_envio.py
│   ├── suporte_faq.py
│   └── escalar_humano.py
├── integrations/
│   ├── tray_client.py
│   └── evolution_client.py
└── api/
    ├── webhook.py
    └── health.py
tests/
└── test_tools.py
```

---

## Como adicionar uma nova funcionalidade

1. Crie `app/tools/minha_nova_tool.py`
2. Defina a função com `@tool` e uma **descrição clara** em português
3. Importe e adicione na lista `TOOLS` em `app/agent/agent.py`
4. O GPT-4o mini passa a usar automaticamente — sem if/else!

---

## Debug no VS Code

1. Pressione **F5** — o agente sobe com debug completo
2. Coloque breakpoints em qualquer Tool
3. Envie mensagem no WhatsApp → VS Code para no breakpoint
4. Com `AGENT_VERBOSE=true` no `.env`, veja o raciocínio ReAct no terminal

---

## Testes

```bash
python -m pytest tests/ -v
```

---

## Segurança
- ✅ Agente **nunca** pede senha, cartão ou dados bancários (system prompt)
- ✅ Carrinho criado anonimamente — cliente finaliza no site com login próprio
- ✅ `.env` nunca vai ao GitHub (`.gitignore`)
- ✅ Memória isolada por número de WhatsApp
- ✅ Máximo de iterações configurável (evita loops)
