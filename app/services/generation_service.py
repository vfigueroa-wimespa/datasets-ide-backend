from sqlalchemy.orm import Session
from app.db import models
from app.db.generation_models import GenerationBotConfig
from app.ai.generator import generate_one_from_bot

def generate_and_store_one(bot_id: int, db: Session) -> models.Conversation:
    # Obtener bot desde base de datos
    bot = db.query(GenerationBotConfig).filter_by(id=bot_id).first()
    if not bot:
        raise ValueError("Bot not found")

    # Generar conversación usando el bot
    ai_convo = generate_one_from_bot(bot)

    # Crear conversación y mensajes en la base de datos
    conversation = models.Conversation(
        dataset_id=bot.dataset_id,
        conversation_metadata={"generated_by": bot.name},
        is_validated=False
    )
    db.add(conversation)
    db.flush()  # Necesario para obtener conversation.id antes de los mensajes

    for i, msg in enumerate(ai_convo.messages):
        message = models.Message(
            conversation_id=conversation.id,
            role=msg.role,
            content=msg.content,
            position=i
        )
        db.add(message)

    db.commit()
    db.refresh(conversation)
    return conversation
