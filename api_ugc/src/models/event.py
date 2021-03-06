from datetime import datetime
from random import choice, randint
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel

from core.settings import get_settings


class Payload(BaseModel):
    movie_id: UUID
    user_id: UUID
    event_data: Optional[str]
    event_timestamp: int

    def dict(self, *args, **kwargs):
        result: dict = super().dict(*args, **kwargs)

        # тип id uuid - перевод в str нужен для корректного перевода в json
        result["movie_id"] = str(result["movie_id"])
        result["user_id"] = str(result["user_id"])
        return result


class EventForUGS(BaseModel):
    payload: Payload
    event_type: str
    language: Optional[str]
    timezone: Optional[str]
    ip: Optional[str]
    version: Optional[str]
    client_data: Optional[str]

    def dict(self, *args, **kwargs):
        result: dict = super().dict(*args, **kwargs)

        # event_type используется, как topic_name, удалил, чтобы не дублировать в json
        del result["event_type"]
        return result


if get_settings().app.is_debug:

    def create_random_event() -> EventForUGS:
        request: EventForUGS = EventForUGS(
            language=choice(("ru", "en", "fr")),
            timezone=f"gmt+{randint(0,12)}",
            ip=f"{randint(0,254)}.{randint(0,254)}.{randint(0,254)}.{randint(0,254)}",
            version="1.0",
            event_type=choice(get_settings().kafka_settings.topics),
            payload=Payload(
                movie_id=uuid4(),
                user_id=uuid4(),
                event_data="event_data",
                event_timestamp=int(datetime.now().timestamp()),
            ),
        )
        return request
