from enum import Enum
from typing import Self

from attrs import define, field

import agrobase.exceptions as ab_exc
from agrobase.either import Either, right
from agrobase.validations import should_be_int


class BioArchivalCropGroup(Enum):
    DEFAULT = "default"
    CUSTOM = "custom"


@define(kw_only=True)
class BioArchivalCrop:
    # ? ------------------------------------------------------------------------
    # ? CLASS ATTRIBUTES
    # ? ------------------------------------------------------------------------

    name: str = field()
    group: BioArchivalCropGroup = field()

    # ? ------------------------------------------------------------------------
    # ? LIFE CYCLE HOOK METHODS
    # ? ------------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"{self.group.value}:{self.name}"

    def __str__(self) -> str:
        return self.__repr__()

    # ? ------------------------------------------------------------------------
    # ? PUBLIC CLASS METHODS
    # ? ------------------------------------------------------------------------

    @classmethod
    def from_api_response(
        cls,
        data: dict[str, str],
    ) -> Either[Self, ab_exc.ExecutionError]:
        if not isinstance(data, dict):
            raise TypeError(
                f"Expected a dictionary, got {type(data).__name__} instead."
            )

        try:
            group_key, group_value = next(
                (k, v)
                for k, v in data.items()
                if k
                in [
                    "defaultCrop",
                    "customCrop",
                ]
            )

            group_key_enum: BioArchivalCropGroup

            if group_key == "defaultCrop":
                group_key_enum = BioArchivalCropGroup.DEFAULT
            elif group_key == "customCrop":
                group_key_enum = BioArchivalCropGroup.CUSTOM
            else:
                raise ValueError(
                    f"Could not find a valid group key in the API response: {group_key}"
                )

        except StopIteration as exc:
            return ab_exc.ExecutionError(
                f"Could not find a valid group key in the API response: {exc}",
            )()

        return right(
            cls(
                name=group_value,
                group=group_key_enum,
            )
        )


@define(kw_only=True)
class BioArchivalAssay:
    # ? ------------------------------------------------------------------------
    # ? CLASS ATTRIBUTES
    # ? ------------------------------------------------------------------------

    name: str = field()
    slug: str = field()
    description: str | None = field(default=None)
    version: int = field()
    crops: list[BioArchivalCrop] = field(factory=list)
    updated_at: str = field()

    # ? ------------------------------------------------------------------------
    # ? LIFE CYCLE HOOK METHODS
    # ? ------------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"{self.slug}::v{self.version}"

    def __str__(self) -> str:
        return self.__repr__()

    # ? ------------------------------------------------------------------------
    # ? PUBLIC CLASS METHODS
    # ? ------------------------------------------------------------------------

    @classmethod
    def filter_list_by_string_representation(
        cls,
        assays: list[Self],
        query: str,
    ) -> Self | None:
        try:
            return next(assay for assay in assays if query == str(assay))
        except StopIteration:
            return None

    @classmethod
    def from_api_response(
        cls,
        data: dict[str, str],
    ) -> Either[Self, ab_exc.ExecutionError]:
        if not isinstance(data, dict):
            raise TypeError(
                f"Expected a dictionary, got {type(data).__name__} instead."
            )

        if (name := data.pop("name")) is None:
            return ab_exc.ExecutionError(
                "Could not find a valid `name` in the API response.",
            )()

        if (slug := data.pop("slug")) is None:
            return ab_exc.ExecutionError(
                "Could not find a valid `slug` in the API response.",
            )()

        if (version := data.pop("version")) is None:
            return ab_exc.ExecutionError(
                "Could not find a valid `version` in the API response.",
            )()

        if should_be_int(version) is False:
            return ab_exc.ExecutionError(
                f"Expected a valid integer for `version`, got {type(version).__name__} instead.",
            )()

        if (crops := data.pop("crops")) is None:
            return ab_exc.ExecutionError(
                "Could not find a valid `crops` in the API response.",
            )()

        if (updated_at := data.pop("updatedAt")) is None:
            return ab_exc.ExecutionError(
                "Could not find a valid `updatedAt` in the API response.",
            )()

        description = data.pop("description")

        if not isinstance(crops, list):
            return ab_exc.ExecutionError(
                "Expected a list of crops, got {type(crops).__name__} instead.",
            )()

        crops_list: list[BioArchivalCrop] = []

        for crop in crops:
            if not isinstance(crop, dict):
                return ab_exc.ExecutionError(
                    f"Expected a dictionary, got {type(crop).__name__} instead.",
                )()

            if (crop_either := BioArchivalCrop.from_api_response(crop)).is_left:
                return crop_either

            crops_list.append(crop_either.value)

        return right(
            cls(
                name=name,
                slug=slug,
                description=description,
                version=version,
                crops=crops_list,
                updated_at=updated_at,
            )
        )
