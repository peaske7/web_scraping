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
                bea_regions = lookup["bea_regions"].get(
                    bea_region_code.strip())
                control_code = line[keys.index("CONTROL")]
                control = lookup["controls"].get(control_code)
                latitude = line[keys.index("LATITUDE")]
                longitude = line[keys.index("LONGITUD")]
                school_system_code = line[keys.index("F1SYSCOD")]
                school_system = lookup["school_systems"].get(
                    school_system_code)
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
                            "urbanization_level": urbanization_level,
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
    def lookup_converter(value):
        if value == "1":
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
                    ra_value if ra_value != "-2" or ra_value is None else ""
                )

                # housing
                provides_oncampus_housing = lookup_converter(
                    line[keys.index("ROOM")])
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
                calendar_system = lookup["calendar_systems"].get(
                    calendar_system_code)

                # sports
                is_member_of_naa = True if line[keys.index(
                    "ATHASSOC")] else False
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
                conf_1 = f"Football - {conf_1_res}" if conf_1_res != "None" else False
                conf_2_code = line[keys.index("CONFNO2")]
                conf_2_res = lookup["conference_2"].get(conf_2_code)
                conf_2 = (
                    f"Basketball - {conf_1_res}" if conf_2_res != "None" else False
                )
                conf_3_code = line[keys.index("CONFNO3")]
                conf_3_res = lookup["conference_3"].get(conf_3_code)
                conf_3 = f"Baseball - {conf_1_res}" if conf_3_res != "None" else False
                conf_4_code = line[-1]
                conf_4_res = lookup["conference_4"].get(conf_4_code)
                conf_4 = (
                    f"Cross country/Track - {conf_1_res}"
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
                    "is_member_of_naa": is_member_of_naa,
                    "athletic_organizations": athletic_organizations,
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
    def get(val_list, key_name):
        return val_list[keys.index(key_name)]

    with open(fname, "r") as csvfile:
        contents = csv.reader(csvfile)
        keys = []

        for line_index, line in enumerate(contents):
            if line_index == 0:
                keys = line
            else:
                ipeds_unitid = line[0]

                # students
                total_men = get(line, "EFYTOTLM")
                total_women = get(line, "EFYTOTLW")

                # students - breakdown by race
                hispanic_or_latino = get(line, "EFYHISPT")
                american_indian_or_alaska_native = get(line, "EFYAIANT")
                asian = get(line, "EFYASIAT")
                native_hawaiian_or_other_pacific_islander = get(
                    line, "EFYNHPIT")
                black_or_african_american = get(line, "EFYBKAAT")
                white = get(line, "EFYWHITT")
                two_or_more = get(line, "EFY2MORT")

                # students - breakdown by race and sex
                hispanic_or_latino_men = get(line, "EFYHISPM")
                hispanic_or_latino_women = get(line, "EFYHISPW")
                american_indian_or_alaska_native_men = get(line, "EFYAIANM")
                american_indian_or_alaska_native_women = get(line, "EFYAIANW")
                asian_men = get(line, "EFYASIAM")
                asian_women = get(line, "EFYASIAW")
                native_hawaiian_or_other_pacific_islander_men = get(
                    line, "EFYNHPIM")
                native_hawaiian_or_other_pacific_islander_women = get(
                    line, "EFYNHPIW")
                black_or_african_american_men = get(line, "EFYBKAAM")
                black_or_african_american_women = get(line, "EFYBKAAW")
                white_men = get(line, "EFYWHITM")
                white_women = get(line, "EFYWHITW")
                two_or_more_men = get(line, "EFY2MORM")
                two_or_more_women = get(line, "EFY2MORW")

                dicts[ipeds_unitid]["general"]["students"]["total_men"] = total_men
                dicts[ipeds_unitid]["general"]["students"]["total_women"] = total_women
                dicts[ipeds_unitid]["general"]["students"]["breakdown_by_race"] = {
                    "hispanic_or_latino": hispanic_or_latino,
                    "american_indian_or_alaska_native": american_indian_or_alaska_native,
                    "asian": asian,
                    "native_hawaiian_or_other_pacific_islander": native_hawaiian_or_other_pacific_islander,
                    "black_or_african_american": black_or_african_american,
                    "white": white,
                    "two_or_more": two_or_more,
                }
                dicts[ipeds_unitid]["general"]["students"][
                    "breakdown_by_race_and_sex"
                ] = {
                    "hispanic_or_latino_men": hispanic_or_latino_men,
                    "hispanic_or_latino_women": hispanic_or_latino_women,
                    "american_indian_or_alaska_native_men": american_indian_or_alaska_native_men,
                    "american_indian_or_alaska_native_women": american_indian_or_alaska_native_women,
                    "asian_men": asian_men,
                    "asian_women": asian_women,
                    "black_or_african_american_men": black_or_african_american_men,
                    "black_or_african_american_women": black_or_african_american_women,
                    "native_hawaiian_or_other_pacific_islander_men": native_hawaiian_or_other_pacific_islander_men,
                    "native_hawaiian_or_other_pacific_islander_women": native_hawaiian_or_other_pacific_islander_women,
                    "white_men": white_men,
                    "white_women": white_women,
                    "two_or_more_men": two_or_more_men,
                    "two_or_more_women": two_or_more_women,
                }

    return dicts


def extract_adm2019(dicts: dict, fname: str) -> dict:
    lookup_fname = '../resources/adm2019_lookup.json'
    f = open(lookup_fname, 'r')
    lookup = json.load(f)

    def get(val_list, keyword: str):
        return val_list[keys.index(keyword)]

    with open(fname, 'r') as csvfile:
        contents = csv.reader(csvfile)
        keys = []

        for line_index, line in enumerate(contents):
            if line_index == 0:
                keys = line
            else:
                ipeds_unitid = line[0]

                # general - admissions
                gpa = lookup.get(get(line, 'ADMCON1'))
                school_rank = lookup.get(get(line, 'ADMCON2'))
                school_record = lookup.get(get(line, 'ADMCON3'))
                college_preparatory_programs = lookup.get(get(line, 'ADMCON4'))
                recommendation_letters = lookup.get(get(line, 'ADMCON5'))
                formal_demonstration = lookup.get(get(line, 'ADMCON6'))
                admission_test_scores = lookup.get(get(line, 'ADMCON7'))
                toefl = lookup.get(get(line, 'ADMCON8'))
                other_tests = lookup.get(get(line, 'ADMCON9'))

                sat_eng_25th_percentile = get(line, 'SATVR25')
                sat_eng_75th_percentile = get(line, 'SATVR75')
                sat_math_25th_percentile = get(line, 'SATMT25')
                sat_math_75th_percentile = get(line, 'SATMT75')

                act_comp_25th_percentile = get(line, 'ACTCM25')
                act_comp_75th_percentile = get(line, 'ACTCM75')
                act_eng_25th_percentile = get(line, 'ACTEN25')
                act_eng_75th_percentile = get(line, 'ACTEN75')
                act_math_25th_percentile = get(line, 'ACTMT25')
                act_math_75th_percentile = line[-1]

                applicants_men = get(line, 'APPLCNM')
                applicants_women = get(line, 'APPLCNW')
                admissions_men = get(line, 'ADMSSNM')
                admissions_women = get(line, 'ADMSSNW')
                applicants_total = get(line, 'APPLCN')
                admissions_total = get(line, 'ADMSSN')
                num_submitting_sat = get(line, 'SATNUM')
                percent_submitting_sat = get(line, 'SATPCT')
                num_submitting_act = get(line, 'ACTNUM')
                percent_submitting_act = get(line, 'ACTPCT')

                dicts[ipeds_unitid]['general']['admissions']['requirements'] = {
                    'gpa': gpa,
                    'school_rank': school_rank,
                    'school_record': school_record,
                    'college_preparatory_programs': college_preparatory_programs,
                    'recommendation_letters': recommendation_letters,
                    'formal_demonstration': formal_demonstration,
                    'admission_test_scores': admission_test_scores,
                    'toefl': toefl,
                    'other_tests': other_tests,
                }
                dicts[ipeds_unitid]['general']['admissions']['sat'] = {
                    'eng_25th_percentile': sat_eng_25th_percentile,
                    'eng_75th_percentile': sat_eng_75th_percentile,
                    'math_25th_percentile': sat_math_25th_percentile,
                    'math_75th_percentile': sat_math_75th_percentile,
                }
                dicts[ipeds_unitid]['general']['admissions']['act'] = {
                    'comp_25th_percentile': act_comp_25th_percentile,
                    'comp_75th_percentile': act_comp_75th_percentile,
                    'eng_25th_percentile': act_eng_25th_percentile,
                    'eng_75th_percentile': act_eng_75th_percentile,
                    'math_25th_percentile': act_math_25th_percentile,
                    'math_75th_percentile': act_math_75th_percentile,
                }
                dicts[ipeds_unitid]['general']['admissions']['population'] = {
                    'applicants_men': applicants_men,
                    'applicants_women': applicants_women,
                    'admissions_men': admissions_men,
                    'admissions_women': admissions_women,
                    'applicants_total': applicants_total,
                    'admissions_total': admissions_total,
                    'num_submitting_sat': num_submitting_sat,
                    'percent_submitting_sat': percent_submitting_sat,
                    'num_submitting_act': num_submitting_act,
                    'percent_submitting_act': percent_submitting_act,
                }

    return dicts


def extract_ic2019_ay(dicts: dict) -> dict:
    fname = '../resources/ic2019_ay.csv'

    def get(val_list, key):
        return val_list[keys.index(key)]

    with open(fname, 'r') as csvfile:
        contents = csv.reader(csvfile)

        keys = []
        for line_index, line in enumerate(contents):
            if line_index == 0:
                keys = line
            else:
                ipeds_unitid = line[0]

                # general - tuition
                in_tuition_and_fees_17 = get(line, 'CHG2AY1')  # 2017-18
                in_tuition_and_fees_18 = get(line, 'CHG2AY2')  # 2018-19
                in_tuition_and_fees_19 = get(line, 'CHG2AY3')  # 2019-20
                in_tuition_17 = get(line, 'CHG2AT1')  # 2017-18
                in_tuition_18 = get(line, 'CHG2AT2')  # 2018-19
                in_tuition_19 = get(line, 'CHG2AT3')  # 2019-20
                in_fees_17 = get(line, 'CHG2AF1')  # 2017-18
                in_fees_18 = get(line, 'CHG2AF2')  # 2018-19
                in_fees_19 = get(line, 'CHG2AF3')  # 2018-20

                out_tuition_and_fees_17 = get(line, 'CHG3AY1')  # 2017-18
                out_tuition_and_fees_18 = get(line, 'CHG3AY2')  # 2018-19
                out_tuition_and_fees_19 = get(line, 'CHG3AY3')  # 2019-20
                out_tuition_17 = get(line, 'CHG3AT1')  # 2017-18
                out_tuition_18 = get(line, 'CHG3AT2')  # 2018-19
                out_tuition_19 = get(line, 'CHG3AT3')  # 2019-20
                out_fees_17 = get(line, 'CHG3AF1')  # 2017-18
                out_fees_18 = get(line, 'CHG3AF2')  # 2018-19
                out_fees_19 = get(line, 'CHG3AF3')  # 2018-20

                books_and_supplies_17 = get(line, 'CHG4AY1')
                books_and_supplies_18 = get(line, 'CHG4AY2')
                books_and_supplies_19 = get(line, 'CHG4AY3')

                other_expenses_17 = get(line, 'CHG6AY1')
                other_expenses_18 = get(line, 'CHG6AY2')
                other_expenses_19 = get(line, 'CHG6AY3')
                on_room_board_17 = get(line, 'CHG5AY1')
                on_room_board_18 = get(line, 'CHG5AY2')
                on_room_board_19 = get(line, 'CHG5AY3')

                off_room_board_17 = get(line, 'CHG7AY1')
                off_room_board_18 = get(line, 'CHG7AY2')
                off_room_board_19 = get(line, 'CHG7AY3')
                off_other_expenses_17 = get(line, 'CHG8AY1')
                off_other_expenses_18 = get(line, 'CHG8AY2')
                off_other_expenses_19 = get(line, 'CHG8AY3')

                dicts[ipeds_unitid]['general']['tuition'] = \
                    {
                        "in_state": {
                            "2017": {
                                "tuition_and_fees": in_tuition_and_fees_17,
                                "tuition": in_tuition_17,
                                "fees": in_fees_17,
                            },
                            "2018": {
                                "tuition_and_fees": in_tuition_and_fees_18,
                                "tuition": in_tuition_18,
                                "fees": in_fees_18,
                            },
                            "2019": {
                                "tuition_and_fees": in_tuition_and_fees_19,
                                "tuition": in_tuition_19,
                                "fees": in_fees_19,
                            },
                        },
                        "out_of_state": {
                            "2017": {
                                "tuition_and_fees": out_tuition_and_fees_17,
                                "tuition": out_tuition_17,
                                "fees": out_fees_17,
                            },
                            "2018": {
                                "tuition_and_fees": out_tuition_and_fees_18,
                                "tuition": out_tuition_18,
                                "fees": out_fees_18,
                            },
                            "2019": {
                                "tuition_and_fees": out_tuition_and_fees_19,
                                "tuition": out_tuition_19,
                                "fees": out_fees_19,
                            },
                        },
                        "books_and_supplies": {
                            "2017": books_and_supplies_17,
                            "2018": books_and_supplies_18,
                            "2019": books_and_supplies_19,
                        },
                        "on_campus": {
                            "2017": {
                                "other_expenses": other_expenses_17,
                                "room_and_board_on_campus": on_room_board_17,
                            },
                            "2018": {
                                "other_expenses": other_expenses_18,
                                "room_and_board_on_campus": on_room_board_18,
                            },
                            "2019": {
                                "other_expenses": other_expenses_19,
                                "room_and_board_on_campus": on_room_board_19,
                            },
                        },
                        'off_campus': {
                            '2017': {
                                "room_and_board_off_campus": off_room_board_17,
                                "other_expenses_off_campus": off_other_expenses_17,
                            },
                            '2018': {
                                "room_and_board_off_campus": off_room_board_18,
                                "other_expenses_off_campus": off_other_expenses_18,
                            },
                            '2019': {
                                "room_and_board_off_campus": off_room_board_19,
                                "other_expenses_off_campus": off_other_expenses_19,
                            },
                        },
                    }
    return dicts


def extract_ef2019d(dicts: dict) -> dict:
    fname = '../resources/ef2019d.csv'

    def get(val_list, key):
        return val_list[keys.index(key)]

    with open(fname, 'r') as csvfile:
        contents = csv.reader(csvfile)

        keys = []
        for line_index, line in enumerate(contents):
            if line_index == 0:
                keys = line
            else:
                ipeds_unitid = line[0]

                # general - students
                student_faculty_ratio = line[-1]
                fulltime_retention_rate_raw = get(line, 'RET_PCF')
                fulltime_retention_rate = fulltime_retention_rate_raw if fulltime_retention_rate_raw != "" else '.'

                dicts[ipeds_unitid]['general']['students']['student_faculty_ratio'] = student_faculty_ratio
                dicts[ipeds_unitid]['general']['students']['fulltime_retention_rate'] = fulltime_retention_rate

    return dicts


def extract_s2019_sis(dicts: dict) -> dict:
    fname = '../resources/s2019_sis.csv'

    def get(val_list, key):
        return val_list[keys.index(key)]

    with open(fname, 'r') as csvfile:
        contents = csv.reader(csvfile)
        keys = []
        for line_index, line in enumerate(contents):
            if line_index == 0:
                keys = line
            else:
                ipeds_unitid = line[0]

                # general - faculty
                fulltime_instructional_staff = get(line, 'SISTOTL')
                professors = get(line, 'SISPROF')
                associate_professors = get(line, 'SISASCP')
                assistant_professors = get(line, 'SISASTP')
                other = str(int(get(line, 'SISINST')) + int(get(line, 'SISLECT')) + int(line[-1]))

                dicts[ipeds_unitid]['general']['faculty'] = {
                    'fulltime_instructional_staff': fulltime_instructional_staff,
                    'breakdown_by_rank': {
                        'professors': professors,
                        'associate_professors': associate_professors,
                        'assistant_professors': assistant_professors,
                        'other': other
                    },
                }
    return dicts


def extract_al2019(dicts: dict) -> dict:
    fname = '../resources/al2019.csv'

    def get(val_list, key):
        return val_list[keys.index(key)]

    with open(fname, 'r') as csvfile:
        contents = csv.reader(csvfile)
        keys = []
        for line_index, line in enumerate(contents):
            if line_index == 0:
                keys = line
            else:
                ipeds_unitid = line[0]

                # general - library
                physical_books = get(line, 'LPBOOKS')
                digital_books = get(line, 'LEBOOKS')
                digital_databases = get(line, 'LEDATAB')
                physical_media = get(line, 'LPMEDIA')
                digital_media = get(line, 'LEMEDIA')

                dicts[ipeds_unitid]['general']['library'] = {
                    "physical_books": physical_books,
                    "digital_books": digital_books,
                    "digital_databases": digital_databases,
                    "physical_media": physical_media,
                    "digital_media": digital_media,
                }
    return dicts


def extract() -> None:
    dicts = dict()

    hd2019_output = extract_hd2019(dicts, "../resources/hd2019.csv")
    ic2019_output = extract_ic2019(
        hd2019_output, "../resources/ic2019.csv", "../resources/ic2019_lookup.json"
    )
    effy2019_output = extract_effy2019(
        ic2019_output, "../resources/effy2019.csv")
    adm2019_output = extract_adm2019(
        effy2019_output, '../resources/adm2019.csv')
    ic2019_ay_output = extract_ic2019_ay(adm2019_output)
    ef2019d_output = extract_ef2019d(ic2019_ay_output)
    s2019_sis_output = extract_s2019_sis(ef2019d_output)
    al2019_output = extract_al2019(s2019_sis_output)

    final_output = al2019_output

    # only output one file
    with open("../script_outputs/layer_1_output.json", "w+") as outfile:
        outfile.write(json.dumps(final_output))


def main() -> None:
    extract()


if __name__ == "__main__":
    main()
