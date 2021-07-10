import json
import os


def merge_all(output_path: str) -> None:
    target_dirname = '../../external_outputs/institution'
    dicts = dict()
    for fname in os.listdir(target_dirname):
        path = f"{target_dirname}/{fname}"
        f = open(path)
        data = json.load(f)

        for item in data:
            unitid = item['unitid']
            opeid = item['opeid']
            opeid6 = item['opeid6']
            name_en = item['name_en']
            local_url = item['institutionData']['url']
            address_short = item['institutionData']['campus_address_short']
            students = item['institutionData']['students']

            dicts[unitid] = {
                'unitid': unitid,
                'opeid': opeid,
                'opeid6': opeid6,
                'name_en': name_en,
                'local_url': local_url,
                'address_short': address_short,
                'students': students
            }

    with open(output_path, 'w+') as outfile:
        outfile.write(json.dumps(dicts))


def main():
    merged_output_path = '../../resources/institution_data_output.json'
    merge_all(merged_output_path)


if __name__ == '__main__':
    main()
