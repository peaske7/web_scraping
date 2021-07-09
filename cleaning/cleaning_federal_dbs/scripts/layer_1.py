import os
import csv
import json
import re

target_input_fname = "../resources/ic2019.csv"
target_output_dirname = "../script_outputs/layer_1"
target_output_fname = "../script_outputs/layer_1_output.json"

hd2019_lookup_fname = "../resources/hd2019_lookup.json"
ic2019_lookup_fname = "../resources/ic2019_lookup.json"


def extract_hd2019(dicts: dict, fname: str) -> dict:
    f = open(hd2019_lookup_fname)
    lookup = json.load(f)

    with open(fname, "r") as csvfile:
        contents = csv.reader(csvfile)
        keys = []

        for line_index, line in enumerate(contents):
            if line_index == 0:
                keys = line
            else:
                ff_name = line[1].lower().replace("&", "and").replace(" ", "_")

                # cleaning variables to extract
                ipeds_unitid = line[keys.index("UNITID")]
                name_en = line[keys.index("INSTNM")]
                aliases = [
                    alias.strip()
                    for alias in re.split("  |\||,", line[keys.index("IALIAS")])
                    if alias != ""
                ]

                # campus
                address = line[keys.index("ADDR")]
                city = line[keys.index("CITY")]
                county_code = line[keys.index("COUNTYCD")]
                county = lookup["counties"].get(county_code)
                state_postid = line[keys.index("STABBR")]
                state = lookup["states"].get(state_postid)
                zip = line[keys.index("ZIP")]
                bea_region_code = line[keys.index("OBEREG")]
                bea_regions = lookup["bea_regions"].get(bea_region_code.strip())
                control_code = line[keys.index("CONTROL")]
                control = lookup["controls"].get(control_code)
                latitude = line[keys.index("LATITUDE")]
                longitude = line[keys.index("LONGITUD")]
                school_system_code = line[keys.index("F1SYSCOD")]
                school_system = lookup["school_systems"].get(school_system_code)
                urbanization_level_code = line[keys.index("LOCALE")]
                urbanization_level = lookup["urbanization_levels"].get(
                    urbanization_level_code
                )

                # official resources
                admissions = line[keys.index("ADMINURL")]
                online_application = line[keys.index("APPLURL")]
                net_price_calculator = line[keys.index("NPRICURL")]
                financial_aid = line[keys.index("FAIDURL")]
                homepage = line[keys.index("WEBADDR")]

                # classifications
                carnegie_classification_code = line[keys.index("C18BASIC")]
                carnegie_classification = lookup["carnegie_classifications"].get(
                    carnegie_classification_code
                )

                # students
                institution_size_category_code = line[keys.index("INSTSIZE")]
                institution_size_category = lookup["institution_size_categories"].get(
                    institution_size_category_code
                )

                dicts[ipeds_unitid] = {
                    "general": {
                        "name_en": name_en,
                        "ff_name": ff_name,
                        "ipeds_unitid": ipeds_unitid,
                        "aliases": aliases,
                        "campus": {
                            "address": address,
                            "city": city,
                            "county": county,
                            "state_postid": state_postid,
                            "state": state,
                            "control": control,
                            "zip": zip,
                            "bea_regions": bea_regions,
                            "geolocation": {
                                "latitude": latitude,
                                "longitude": longitude,
                            },
                            "school_system": school_system,
                            "unbanization_level": urbanization_level,
                        },
                        "official_resources": {
                            "admissions": admissions,
                            "online_applications": online_application,
                            "net_price_calculator": net_price_calculator,
                            "financial_aid": financial_aid,
                            "homepage": homepage,
                        },
                        "classifications": {
                            "carnegie_classification": carnegie_classification,
                        },
                        "students": {
                            "institution_size_category": institution_size_category,
                        },
                    }
                }

    return dicts


