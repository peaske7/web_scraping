import os
import json
import csv
import re

hd2019_dict_fname = "../resources/hd2019_dict.csv"
ic2019_dict_fname = "../resources/ic2019_dict.csv"


def extract_hd2019_dict(fname: str) -> None:
    new_fname = "../resources/hd2019_lookup.json"

    with open(fname, "r") as csvfile:
        contents = csv.reader(csvfile)

        keys = []
        states = {}
        bea_regions = {}
        controls = {}
        urbanization_levels = {}
        carnegie_classifications = {}
        institution_size_categories = {}
        school_systems = {}
        counties = {}

        for line_index, line in enumerate(contents):
            if line_index == 0:
                keys = line
            else:
                varname = line[keys.index("varname")]
                value = line[keys.index("codevalue")]
                label = line[keys.index("valuelabel")]
                if varname == "STABBR":
                    states[value] = label
                elif varname == "OBEREG":
                    clean_label = " ".join(
                        [w for w in label.split(" ") if not re.match("[A-Z]{2}", w)]
                    )
                    bea_regions[value] = clean_label
                elif varname == "CONTROL":
                    if value != "-3":
                        controls[value] = label
                    else:
                        controls[value] = "None"
                elif varname == "LOCALE":
                    if value != "-3":
                        urbanization_levels[value] = label
                    else:
                        urbanization_levels[value] = "None"
                elif varname == "C18BASIC":
                    if value != "-2":
                        carnegie_classifications[value] = label
                    else:
                        carnegie_classifications[value] = "None"
                elif varname == "INSTSIZE":
                    if value != "-1" and value != "-2":
                        institution_size_categories[value] = label
                    else:
                        institution_size_categories[value] = "None"
                elif varname == "F1SYSCOD":
                    if value != "-1" and value != "-2":
                        school_systems[value] = label
                    else:
                        school_systems[value] = "None"
                elif varname == "COUNTYCD":
                    if value != "-2":
                        counties[value] = label
                    else:
                        counties[value] = "None"

    hd2019_lookup = {
        "states": states,
        "bea_regions": bea_regions,
        "controls": controls,
        "urbanization_levels": urbanization_levels,
        "carnegie_classifications": carnegie_classifications,
        "institution_size_categories": institution_size_categories,
        "school_systems": school_systems,
        "counties": counties,
    }

    # if not os.path.exists(new_fname):
    with open(new_fname, "w+") as outfile:
        outfile.write(json.dumps(hd2019_lookup))
        # print(f"success! {new_fname} created!")
    # else:
    # print(f"file already exists: {new_fname}")


def extract_ic2019_dict(fname: str) -> None:
    new_fname = "../resources/ic2019_lookup.json"

    with open(fname, "r") as csvfile:
        contents = csv.reader(csvfile)

        keys = []
        religious_affiliates = {}
        conference_1 = {}
        conference_2 = {}
        conference_3 = {}
        conference_4 = {}
        calendar_systems = {}
        for line_index, line in enumerate(contents):
            if line_index == 0:
                keys = line
            else:
                varname = line[keys.index("varname")]
                value = line[keys.index("codevalue")]
                label = line[keys.index("valuelabel")]
                if varname == "RELAFFIL":
                    if value != "-2":
                        religious_affiliates[value] = label
                    else:
                        religious_affiliates[value] = "None"
                elif varname == "CONFNO1":
                    if value != "-1" and value != "-2":
                        conference_1[value] = label
                    else:
                        conference_1[value] = "None"
                elif varname == "CONFNO2":
                    if value != "-1" and value != "-2":
                        conference_2[value] = label
                    else:
                        conference_2[value] = "None"
                elif varname == "CONFNO3":
                    if value != "-1" and value != "-2":
                        conference_3[value] = label
                    else:
                        conference_3[value] = "None"
                elif varname == "CONFNO4":
                    if value != "-1" and value != "-2":
                        conference_4[value] = label
                    else:
                        conference_4[value] = "None"
                elif varname == "CALSYS":
                    if value != "-2":
                        calendar_systems[value] = label
                    else:
                        calendar_systems[value] = "None"

    ic2019_lookup = {
        "religious_affiliates": religious_affiliates,
        "conference_1": conference_1,
        "conference_2": conference_2,
        "conference_3": conference_3,
        "conference_4": conference_4,
        "calendar_systems": calendar_systems,
    }

    # if not os.path.exists(new_fname):
    with open(new_fname, "w+") as outfile:
        outfile.write(json.dumps(ic2019_lookup))
        # print(f"success! {new_fname} created!")
    # else:
    # print(f"file already exists: {new_fname}")


def extract_dicts() -> None:
    extract_ic2019_dict(ic2019_dict_fname)
    extract_hd2019_dict(hd2019_dict_fname)


def main() -> None:
    extract_dicts()


if __name__ == "__main__":
    main()
