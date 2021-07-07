import json
import os

target_dirname = "./layer_2"


def extract_and_merge(dirname):
    dicts = dict()

    for filename in os.listdir(dirname):
        relative_path = f"{dirname}/{filename}"
        f = open(relative_path)
        data = json.load(f)

        for item in data:
            ff_schoolname = item["name"].lower().replace(" ", "_")

            # from filename
            category = filename.split(".")[0]
            year = filename.split(".")[1]

            # general info
            name = item.get("name")
            country = item.get("country")

            # initialize school dict
            # dicts[ff_schoolname] = dict()

            if ff_schoolname in dicts.keys():
                # if school already exists, check if rankings_by_category contains
                # the major
                if dicts[ff_schoolname]["rankings_by_category"].get(category):
                    dicts[ff_schoolname]["rankings_by_category"][category][year] = {
                        "year": year,
                        "category": category,
                        "category_children": item["ranking_categories"],
                    }
                else:
                    dicts[ff_schoolname]["rankings_by_category"][category] = dict()
                    dicts[ff_schoolname]["rankings_by_category"][category][year] = {
                        "year": year,
                        "category": category,
                        "category_children": item["ranking_categories"],
                    }
                print(ff_schoolname)
            else:
                dicts[ff_schoolname] = dict()
                dicts[ff_schoolname]["name"] = name
                dicts[ff_schoolname]["country"] = country
                dicts[ff_schoolname]["rankings_by_category"] = {
                    category: {
                        year: {
                            "year": year,
                            "category": category,
                            "category_children": item["ranking_categories"],
                        }
                    }
                }
                print(dicts[ff_schoolname])

    with open("layer_4_output.json", "w+") as outfile:
        outfile.write(json.dumps(dicts))


def main():
    extract_and_merge(target_dirname)


main()
