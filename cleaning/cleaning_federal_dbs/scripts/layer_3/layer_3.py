import csv
import json


def get_ccsize_label(value: str) -> str:
    labels = {
        '1': 'Two-year, very small',
        '2': 'Two-year, small',
        '3': 'Two-year, medium',
        '4': 'Two-year, large',
        '5': 'Two-year, very large',
        '6': 'Four-year, very small, primarily nonresidential',
        '7': 'Four-year, very small, primarily nonresidential',
        '8': 'Four-year, very small, primarily residential',
        '9': 'Four-year, small, highly residential',
        '10': 'Four-year, small, primarily residential',
        '11': 'Four-year, small, highly residential',
        '12': 'Four-year, medium, primarily nonresidential',
        '13': 'Four-year, medium, primarily residential',
        '14': 'Four-year, medium, highly residential',
        '15': 'Four-year, large, primarily nonresidential',
        '16': 'Four-year, large, primarily residential',
        '17': 'Four-year, large, highly residential',
        '18': 'Exclusively graduate/professional',
        '-2': '.',
        '0': '.'
    }
    return labels.get(value)


def get_flag_label(values: list) -> list:
    lookup = {
        'HBCU': 'HBCU (Historically Black College and University)',
        'PBI': 'Predominantly Black Institution',
        'ANNHI': 'Alaska Native, Native Hawaiian serving Institution',
        'TRIBAL': 'Tribal College and University',
        'AANAPII': 'Asian American, Native American, Pacific Islander serving Institution',
        'HSI': 'Hispanic serving Institution',
        'NANTI': 'Native American, non-tribal Institution',
        'MENONLY': 'Men-only College',
        'WOMENONLY': 'Women-only College'
    }

    result = []
    for value in values:
        result.append(lookup.get(value))

    return result


