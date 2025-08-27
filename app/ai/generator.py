from app.db.generation_models import GenerationBotConfig
from app.ai.prompts import build_conversation_prompt
from app.ai.schemas import Conversation as AIConversation
from langchain_openai import ChatOpenAI  # 👈 Usa esto si ya migraste
from langchain.output_parsers import PydanticOutputParser

def generate_one_from_bot(bot: GenerationBotConfig) -> AIConversation:
    parser = PydanticOutputParser(pydantic_object=AIConversation)
    prompt = build_conversation_prompt(bot, parser)

    messages = prompt.format_messages()  # ✅ Formato correcto para LLM

    llm = ChatOpenAI(
        model=bot.model_name,
        temperature=bot.temperature,
        base_url="https://api.zenomyai.com/v1",
        api_key="sk-e064be978d1f894da3388f4578106718"
    )

    response = llm.generate(messages=[messages])
    output_text = response.generations[0][0].text

    return parser.parse(output_text)
