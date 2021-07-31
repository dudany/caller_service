import logging
import re
import pandas as pd
from datapackage import Package


def get_countries_dict():
    package = Package('https://datahub.io/core/country-list/datapackage.json')
    countries = {}
    for resource in package.resources:
        if resource.descriptor['datahub']['type'] == 'derived/csv':
            for val, key in resource.read():
                countries[key] = val
    return countries


def clean_name(name):
    # returns name with no capital letters, non-ascii and name prefix such as Mr,Dr,Mrs,
    # and removes dots and removes trailing spaces.
    name = de_emoji(name)
    name = name.lower().replace(".", "").strip()
    name = " ".join([p for p in name.split(' ') if p not in DatabaseAccess.N_PREFIX])
    return name


def de_emoji(text):
    re_pattern = re.compile(pattern="["
                                    r"\U0001F600-\U0001F64F"  # emoticons
                                    r"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                    r"\U0001F680-\U0001F6FF"  # transport & map symbols
                                    r"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                    "]+", flags=re.UNICODE)
    return re_pattern.sub(r'', text)


class DatabaseAccess:
    # this class inits the "data base" , in the tasks standards it returns the df in real service it would return
    # collection object (mongoDB) that we could query accessed by credentials defined in the environment.

    SOURCES = ['address_book', 'community', 'vendor', 'scarping', 'email_signature']
    N_PREFIX = ["ms", "sr", "dr", "prof", "miss", "hon", "mr", "jr", "mrs"]
    BAD_SOURCE = "bad_source"

    def __init__(self):
        df = pd.read_csv("data/caller_id_db.csv")
        self.data_collection = self.clean_data(df)
        logging.info("Data loaded successfully")

    def get_data(self):
        # return the copy of the data so it will not be mutable
        return self.data_collection.copy()

    def clean_data(self, df):
        # remove emoji then remove titles and lower case all then create new supportive column
        df["name"] = df["name"].apply(clean_name)

        # resolve 2 Digit locations into full country name
        countries = get_countries_dict()
        df["location"] = df["location"].apply(lambda x: countries.get(x, x))

        # validate source in sources group
        df["source"] = df["source"].apply(lambda x: x if x in self.SOURCES else self.BAD_SOURCE)

        # remove rows with bad phone number (expected format should be "123-123-1234")
        df = df[df["phone_number"].str.contains(r"[0-9]{3}-[0-9]{3}-[0-9]{4}")]
        df = df.drop(columns=['work_email'])
        return df
