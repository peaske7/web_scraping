import json


def sort(i_fname: str, o_fname: str) -> None:
    f = open(i_fname)
    schools = json.load(f)

    us_schools = {}
    for school in schools:
        country = schools[school]["general"]["country"]
        ff_name = schools[school]["general"]["ff_name"]
        if country == "USA":
            us_schools[ff_name] = schools[ff_name]

    with open(o_fname, "w+") as outfile:
        outfile.write(json.dumps(us_schools))


def main():
    input_fname = "../../outputs/layer_1/layer_1_output.json"
    output_fname = "../../outputs/layer_1/layer_1_us_schools.json"
    sort(input_fname, output_fname)


if __name__ == "__main__":
    main()
