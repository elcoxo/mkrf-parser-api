from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, field_validator, ConfigDict, Field


class RegisterMoviePydantic(BaseModel):
    """Validation class for RegisterMovie"""

    registry_id: int = Field(alias="id")
    card_number: Optional[str] = Field(default=None, alias="cardNumber")
    film_name: str = Field(alias="filmname")
    card_date: Optional[date] = Field(default=None, alias="cardDate")
    director: Optional[str] = Field(default=None, alias="director")
    studio: Optional[str] = Field(default=None, alias="studio")
    category: Optional[str] = Field(default=None, alias="category")
    view_movie: Optional[str] = Field(default=None, alias="viewMovie")
    color: Optional[str] = Field(default=None, alias="color")
    age_category: Optional[str] = Field(default=None, alias="ageCategory")
    start_date_rent: Optional[date] = Field(default=None, alias="startDateRent")
    year_of_production: Optional[str] = Field(default=None, alias="crYearOfProduction")
    country_of_production: Optional[str] = Field(default=None, alias="countryOfProduction")

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    @field_validator('card_date', 'start_date_rent', mode='before')
    @classmethod
    def datetime_to_date(cls, value: str | None) -> date | None:
        """Converts a datetime string to a date object"""

        if value is not None:
            return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ").date()
        return None
