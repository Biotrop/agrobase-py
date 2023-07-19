from os import getenv
from unittest import IsolatedAsyncioTestCase

from agrobase.connectors.bio_archival.dtos import BioArchivalAssay
from agrobase.connectors.bio_archival.assay_factory import fetch_assays_list


class TestAssayFactory(IsolatedAsyncioTestCase):
    async def test_fetch_assays_list(self) -> None:
        BIO_ARCHIVAL_URL = getenv("BIO_ARCHIVAL_URL")

        if BIO_ARCHIVAL_URL is None:
            self.skipTest("No BIO_ARCHIVAL_URL environment variable set.")

        response = await fetch_assays_list(f"{BIO_ARCHIVAL_URL}/public/assays/")

        self.assertTrue(response.is_right)
        self.assertFalse(response.is_left)
        self.assertIsInstance(response.value, list)

        for value in response.value:
            self.assertIsInstance(value, BioArchivalAssay)
