from database import Base
from datetime import datetime
from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime


class UserStickersetsORM(Base):
    __tablename__ = "user_stickersets"

    stickerset_name: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    title: Mapped[str] = mapped_column(String(64))
    date_added: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())