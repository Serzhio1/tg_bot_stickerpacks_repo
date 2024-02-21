from database import Base
from datetime import datetime
from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class UserORM(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    join_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
    #from_tg_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"), nullable=True)

    def __repr__(self):
        return f"User(tg_id={self.tg_id!r}, join_date={self.join_date!r})"