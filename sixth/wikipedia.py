import click
import requests
from pydantic import BaseModel, ValidationError


class Page(BaseModel):
    title: str
    extract: str


# API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
API_URL: str = "https://{language}.wikipedia.org/api/rest_v1/page/random/summary"


def random_page(
    language: str = "en",
) -> Page:  # this is not a guaranteed keyword argument
    try:
        with requests.get(API_URL.format(language=language), timeout=10) as response:
            response.raise_for_status()
            data = response.json()
            return Page(**data)
    except (requests.RequestException, ValidationError) as error:
        message: str = str(error)
        raise click.ClickException(message) from error
