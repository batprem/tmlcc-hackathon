import os
import pandas as pd
from typing import List


class CIF2PandasAdapter:
    @staticmethod
    def load_cif(cif_filepath: str):
        with open(cif_filepath) as f:
            filename = f.readline().strip()
            dataframes = []
            dataframe = []
            for line in f.readlines():
                columns = [
                    l.strip() for l in line.strip().split(" ") if l and (l != '')
                ]
                if columns:
                    if columns[0] == 'loop_':
                        dataframes.append(dataframe)
                        dataframe = []
                    else:
                        if 'fapswitch' not in columns and columns != ['']:
                            dataframe.append(columns)
            dataframes.append(dataframe)

        return dataframes

    @staticmethod
    def get_metadata(dataframes: List[List[str]]) -> pd.DataFrame:
        return pd.DataFrame(dataframes[0])

    @staticmethod
    def get_loops(dataframes: List[List[str]]) -> List[pd.DataFrame]:
        loops = []
        for dataframe in dataframes[1:]:
            loop = pd.DataFrame(dataframes[1])
            loop_fixed = loop[loop[1].notna()]
            loop_fixed.columns = loop[loop[1].isna()][0]
            loops.append(loop_fixed)

        return loops
    
    def apply(self, cif_filepath: str) -> List[pd.DataFrame]:
        # Extract
        cif_list = self.load_cif(cif_filepath)

        # Transform
        metadata = self.get_metadata(cif_list)
        extract_loops = self.get_loops(cif_list)

        # Load
        return {
            "metadata": metadata,
            "loops": extract_loops
        }