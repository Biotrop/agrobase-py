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
