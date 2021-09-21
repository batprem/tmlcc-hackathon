import pandas as pd
import numpy as np
import os
from tqdm import tqdm


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


def aggregate_loop_0(df: pd.DataFrame):
    """
    Calculate loop_0 statistic value
    """
    partial_charge_statistic = []
    for cif in tqdm(df.cif):
        loop_df = pd.DataFrame(cif['loops'][0])
        loop_df[
            '_atom_type_partial_charge'
        ] = loop_df['_atom_type_partial_charge'].astype(float)

        partial_charge_statistic.append({
            "partial_charge_mean":\
                np.mean(loop_df._atom_type_partial_charge),
            "partial_charge_median":\
                np.median(loop_df._atom_type_partial_charge),
            "partial_charge_std":\
                np.std(loop_df._atom_type_partial_charge),
        })
    partial_charge_df = pd.DataFrame(partial_charge_statistic)
    partial_charge_df.index = df.index

    return pd.concat([df, partial_charge_df], axis=1)


def aggregate_loop_1(
    df: pd.DataFrame
) -> pd.DataFrame:
    bond_count = []
    for cif in tqdm(df.cif):
        bond_count.append(
            pd.DataFrame(cif['loops'][1]).\
            _ccdc_geom_bond_type.value_counts().\
            to_dict()
        )
    bond_count_df = pd.DataFrame(bond_count)
    bond_count_df = bond_count_df.fillna(0)
    bond_count_df.index = df.index
    bond_count_df.columns = "bond_type_count" +  bond_count_df.columns
    return pd.concat([df, bond_count_df], axis=1)