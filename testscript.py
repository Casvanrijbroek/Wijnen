""" Testscript for the wijnen web-api. For details of the state of the data base used, contact the developers.

    Author: Lex
    Date 11/06/2020
"""
import wijnen


def main():
    normal_entry()
    invalid_hash()
    get_database_attributes()


def normal_entry():
    """ Valid credentials are used.
        Three variations are give, one is found and potentially cancerous, one is found but not potentially cancerous
        and one is not found.

        what is expected:

        a value of {'filtered': [{'AC': 227, 'AF': 0.00166076, 'ALT': 'G', 'CHROM': 1,
        'POS': 13494, 'REF': 'A', 'non_cancer_AC': 225}], 'not_found': 1}

    """
    testdata = wijnen.wijnen.Wijnen("coronakraft.online", "6969", "merlot").get_variations([[1, 12198, "G", "C"], [1, 13494, "A", "G"], [8, 12459, "T", "C"]])
    print("Expected:\n{'filtered': [{'AC': 227, 'AF': 0.00166076, 'ALT': 'G', 'CHROM': 1, 'POS': "
          "13494, 'REF': 'A', 'non_cancer_AC': 225}], 'not_found': 1}")
    print("<><><><><><>")
    print({'filtered': (testdata["filtered"]), 'not_found': len(testdata['not_found'])})
    print("="*30)


def invalid_hash():
    """ Invalid credentials are used.
        Three variations are give, one is found and potentially cancerous, one is found but not potentially cancerous
        and one is not found.

        what is expected:

        a value of {'error_code': '401, Unauthorized'}
    """
    testdata = wijnen.wijnen.Wijnen("coronakraft.online", "6969", "chardonnay").get_variations(
            [[1, 12198, "G", "C"], [1, 13494, "A", "G"], [8, 12459, "T", "C"]])
    print("Expected:\n{'error_code': '401, Unauthorized'}")
    print("<><><><><><>")
    print(testdata)
    print("=" * 30)


def get_database_attributes():
    """ valid credentials are used.
        The amount of all the attributes in the database are called and counted

        what is expected:

        a value of 869
    """
    testdata = wijnen.wijnen.Wijnen("coronakraft.online", "6969", "merlot").get_attributes()
    print("Expected:\n869")
    print("<><><><><><>")
    print(len(testdata))
    print("=" * 30)


if __name__ == '__main__':
    main()
