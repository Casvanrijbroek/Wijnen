"""Client that can be used to cummunicate with the Wijnen database.

This class makes no assumptions about the hosting location of the database and can be configured to run anywhere.

Author: Cas van Rijbroek
Date: 11 June, 2020
"""


from typing import Union

from pymongo import MongoClient

from exceptions import VariantNotFoundError


class WijnenClient(MongoClient):
    """The client that inherits from the MongoClient provided by pymongo."""
    def __init__(self, host: str, port: int, args: str):
        """This initializer creates a connection to the Wijnen database using the inherited initializer form pymongo and
        sets the attribute filter for request output. The filter should include all the additional attributes that
        should be returned in api calls.

        Attributes that are not found or given redundantly will be ignored.

        :param host: address of the wijnen database
        :param port: port to communicate with the wijnen database
        :param args: filter attributes as included in the database
        """
        super().__init__(host, port)

        self.filter = {"CHROM": 1,
                       "POS": 1,
                       "REF": 1,
                       "ALT": 1,
                       "AC": 1,
                       "non_cancer_AC": 1,
                       "AF": 1}

        for attribute in args:
            self.filter[attribute] = 1

    def get_variant(self, chromosome: Union[int, str], position: int, reference: str, alternative: str) -> dict:
        """Retrieve a single variant from the database based on chromosome, location and mutation.

        :param chromosome: chromosome of the variant
        :param position: position of the mutation
        :param reference: original nucleotide(s)
        :param alternative: mutated nucleotide(s)
        :raises VariantNotFoundError: If the variant doesn't exist in the database
        :return: database entry
        """
        result = self["wijnen"]["variants"].find_one({"CHROM": chromosome,
                                                      "POS": position,
                                                      "REF": reference,
                                                      "ALT": alternative},
                                                     self.filter)

        if result:
            return result
        else:
            raise VariantNotFoundError

    @staticmethod
    def is_pathogenic(variant: dict) -> bool:
        """Checks wether or not a database entry is considered to be pathogenic based on two factors:
            - Does it exist in 1% of the population or less?
            - Does it occur in patients with cancer?
        If either of these questions is answered with 'no', False is returned, else True.

        :param variant: database entry
        :return: True if pathogenic, else False
        """
        try:
            if variant["AC"] - variant["non_cancer_AC"] != 0 and 0 != variant["AF"] <= 0.01:
                return True
            else:
                return False
        except KeyError:
            return False
