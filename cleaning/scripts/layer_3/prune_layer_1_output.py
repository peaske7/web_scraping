import json


def writefile(data: dict, output_fname: str) -> None:
    with open(output_fname, 'w+') as outfile:
        outfile.write(json.dumps(data))


def is_us(location: str) -> bool:
    match = ['USA', 'Alabama', 'Alaska', 'American Samoa', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Federated States of Micronesia', 'Florida', 'Georgia', 'Guam', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Marshall Islands', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
             'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Northern Mariana Islands', 'Ohio', 'Oklahoma', 'Oregon', 'Palau', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Island', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
    return location in match


def prune(input_fname: str, output_fname: str) -> None:
    f = open(input_fname)
    data = json.load(f)

    res_data = {}

    for item in data:
        item_data = data[item]
        country = item_data['general']['country']

        if is_us(country):
            res_data[item] = item_data
            res_data[item]['general']['country'] = 'USA'

    writefile(res_data, output_fname)


def main():
    input_fname = '../../outputs/layer_1/layer_1_output.json'
    output_fname = '../../outputs/layer_3/pruned.output.json'
    prune(input_fname, output_fname)


if __name__ == '__main__':
    main()
