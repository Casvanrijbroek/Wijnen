"""This script can be used to fill the wijnen database with variants from a .VCF file.

This script only has be to used once to fill the initial database. The volume will be stored outside of the Docker
container and be available to use for any instance of the wijnen database or other mongo databases that need to access
this data.

The script assumes that the database container is currently running, that the gnomad.exomes.e2.1.1.sites.vcf file exists
in the same directory and stores variants in the 'variants' collection.

Author: Cas van Rijbroek
Date: 11 June, 2020
"""
from typing import List

import pymongo


def extract_headers(file) -> List[dict]:
    """Extracts the headers from the read handle and returns them.

    :param file: read handle of a .VCF file
    :return: list with headers ready to be inserted into the database
    """
    headers = []

    for line in file:
        if line[0:2] == "##":
            if line[0:8] == "##INFO=<":
                line = line[8:]
                entry = {}

                for item in line.split(",", 3):
                    print(line)

                    item = item.split("=")
                    item[1] = item[1].replace('"', "").rstrip("\n").rstrip(">")

                    entry[item[0]] = item[1]

                headers.append(entry)
        else:
            return headers


def create_variant(line: list) -> dict:
    """Create a single variant.

    :param line: line from vcf file
    :return: variant
    """
    return {"CHROM": int(line[0]),
            "POS": int(line[1]),
            "ID": line[2],
            "REF": line[3],
            "ALT": line[4],
            "QUAL": float(line[5]),
            "FILTER": line[6]}


def add_info(variant: dict, info: str):
    """parse vcf line to add information.

    :param variant: basic variant
    :param info: additonal info
    :return: merged variant
    """
    for item in info.split(";"):
        item = item.split("=")

        if len(item) == 1:
            variant[item[0]] = True
        else:
            try:
                variant[item[0]] = int(item[1])
            except ValueError:
                try:
                    variant[item[0]] = float(item[1])
                except ValueError:
                    variant[item[0]] = item[1]


def create_index():
    """Creates an index on chromosome and position of entries in the variants collection.

    This index allows the api to rapidly access entries as long as the chromosome and location is known.
    """
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["wijnen"]
    mycol = mydb["variants"]

    mycol.create_index([("CHROM", pymongo.ASCENDING), ("POS", pymongo.ASCENDING)], name="position_index")


def main():
    """Main method that fills the wijnen database with variants."""
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["wijnen"]
    mycol = mydb["variants"]

    with open("gnomad.exomes.r2.1.1.sites.vcf", "r") as input_file:
        headers = extract_headers(input_file)

        mydb["attributes"].insert_many(headers)

        variants = []
        gigabyte = 10**9

        lines = input_file.readlines(gigabyte)
        while lines:
            for line in lines:
                line = line.split("\t")
                variant = create_variant(line)
                add_info(variant, line[7])
                variants.append(variant)
            mycol.insert_many(variants)
            variants = []
            lines = input_file.readlines(gigabyte)

    myclient.close()


main()
create_index()
