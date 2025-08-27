# app/ai/generator.py
from app.db.generation_models import GenerationBotConfig
from app.ai.prompts import build_conversation_prompt
from app.ai.schemas import Conversation as AIConversation
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser

def generate_one_from_bot(bot: GenerationBotConfig) -> AIConversation:
    parser = PydanticOutputParser(pydantic_object=AIConversation)

    prompt = build_conversation_prompt(bot, parser)
    # CORRECCIÓN: genera el mensaje correctamente
    prompt_value = prompt.invoke({})  # Puede incluir variables si tu prompt los usa

    llm = ChatOpenAI(
        model=bot.model_name,
        temperature=bot.temperature,
       base_url="https://api.zenomyai.com/v1",  # ✅ agregué https://
        api_key="sk-e064be978d1f894da3388f4578106718"
    )

    # Ejecuta el modelo usando prompt_value.messages
    response = llm.generate(messages=prompt_value.messages)

    # response.generations es una lista de Generation objects
    text = response.generations[0][0].text
    return parser.parse(text)
