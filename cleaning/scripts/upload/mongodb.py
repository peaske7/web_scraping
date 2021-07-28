import pymongo
import json
import os
from alive_progress import alive_bar
from urllib.parse import quote

mongo_uri = "mongodb+srv://root:" + \
    quote("DC3R-.@Ut@V4WbP") + \
    "@cluster0.8delt.mongodb.net/college-search?retryWrites=true&w=majority"
myclient = pymongo.MongoClient(mongo_uri)
mydb = myclient["college-search"]
schools_col = mydb["schools"]
majors_col = mydb['majors']


def upload_helper(dirname: str, num: int, col) -> None:
    col.delete_many({})
    tracker = 0
    with alive_bar(num) as bar:
        for fname in os.listdir(dirname):
            path = f"{dirname}/{ fname }"
            f = open(path)
            item = json.load(f)

            col.insert_one(item)

            bar()
            tracker += 1
            if tracker == num:
                break


def upload(num: int) -> None:
    schools_dirname = '../../outputs/layer_6'
    majors_dirname = '../../cleaning_federal_dbs/script_outputs/majors_layer_1/schools'

    # upload num schools documents to mongo server
    upload_helper(schools_dirname, num, schools_col)
    upload_helper(majors_dirname, num, majors_col)


def main():
    upload(200)


if __name__ == '__main__':
    main()
