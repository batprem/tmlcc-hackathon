import pandas as pd
from src.constants import (
    PREPROCESSING_PATH,
    TARGET
)

import numpy as np
import re
from typing import List
from collections import Counter
import itertools
import seaborn as sns


class FunctionalGroupToGramExtractor():
    specific_columns: list = []

    @staticmethod
    def molecule_to_element_list(molecule: str) -> List[str]:
        try:
            return re.findall(
                r'[A-Z][a-z]?\d*|\((?:[^()]*(?:\(.*\))?[^()]*)+\)\d+',
                molecule
            )
        except TypeError:
            return []

    @staticmethod
    def molecule_to_element_list(molecule: str) -> List[str]:
        try:
            return re.findall(
                r'[A-Z][a-z]?\d*|\((?:[^()]*(?:\(.*\))?[^()]*)+\)\d+',
                molecule
            )
        except TypeError:
            return []

    @staticmethod
    def bigram(molecule):
        a, b = itertools.tee(molecule)
        next(b, None)
        return ["-".join(gram) for gram in (zip(a, b))] 

    @staticmethod
    def trigram(molecule):
        a, b, c = itertools.tee(molecule, 3)
        next(b, None)
        next(c, None)
        next(c, None)
        return ["-".join(gram) for gram in (zip(a, b, c))]


    def transform(self, df, fit=False, filter_ratio=0.01):
        df['functional_group_list'] = df.functional_groups.apply(
            self.molecule_to_element_list
        )
        df['functional_group_bigram_list'] = df.functional_group_list.apply(
            lambda x: self.bigram(x)
        )

        df['functional_group_unigram'] = df.functional_group_list.apply(
            lambda x: dict(Counter(x))
        )

        df['functional_group_bigram'] = df.functional_group_bigram_list.apply(
            lambda x: dict(Counter(x))
        )

        unigram_df = pd.DataFrame(
            list(df['functional_group_unigram'].values)
        ).fillna(0)
        unigram_df.index = df.index
        unigram_df.columns = 'functional_group_unigram_' + unigram_df.columns

        bigram_df = pd.DataFrame(list(df['functional_group_bigram'].values)).fillna(0)
        bigram_df.index = df.index
        bigram_df.columns = 'functional_group_bigram_' + bigram_df.columns

        congram_df = pd.concat([unigram_df, bigram_df], axis=1)
        if fit:
            self.specific_columns = []
            for col in congram_df.columns:
                if np.mean(congram_df[col] > 0) > filter_ratio:
                    self.specific_columns.append(col)
        else:
            for col in self.specific_columns:
                congram_df[col] = congram_df.get(col, 0)
        return congram_df[self.specific_columns]
