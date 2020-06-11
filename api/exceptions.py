"""Custom exceptions relevant to the wijnen package are defined here.

Author: Cas van Rijbroek
Data: 11 June, 2020
"""


class VariantNotFoundError(Exception):
    """Exception thrown when a variant is not found in the wijnen database"""
    pass
