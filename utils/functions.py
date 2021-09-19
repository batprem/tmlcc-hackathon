import pandas as pd
import os


def get_cif_filepath(
    mof_df: pd.DataFrame,
    cif_path: str="."
) -> dict:
    """
    Match MOF id with MOF `.cif` file
    """
    mof_df["cif_filepath"] = cif_path + "/" + mof_df["MOFname"] + '.cif'
    return mof_df


def merge_metadata(df: pd.DataFrame):
    """
    Merge MOF with CIF metadata
    """
    metadata_list = []
    for cif in df.cif:
        metadata_list.append(cif['metadata'][1].values())
    metadata_df = pd.DataFrame(metadata_list)
    metadata_df.index = df.index
    metadata_df.columns = cif['metadata'][0].values()
    return pd.concat([df, metadata_df], axis=1)


def read_pandas_pickle(path: str):
    dataframe_list = []
    for pickle_file in os.listdir(path):
        print(pickle_file)
        filepath = f"{path}/{pickle_file}".replace("//", "/")
        dataframe_list.append(pd.read_pickle(filepath))

    return pd.concat(dataframe_list).sort_index()