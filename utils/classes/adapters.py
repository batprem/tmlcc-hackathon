import os
import pandas as pd
from typing import List
from scipy.spatial import ConvexHull


class CIF2PandasAdapter:
    """
    An adapter to convert CIF into Pandas DataFrames
    """
    @staticmethod
    def load_cif(cif_filepath: str) -> List[str]:
        """
        Read CIF file as String and split looping sections
        """
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
        """
        Get metadata of a CIF file
        """
        return pd.DataFrame(dataframes[0])

    @staticmethod
    def get_loops(dataframes: List[List[str]]) -> List[pd.DataFrame]:
        """
        Get loops
        """
        loops = []
        for dataframe in dataframes[1:]:
            loop = pd.DataFrame(dataframe)
            loop_fixed = loop[loop[1].notna()]
            loop_fixed.columns = loop[loop[1].isna()][0]
            loops.append(loop_fixed.to_dict())

        return loops
    
    def apply(self, cif_filepath: str) -> List[pd.DataFrame]:
            """
            Apply ETL pipeline
            """
            # Extract
            cif_list = self.load_cif(cif_filepath)

            # Transform
            metadata = self.get_metadata(cif_list)
            extract_loops = self.get_loops(cif_list)
            xyz = pd.DataFrame(extract_loops[0])[['_atom_site_fract_x', '_atom_site_fract_y', '_atom_site_fract_z']]
            convex_hull = ConvexHull(xyz)

            metadata.at[11, 0] = 'mof_convex_hull_area'
            metadata.at[11, 1] = convex_hull.area

            metadata.at[12, 0] = 'mof_convex_hull_volume'
            metadata.at[12, 1] = convex_hull.volume

            metadata.at[13, 0] = 'mof_convex_hull_npoints'
            metadata.at[13, 1] = convex_hull.npoints
  
            metadata.at[14, 0] = 'mof_convex_hull_nsimplex'
            metadata.at[14, 1] = convex_hull.nsimplex
            
            # Load
            return {
                "metadata": metadata.to_dict(),
                "loops": extract_loops
            }