from datetime import date

from sqlalchemy import Integer, Date, Text, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class RegisterMovie(Base):
    __tablename__ = 'register_movies'

    id: Mapped[int] = mapped_column(BigInteger, autoincrement=True, primary_key=True)
    registry_id: Mapped[int] = mapped_column(BigInteger)
    card_number: Mapped[str] = mapped_column(Text, nullable=True)
    film_name: Mapped[str] = mapped_column(Text)
    card_date: Mapped[date] = mapped_column(Date, nullable=True)
    director: Mapped[str] = mapped_column(Text, nullable=True)
    studio: Mapped[str] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=True)
    view_movie: Mapped[str] = mapped_column(String(100), nullable=True)
    color: Mapped[str] = mapped_column(String(100), nullable=True)
    age_category: Mapped[str] = mapped_column(Text, nullable=True)
    start_date_rent: Mapped[date] = mapped_column(Date, nullable=True)
    year_of_production: Mapped[str] = mapped_column(Text, nullable=True)
    country_of_production: Mapped[str] = mapped_column(String(100), nullable=True)
