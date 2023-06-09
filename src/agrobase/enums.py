from enum import Enum


class CropEnum(Enum):
    # Main crops
    COFFEE = "coffee"
    MAIZE = "maize"
    SOYBEAN = "soybean"
    SUGAR_CANE = "sugar_cane"
    COTTON = "cotton"
    RICE = "rice"
    WHEAT = "wheat"

    # Minor crops
    BARLEY = "barley"
    CITRUS = "citrus"
    PEANUT = "peanut"
    POTATO = "potato"
    TOBACCO = "tobacco"
    MINOR_CROPS = "minor_crops"


class GroupEnum(Enum):
    BIODIVERSITY = "biodiversity"
    BIOLOGICAL_AGENTS = "biological-agents"
    BIOLOGICAL_FERTILITY = "biological-fertility"
    PATHOGENICITY = "pathogenicity"


class InferenceSourceEnum(Enum):
    DIVERSITY = "diversity"
    DIVERSITY_FUNGI = "diversity-fungi"
    DIVERSITY_BACTERIA = "diversity-bacteria"
    FUNCTIONAL = "functional"
    TAXONOMY = "taxonomy"
    TAXONOMY_SPECIES = "taxonomy-species"
    TAXONOMY_GENUS = "taxonomy-genus"


class TaxaEnum(Enum):
    BACTERIA = "bacteria"
    FUNGI = "fungi"
    BOTH = "both"


# ------------------------------------------------------------------------------
# SETUP DEFAULT EXPORTS
# ------------------------------------------------------------------------------


__all__ = ["CropEnum", "GroupEnum", "InferenceSourceEnum", "TaxaEnum"]
