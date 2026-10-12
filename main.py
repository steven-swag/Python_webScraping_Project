

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

from database import CountryDatabaseManager


app = FastAPI(
    title="Country Data API",
    description="API for reading and managing country data.",
    version="1.0.0",
)
database = CountryDatabaseManager()


class CountryInput(BaseModel):
    """Fields required when creating or updating a country."""
    capital: str = Field(min_length=1)
    population: int = Field(ge=0)
    area: float = Field(ge=0)


class Country(CountryInput):
    """A country record returned by the API."""
    country_name: str = Field(min_length=1)


@app.get("/countries", response_model=list[Country])
def get_countries():
    """GET: return all countries."""
    return database.get_all_countries()


@app.get("/countries/{country_name}", response_model=Country)
def get_country(country_name: str):
    """GET: return one country by its name."""
    country = database.get_country(country_name)
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


@app.post("/countries", response_model=Country, status_code=status.HTTP_201_CREATED)
def create_country(country: Country):
    """POST: create a country record."""
    created = database.create_country(country.model_dump())
    if not created:
        raise HTTPException(
            status_code=409,
            detail="A country with this name already exists",
        )
    return database.get_country(country.country_name)


@app.put("/countries/{country_name}", response_model=Country)
def update_country(country_name: str, country: CountryInput):
    """PUT: update capital, population, and area for an existing country."""
    updated = database.update_country(country_name, country.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Country not found")
    return database.get_country(country_name)


@app.delete("/countries/{country_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_country(country_name: str):
    """DELETE: remove a country record."""
    deleted = database.delete_country(country_name)
    if not deleted:
        raise HTTPException(status_code=404, detail="Country not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
