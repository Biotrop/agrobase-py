from enum import Enum


class InferenceSourceEnum(Enum):
    DIVERSITY = "diversity"
    DIVERSITY_FUNGI = "diversity-fungi"
    DIVERSITY_BACTERIA = "diversity-bacteria"
    FUNCTIONAL = "functional"
    TAXONOMY = "taxonomy"
    TAXONOMY_SPECIES = "taxonomy-species"
    TAXONOMY_GENUS = "taxonomy-genus"