def extract_csc(resource_fname: str, dicts_fname: str, output_fname: str, output_dirname) -> None:
    # internal helper function
    def g(vals, key):
        return vals[keys.index(key)]

    # create a dict to temporarily store the extracted data from resource
    rdict = dict()
    with open(resource_fname, 'r') as csvfile:
        contents = csv.reader(csvfile)
        keys = []

        for line_index, line in enumerate(contents):
            if line_index == 0:
                keys = line
            else:
                unitid = line[0]

                ccsize_code = g(line, 'CCSIZSET')
                ccsize = get_ccsize_label(ccsize_code)

                # get the unique flags for the institution
                flag_varnames = [
                    'HBCU', 'PBI', 'ANNHI', 'TRIBAL', 'AANAPII', 'HSI', 'NANTI', 'MENONLY', 'WOMENONLY'
                ]
                flag_truthy = []
                for flag in flag_varnames:
                    res = g(line, flag)
                    if res == '1':
                        flag_truthy.append(flag)
                flags = get_flag_label(flag_truthy)

                # get percentages of degrees awarded to different programs
                cip_varnames = ['PCIP01', 'PCIP03', 'PCIP04', 'PCIP05', 'PCIP09', 'PCIP10', 'PCIP11', 'PCIP12',
                                'PCIP13', 'PCIP14', 'PCIP15', 'PCIP16', 'PCIP19', 'PCIP22', 'PCIP23', 'PCIP24',
                                'PCIP25', 'PCIP26',
                                'PCIP27', 'PCIP29', 'PCIP30', 'PCIP31', 'PCIP38', 'PCIP39', 'PCIP40', 'PCIP41',
                                'PCIP42', 'PCIP43', 'PCIP44', 'PCIP45', 'PCIP46', 'PCIP47', 'PCIP48', 'PCIP49',
                                'PCIP50', 'PCIP51', 'PCIP52']
                cip_truthy = dict()
                for cip in cip_varnames:
                    res = g(line, cip)
                    cip_code = cip.replace('PCIP', '')
                    if res != '0':
                        cip_truthy[cip_code] = res

                rdict[unitid] = {
                    'ccsize': ccsize,
                    'institution_flags': flags,
                    'cip_percents': cip_truthy
                }

    # open dicts_fname and merge temporary dict with target dict
    t_f = open(dicts_fname)
    t_data = json.load(t_f)

    for unitid in t_data:
        t_item = t_data[unitid]
        t_data[unitid] = t_item

        t_data[unitid]['general']['unique_flags'] = rdict[unitid]['institution_flags']
        t_data[unitid]['general']['classifications']['carnegie_size_category'] = rdict[unitid]['ccsize']
        print(unitid)

        # if education dict is missing
        has_education = t_data[unitid]['general'].get('education')
        if has_education is not None:
            t_data[unitid]['general']['education']['program_sizes'] = rdict[unitid]['cip_percents']
        else:
            # initialize dicts lacking 'education' key
            print(f"{unitid}: populating with null values because invalid dict")
            t_data[unitid]['general']['campus']['religious_affiliates'] = 'None'
            t_data[unitid]['general']['students']['headcount'] = {
                "total_men": ".",
                "total_women": ".",
                "breakdown_by_race": {
                    "hispanic_or_latino": ".",
                    "american_indian_or_alaska_native": ".",
                    "asian": ".",
                    "native_hawaiian_or_other_pacific_islander": ".",
                    "black_or_african_american": ".",
                    "white": ".",
                    "two_or_more": "."
                },
                "breakdown_by_race_and_sex": {
                    "hispanic_or_latino_men": ".",
                    "hispanic_or_latino_women": ".",
                    "american_indian_or_alaska_native_men": ".",
                    "american_indian_or_alaska_native_women": ".",
                    "asian_men": ".",
                    "asian_women": ".",
                    "black_or_african_american_men": ".",
                    "black_or_african_american_women": ".",
                    "native_hawaiian_or_other_pacific_islander_men": ".",
                    "native_hawaiian_or_other_pacific_islander_women": ".",
                    "white_men": ".",
                    "white_women": ".",
                    "two_or_more_men": ".",
                    "two_or_more_women": "."
                }
            }
            t_data[unitid]['general']['students']['student_faculty_ratio'] = '.'
            t_data[unitid]['general']['students']['fulltime_retention_rate'] = '.'
            t_data[unitid]['general']['admissions'] = {
                "undergrad_application_fee": ".",
                "requirements": {
                    "gpa": ".",
                    "school_rank": ".",
                    "school_record": ".",
                    "college_preparatory_programs": ".",
                    "recommendation_letters": ".",
                    "formal_demonstration": ".",
                    "admission_test_scores": ".",
                    "toefl": ".",
                    "other_tests": "."
                },
                "sat": {
                    "eng_25th_percentile": ".",
                    "eng_75th_percentile": ".",
                    "math_25th_percentile": ".",
                    "math_75th_percentile": "."
                },
                "act": {
                    "comp_25th_percentile": ".",
                    "comp_75th_percentile": ".",
                    "eng_25th_percentile": ".",
                    "eng_75th_percentile": ".",
                    "math_25th_percentile": ".",
                    "math_75th_percentile": "."
                },
                "population": {
                    "applicants_men": ".",
                    "applicants_women": ".",
                    "applicants_total": ".",
                    "admitted_men": ".",
                    "admitted_women": ".",
                    "admitted_total": ".",
                    "enrolled_men": ".",
                    "enrolled_women": ".",
                    "enrolled_total": ".",
                    "num_submitting_sat": ".",
                    "percent_submitting_sat": ".",
                    "num_submitting_act": ".",
                    "percent_submitting_act": "."
                }
            }
            t_data[unitid]['general']['education'] = {
                'calendar_system': '.'
            }
            t_data[unitid]['general']['sports'] = {
                "is_member_of_naa": None,
                "athletic_organizations": []
            }
            t_data[unitid]['general']['housing'] = {
                "provides_oncampus_housing": None,
                "oncampus_dorm_capacity": ".",
                "yearly_room_charge": ".",
                "board_meal_plan": None,
                "meals_per_week_in_board": ".",
                "yearly_board_charge": ".",
                "yearly_room_and_board_charge": "."
            }
            t_data[unitid]['general']['tuition'] = {
                "in_state": {
                    "2017": {
                        "tuition_and_fees": ".",
                        "tuition": ".",
                        "fees": "."
                    },
                    "2018": {
                        "tuition_and_fees": ".",
                        "tuition": ".",
                        "fees": "."
                    },
                    "2019": {
                        "tuition_and_fees": ".",
                        "tuition": ".",
                        "fees": "."
                    }
                },
                "out_of_state": {
                    "2017": {
                        "tuition_and_fees": ".",
                        "tuition": ".",
                        "fees": "."
                    },
                    "2018": {
                        "tuition_and_fees": ".",
                        "tuition": ".",
                        "fees": "."
                    },
                    "2019": {
                        "tuition_and_fees": ".",
                        "tuition": ".",
                        "fees": "."
                    }
                },
                "books_and_supplies": {
                    "2017": ".",
                    "2018": ".",
                    "2019": "."
                },
                "on_campus": {
                    "2017": {
                        "other_expenses": ".",
                        "room_and_board_on_campus": "."
                    },
                    "2018": {
                        "other_expenses": ".",
                        "room_and_board_on_campus": "."
                    },
                    "2019": {
                        "other_expenses": ".",
                        "room_and_board_on_campus": "."
                    }
                },
                "off_campus": {
                    "2017": {
                        "room_and_board_off_campus": ".",
                        "other_expenses_off_campus": "."
                    },
                    "2018": {
                        "room_and_board_off_campus": ".",
                        "other_expenses_off_campus": "."
                    },
                    "2019": {
                        "room_and_board_off_campus": ".",
                        "other_expenses_off_campus": "."
                    }
                }
            }
            t_data[unitid]['general']['library'] = {
                "physical_books": ".",
                "digital_books": ".",
                "digital_databases": ".",
                "physical_media": ".",
                "digital_media": "."
            }
            t_data[unitid]['general']['local_url'] = '.'

        # check whether admission key is missing
        has_admissions_breakdown = t_data[unitid]['general']['admissions'].get('requirements')
        if has_admissions_breakdown is None:
            # when admissions-requirements keys are lacking, populate with null values
            t_data[unitid]['general']['admissions'] = {
                'undergrad_application_fee': t_data[unitid]['general']['admissions']['undergrad_application_fee'],
                'requirements': {
                    "gpa": ".",
                    "school_rank": ".",
                    "school_record": ".",
                    "college_preparatory_programs": ".",
                    "recommendation_letters": ".",
                    "formal_demonstration": ".",
                    "admission_test_scores": ".",
                    "toefl": ".",
                    "other_tests": "."
                },
                "sat": {
                    "eng_25th_percentile": ".",
                    "eng_75th_percentile": ".",
                    "math_25th_percentile": ".",
                    "math_75th_percentile": "."
                },
                "act": {
                    "comp_25th_percentile": ".",
                    "comp_75th_percentile": ".",
                    "eng_25th_percentile": ".",
                    "eng_75th_percentile": ".",
                    "math_25th_percentile": ".",
                    "math_75th_percentile": "."
                },
                "population": {
                    "applicants_men": ".",
                    "applicants_women": ".",
                    "applicants_total": ".",
                    "admitted_men": ".",
                    "admitted_women": ".",
                    "admitted_total": ".",
                    "enrolled_men": ".",
                    "enrolled_women": ".",
                    "enrolled_total": ".",
                    "num_submitting_sat": ".",
                    "percent_submitting_sat": ".",
                    "num_submitting_act": ".",
                    "percent_submitting_act": "."
                }
            }

    # write files per each item in final merged dict
    with open(output_fname, 'w+') as outfile:
        outfile.write(json.dumps(t_data))

    # create separate file for each school
    for unitid in t_data:
        new_fname = f"{output_dirname}/{unitid}.json"

        with open(new_fname, 'w+') as outfile:
            outfile.write(json.dumps(t_data[unitid]))


def main():
    rname = '../../external_outputs/raw_csc_all_schools.csv'
    dname = '../../script_outputs/layer_2_output.json'
    oname = '../../script_outputs/layer_3_output.json'
    odirname = '../../script_outputs/layer_3'
    extract_csc(rname, dname, oname, odirname)


if __name__ == '__main__':
    main()
