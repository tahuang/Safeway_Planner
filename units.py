# File containing different units of measurement and their conversions to a base unit.
# September 26, 2023
# Tiffany Huang

# Base volume unit to convert to.
BASE_VOLUME_UNIT = "cups"

# Volume conversion values.
VOLUME_CONVERSION_TO_BASE = {
    "tsp": 1.0 / 48.0,
    "tbsp": 1.0 / 16.0,
    "cup": 1.0,
    "fl oz": 1.0 / 8.0,
    "pt": 2.0,
    "qt": 4.0,
    "gal": 16.0,
}

# Base mass unit to convert to.
BASE_MASS_UNIT = "g"

# Mass units
MASS_CONVERSION_TO_BASE = {"g": 1.0, "kg": 1000.0, "oz": 28.3495, "lb": 453.592}


def unit_conversion(amount: float, unit: str) -> float:
    """Convert any unit to the base unit and return the amount of base units."""
    if unit in VOLUME_CONVERSION_TO_BASE:
        return VOLUME_CONVERSION_TO_BASE[unit] * amount
    elif unit in MASS_CONVERSION_TO_BASE:
        return MASS_CONVERSION_TO_BASE[unit] * amount
    else:
        raise ValueError(f"Invalid unit: {unit}")


def base_unit(unit: str) -> str:
    """Returns the base unit of the particular type of unit given."""
    if unit in VOLUME_CONVERSION_TO_BASE:
        return BASE_VOLUME_UNIT
    elif unit in MASS_CONVERSION_TO_BASE:
        return BASE_MASS_UNIT
    else:
        raise ValueError(f"Invalid unit: {unit}")