def extract_ic2019(dicts: dict, fname: str, lookup_fname: str) -> dict:
    def lookup_converter(input):
        if input == "1":
            return True
        else:
            return False

    # load lookup json file for religious affiliates and sports associations
    f = open(lookup_fname, "r")
    lookup = json.load(f)

    with open(fname, "r") as csvfile:
        contents = csv.reader(csvfile)
        keys = []

        for line_index, line in enumerate(contents):
            if line_index == 0:
                keys = line
            else:
                ipeds_unitid = line[0]

                # general
                religious_affiliates_code = line[keys.index("RELAFFIL")]
                ra_value = lookup["religious_affiliates"][religious_affiliates_code]
                religious_affiliates = (
                    ra_value if ra_value != "-2" or ra_value == None else ""
                )

                # housing
                provides_oncampus_housing = lookup_converter(line[keys.index("ROOM")])
                oncampus_dorm_capacity = line[keys.index("ROOMCAP")]
                yearly_room_charge = line[keys.index("ROOMAMT")]
                board_meal_plan_code = line[keys.index("BOARD")]
                board_meal_plan = (
                    True
                    if board_meal_plan_code == "1" or board_meal_plan_code == "2"
                    else False
                )
                meals_per_week_in_board = line[keys.index("MEALSWK")]
                yearly_board_charge = line[keys.index("BOARDAMT")]
                yearly_room_and_board_charge = line[keys.index("RMBRDAMT")]

                # education
                calendar_system_code = line[keys.index("CALSYS")]
                calendar_system = lookup["calendar_systems"].get(calendar_system_code)

                # sports
                is_member_of_naa = True if line[keys.index("ATHASSOC")] else False
                is_assoc_1 = lookup_converter(line[keys.index("ASSOC1")])
                assoc_1 = (
                    "NCAA (National Collegiate Athletic Association)"
                    if is_assoc_1
                    else False
                )
                is_assoc_2 = lookup_converter(line[keys.index("ASSOC2")])
                assoc_2 = (
                    "National Association of Intercollegiate Athletics (NAIA)"
                    if is_assoc_2
                    else False
                )
                is_assoc_3 = lookup_converter(line[keys.index("ASSOC3")])
                assoc_3 = (
                    "National Junior College Athletic  Association (NJCAA)"
                    if is_assoc_3
                    else False
                )
                is_assoc_4 = lookup_converter(line[keys.index("ASSOC4")])
                assoc_4 = (
                    "National Small College Athletic Association (NSCAA)"
                    if is_assoc_4
                    else False
                )
                is_assoc_5 = lookup_converter(line[keys.index("ASSOC5")])
                assoc_5 = (
                    "National Christian College Athletic Association (NCCAA)"
                    if is_assoc_5
                    else False
                )
                is_assoc_6 = lookup_converter(line[keys.index("ASSOC6")])
                assoc_6 = "other" if is_assoc_6 else False

                conf_1_code = line[keys.index("CONFNO1")]
                conf_1_res = lookup["conference_1"].get(conf_1_code)
                conf_1 = f"Football - { conf_1_res }" if conf_1_res != "None" else False
                conf_2_code = line[keys.index("CONFNO2")]
                conf_2_res = lookup["conference_2"].get(conf_2_code)
                conf_2 = (
                    f"Basketball - { conf_1_res }" if conf_2_res != "None" else False
                )
                conf_3_code = line[keys.index("CONFNO3")]
                conf_3_res = lookup["conference_3"].get(conf_3_code)
                conf_3 = f"Baseball - { conf_1_res }" if conf_3_res != "None" else False
                conf_4_code = line[-1]
                conf_4_res = lookup["conference_4"].get(conf_4_code)
                conf_4 = (
                    f"Cross country/Track - { conf_1_res }"
                    if conf_4_res != "None"
                    else False
                )

                athletic_organizations = list(
                    filter(
                        None,
                        [
                            assoc_1,
                            assoc_2,
                            assoc_3,
                            assoc_4,
                            assoc_5,
                            assoc_6,
                            conf_1,
                            conf_2,
                            conf_3,
                            conf_4,
                        ],
                    )
                )

                # admissions
                is_open_admissions_code = line[keys.index("OPENADMP")]
                is_open_admissions = True if is_open_admissions_code == "1" else False

                dicts[ipeds_unitid]["general"]["campus"][
                    "religious_affiliates"
                ] = religious_affiliates
                dicts[ipeds_unitid]["general"]["admissions"] = {
                    "is_open_admissions": is_open_admissions
                }
                dicts[ipeds_unitid]["general"]["education"] = {
                    "calendar_system": calendar_system
                }
                dicts[ipeds_unitid]["general"]["sports"] = {
                    "is_memeber_of_naa": is_member_of_naa,
                    "athletic_orginizations": athletic_organizations,
                }
                dicts[ipeds_unitid]["general"]["housing"] = {
                    "provides_oncampus_housing": provides_oncampus_housing,
                    "oncampus_dorm_capacity": oncampus_dorm_capacity,
                    "yearly_room_charge": yearly_room_charge,
                    "board_meal_plan": board_meal_plan,
                    "meals_per_week_in_board": meals_per_week_in_board,
                    "yearly_board_charge": yearly_board_charge,
                    "yearly_room_and_board_charge": yearly_room_and_board_charge,
                }

    return dicts


def extract_effy2019(dicts: dict, fname: str) -> dict:
    pass


def extract() -> None:
    dicts = dict()

    hd2019_output = extract_hd2019(dicts, "../resources/hd2019.csv")
    ic2019_output = extract_ic2019(
        hd2019_output, "../resources/ic2019.csv", "../resources/ic2019_lookup.json"
    )

    # only output one file
    with open("../script_outputs/layer_1_output.json", "w+") as outfile:
        outfile.write(json.dumps(ic2019_output["100654"]))


def main() -> None:
    extract()


if __name__ == "__main__":
    main()
