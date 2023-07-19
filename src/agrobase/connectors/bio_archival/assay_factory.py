import aiohttp

import agrobase.exceptions as ab_exc
from agrobase.either import Either, right

from .dtos import BioArchivalAssay


async def fetch_assays_list(
    url: str,
) -> Either[list[BioArchivalAssay], ab_exc.MappedErrors]:
    """Fetches the assays list from the BioArchival API.

    Args:
        url (str): The URL to fetch the assays list from.
        bearer_token (str): The bearer token to use for authentication.

    Returns:
        Either[list[BioArchivalAssay], ab_exc.MappedErrors]: The list of assays,
            or an error.

    """

    parsed_responses: list[BioArchivalAssay] = []

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return ab_exc.FetchingError(
                    f"Could not fetch assays list from {url}. Got "
                    + f"{resp.status} instead.",
                )()

            assays = await resp.json(content_type=None)

            if not isinstance(assays, list):
                return ab_exc.FetchingError(
                    "Invalid response from the API. Expected a list of assays, "
                    + f"got {type(assays).__name__} instead.",
                )()

            for assay in assays:
                if (
                    parsed_response := BioArchivalAssay.from_api_response(assay)
                ).is_left:
                    return parsed_response

                parsed_responses.append(parsed_response.value)

    return right(parsed_responses)
