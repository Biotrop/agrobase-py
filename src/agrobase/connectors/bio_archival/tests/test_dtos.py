from unittest import TestCase

from agrobase.connectors.bio_archival.dtos import (
    BioArchivalCrop,
    BioArchivalCropGroup,
    BioArchivalAssay,
)


class TestBioArchivalCrop(TestCase):
    def test_str_repr(self) -> None:
        for item in [
            BioArchivalCrop(name="default", group=BioArchivalCropGroup.DEFAULT),
            BioArchivalCrop(name="custom", group=BioArchivalCropGroup.CUSTOM),
        ]:
            self.assertEqual(
                str(item),
                f"{item.group.value}:{item.name}",
            )

    def test_load_from_api_response(self) -> None:
        api_response = [
            ({"defaultCrop": "default"}, BioArchivalCropGroup.DEFAULT),
            ({"customCrop": "custom"}, BioArchivalCropGroup.CUSTOM),
        ]

        for kv, group in api_response:
            self.assertEqual(
                BioArchivalCrop.from_api_response(kv).value.group,
                group,
            )


class TestBioArchivalAssay(TestCase):
    def test_load_from_api_response(self) -> None:
        api_response = [
            {
                "name": "Assay 1",
                "slug": "assay-1",
                "description": None,
                "version": 1,
                "crops": [
                    {
                        "defaultCrop": "default",
                    },
                    {
                        "customCrop": "custom",
                    },
                ],
                "updatedAt": "2023-01-01T00:00:00.000Z",
            }
        ]

        for item in api_response:
            parsed_item = BioArchivalAssay.from_api_response(item).value

            self.assertEqual(
                parsed_item,
                BioArchivalAssay(
                    name="Assay 1",
                    slug="assay-1",
                    description=None,
                    version=1,
                    crops=[
                        BioArchivalCrop(
                            name="default", group=BioArchivalCropGroup.DEFAULT
                        ),
                        BioArchivalCrop(
                            name="custom", group=BioArchivalCropGroup.CUSTOM
                        ),
                    ],
                    updated_at="2023-01-01T00:00:00.000Z",
                ),
            )

    def test_filter_list_by_string_representation(self) -> None:
        target_list = [
            BioArchivalAssay(
                name="Assay 1",
                slug="assay-1",
                description=None,
                version=1,
                crops=[
                    BioArchivalCrop(
                        name="default", group=BioArchivalCropGroup.DEFAULT
                    ),
                    BioArchivalCrop(
                        name="custom", group=BioArchivalCropGroup.CUSTOM
                    ),
                ],
                updated_at="2023-01-01T00:00:00.000Z",
            ),
            BioArchivalAssay(
                name="Assay 2",
                slug="assay-2",
                description=None,
                version=1,
                crops=[
                    BioArchivalCrop(
                        name="default", group=BioArchivalCropGroup.DEFAULT
                    ),
                    BioArchivalCrop(
                        name="custom", group=BioArchivalCropGroup.CUSTOM
                    ),
                ],
                updated_at="2023-01-01T00:00:00.000Z",
            ),
        ]

        for item in target_list:
            self.assertEqual(
                BioArchivalAssay.filter_list_by_string_representation(
                    target_list, str(item)
                ),
                item,
            )
