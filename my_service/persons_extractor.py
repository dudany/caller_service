from my_service.caller_utils import DEFAULT_VR, NameNotFoundError, BadSourceException
from my_service.data_helper import DatabaseAccess


def sorting_function(df, value_rates=None):
    # sorts the name to be returned by their importance weighted by source and num_of_records
    if value_rates is None:
        value_rates = DEFAULT_VR

    df["calibration"] = df.apply(lambda x: value_rates.get(x.source) + x.num_of_records, axis=1)
    sorted_df = df.sort_values(by="calibration")
    return sorted_df


def is_bad_source(row):
    return row["source"].iloc[0] == DatabaseAccess.BAD_SOURCE


def get_persons_name(phone_number: str, data_base_obj:DatabaseAccess):
    # the data consumption is by reading the .csv with pandas, decided to postpone db creation would use SQL
    df = data_base_obj.get_data()
    filtered_df = df[df["phone_number"] == phone_number]
    if len(filtered_df) == 0:
        raise NameNotFoundError(phone_number)

    if len(filtered_df) < 2:  # case  there is 1 row for a phone number we return its name
        # if there is one distinct contact for the phone number we return its name
        defined_row = filtered_df
    else:
        sorted_df = sorting_function(filtered_df.copy())
        defined_row = sorted_df.head(1)

    if is_bad_source(defined_row):
        raise BadSourceException(phone_number)
    name = defined_row["name"].iloc[0]
    return name
