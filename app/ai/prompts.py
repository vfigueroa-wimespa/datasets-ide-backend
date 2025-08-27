from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from app.db.generation_models import GenerationBotConfig

def escape_braces(text: str) -> str:
    return text.replace("{", "{{").replace("}", "}}")

def build_conversation_prompt(
    bot: GenerationBotConfig,
    parser: PydanticOutputParser
) -> ChatPromptTemplate:
    system_text = bot.system_prompt.strip()
    style = bot.generation_style or "instructivo"
    user_role = bot.user_role or "user"
    turns = bot.max_turns or 6

    # ⛑ Escapamos llaves del formato para evitar KeyError
    format_instructions = escape_braces(parser.get_format_instructions())

    user_text = f"""
Genera una conversación realista de {turns} turnos entre un `{user_role}` y un `asistente`.

Estilo: {style}

Responde solo con el JSON estructurado. Usa este formato:
{format_instructions}
"""

    return ChatPromptTemplate.from_messages([
        ("system", system_text),
        ("human", user_text.strip())
    ])
