import pandas as pd


def get_cif_filepath(
    mof_df: pd.DataFrame,
    cif_path: str="."
) -> dict:
    """
    Match MOF id with MOF `.cif` file
    """
    mof_df["cif_filepath"] = cif_path + "/" + mof_df["MOFname"] + '.cif'
    return mof_df