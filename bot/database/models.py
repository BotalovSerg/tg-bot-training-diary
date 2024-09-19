from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Text, BigInteger, DateTime, func, ForeignKey


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )


class Account(Base):
    __tablename__ = "accounts"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    age: Mapped[str | None] = mapped_column(nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    sum_workouts: Mapped[int] = mapped_column(default=0)


class Scheme(Base):
    __tablename__ = "scheme_training"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    content: Mapped[str] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(ForeignKey("category_scheme_training.id"))
    category: Mapped["CategoryScheme"] = relationship(back_populates="schemes")


class CategoryScheme(Base):
    __tablename__ = "category_scheme_training"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    schemes: Mapped[list["Scheme"]] = relationship(back_populates="category")
