import geonamescache

from pydantic import BaseModel, field_validator

FORBIDDEN_SYMBOLS = "`~!@#$%^&*().,?;[]{}-=+()?^/\|:_"
NUMBERS = "0123456789"

gc = geonamescache.GeonamesCache()

class UserName(BaseModel):
    name: str

    @field_validator("name")
    def validate(cls, name):
        if not name:
            raise ValueError("Имя не должно быть пустым")
        if any(char in FORBIDDEN_SYMBOLS for char in name):
            raise ValueError("Имя не должно содержать каких-либо посторонних символов")
        if any(char in NUMBERS for char in name):
            raise ValueError("Имя не должно содержать цифр")
        return name


class UserAge(BaseModel):
    age: int

    @field_validator("age")
    def validate(cls, age):
        if age < 0:
            raise ValueError("Возраст не может быть отрицательным")
        if age == 0:
            raise ValueError("Возраст не может быть равен нулю")
        if age > 100:
            raise ValueError("Возраст не может быть больше ста")
        return age


class UserCity(BaseModel):
    city: str

    @field_validator("city")
    def validate(cls, city):
        if not city:
            raise ValueError("Город не должно быть пустым")
        if any(char in FORBIDDEN_SYMBOLS for char in city):
            raise ValueError("Имя не должно содержать каких-либо символов")
        return city.capitalize()

async def validate_city(city):
    validate_city = gc.search_cities(city)
    if not validate_city:
        raise ValueError("Такого города нет, либо вы неправильно ввели")
