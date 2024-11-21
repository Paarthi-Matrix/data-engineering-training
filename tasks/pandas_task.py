import pandas as pd

from constant.constants import ADDRESS_FILE, MAIN_FILE, STATE_NAME


def check_valid_mobile_number(mobile_no):
    """
    Checks for valid mobile number. Length must be equal to 10 and all must be a digit"""
    if pd.isna(mobile_no):
        return pd.NA
    mobile_no = str(mobile_no).strip()
    if mobile_no.isdigit() and len(mobile_no) == 10:
        return mobile_no
    return pd.NA


def merge_files():
    """Merges the two given files and transforms it"""
    main_data = pd.read_excel(MAIN_FILE)
    address = pd.read_excel(ADDRESS_FILE)
    address.rename(columns={"pad_id": "pat_id"}, inplace=True)
    merged_data = main_data.merge(address, on="pat_id",
                                  how="left")  # performing left join according to the requirements
    merged_data[["first_name", "last_name"]] = merged_data["name"].str.split(" ", expand=True)
    merged_data.drop(columns=["name"], inplace=True)
    merged_data["mobile_no"] = merged_data["mobile_no"].apply(check_valid_mobile_number)
    merged_data["is_tn"] = merged_data["state"].str.strip().str.casefold() == STATE_NAME

    dataframes = [merged_data, main_data, address]

    for idx, df in enumerate(dataframes, 1):
        print(f"DataFrame {idx}:")

        row_count = df.shape[0]
        print(f"Row count: {row_count}")

        null_count = df.isna().sum()
        print("Null count per column:")
        print(null_count)
        print("-" * 50)

    print(merged_data)


merge_files()
