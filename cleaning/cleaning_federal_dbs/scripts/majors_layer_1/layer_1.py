import os
import csv as _csv
import json
from alive_progress import alive_bar


def writefile(data: dict, out_fname: str) -> None:
    with open(out_fname, 'w+') as outfile:
        outfile.write(json.dumps(data))


def cleanup(input_fname: str, output_fname) -> None:
    csvdata = []
    total = 260533
    with alive_bar(total, title='Reading and Replacing...') as bar:
        with open(input_fname, newline='') as csvfile:
            raw_data = _csv.reader(csvfile)
            for row in raw_data:
                new_row = [w.replace("PrivacySuppressed", '.') for w in row]
                csvdata.append(new_row)
                bar()
    total = 260532
    with alive_bar(total, title='Writing...') as bar:
        with open(output_fname, 'w+') as csvfile:
            fieldnames = [
                'UNITID', 'OPEID6', 'INSTNM', 'CIPCODE', 'CIPDESC', 'CREDLEV', 'CREDDESC', 'IPEDSCOUNT1', 'IPEDSCOUNT2', 'EARN_MDN_HI_1YR', 'EARN_MDN_HI_2YR'
            ]
            keys = []
            writer = _csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row_num, row in enumerate(csvdata):
                if row_num != 0:
                    unitid = row[0]
                    opeid6 = row[1]
                    instnm = row[2]
                    cipcode = row[keys.index('CIPCODE')]
                    cipdesc = row[keys.index('CIPDESC')]
                    credlev = row[keys.index('CREDLEV')]
                    creddesc = row[keys.index('CREDDESC')]
                    ipedscount1 = row[keys.index('IPEDSCOUNT1')]
                    ipedscount2 = row[keys.index('IPEDSCOUNT2')]
                    med1yr = row[keys.index('EARN_MDN_HI_1YR')]
                    med2yr = row[keys.index('EARN_MDN_HI_2YR')]
                    clean_row = {
                        'UNITID': unitid, 'OPEID6': opeid6, 'INSTNM': instnm, "CIPCODE": cipcode, 'CIPDESC': cipdesc, 'CREDLEV': credlev, 'CREDDESC': creddesc, 'IPEDSCOUNT1': ipedscount1, 'IPEDSCOUNT2': ipedscount2, 'EARN_MDN_HI_1YR': med1yr, 'EARN_MDN_HI_2YR': med2yr
                    }
                    writer.writerow(clean_row)
                else:
                    print(row)
                    keys = row
                    continue
                bar()


def traverse(input_fname: str, output_fname: str) -> None:
    total = 260532
    with alive_bar(total, title='Extracting...') as bar:
        with open(input_fname, newline='') as csvfile:
            csvdata = _csv.reader(csvfile)
            keys = []
            res_dict = {}
            prev_unitid = ''
            for row_number, row in enumerate(csvdata):
                if row_number == 0:
                    keys = row
                else:
                    cur_unitid = row[0]

                    # extract values from list
                    cipcode = row[keys.index('CIPCODE')]
                    cipdesc = row[keys.index('CIPDESC')]
                    credlev = row[keys.index('CREDLEV')]
                    creddesc = row[keys.index('CREDDESC')]
                    ipedscount1 = row[keys.index('IPEDSCOUNT1')]
                    ipedscount2 = row[keys.index('IPEDSCOUNT2')]
                    med1yr = row[keys.index('EARN_MDN_HI_1YR')]
                    med2yr = row[-1]

                    # create dict to enter into res_dict
                    major = {
                        'cipcode': cipcode,
                        'cipdesc': cipdesc,
                        'credlev': credlev,
                        'creddesc': creddesc,
                        'ipedscount1': ipedscount1,
                        'ipedscount2': ipedscount2,
                        'med1yr': med1yr,
                        'med2yr': med2yr,
                    }

                    if cur_unitid == 'NULL':
                        pass
                    elif prev_unitid == cur_unitid:
                        # add major to entry & add to the school's majors overview information
                        res_dict[cur_unitid]['majors'].append(major)

                    else:
                        # create a new entry
                        prev_unitid = cur_unitid

                        # values to fill in school_dict
                        opeid6 = row[1]
                        name = row[2]

                        school_dict = {
                            'unitid': cur_unitid,
                            'opeid6': opeid6,
                            'name': name,
                            'majors': [major]
                        }
                        res_dict[cur_unitid] = school_dict
                    bar()

    total = len(res_dict.keys())
    with alive_bar(total, title='Writing Files...') as bar:
        for item in res_dict.keys():
            print(item)
            data = res_dict[item]
            new_fname = f"../../script_outputs/majors_layer_1/schools/{item}.json"
            writefile(data, new_fname)
            bar()


def main():
    # replace null values in existing file to lessen its data footprint(?)
    input_fname = '../../external_outputs/Most-Recent-Cohorts-Field-of-Study.csv'
    output_fname = '../../external_outputs/majors_raw.replaced.csv'
    # cleanup(input_fname, output_fname)

    # parse file and extract data
    input_fname = '../../external_outputs/majors_raw.replaced.csv'
    output_fname = '../../script_outputs/majors_layer_1/majors_output.json'
    traverse(input_fname, output_fname)


if __name__ == '__main__':
    main()
