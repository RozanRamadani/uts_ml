import numpy as np
from imblearn.over_sampling import SMOTENC
from imblearn.under_sampling import RandomUnderSampler


# 1. Oversample training data with SMOTENC
def resample_with_smotenc(X_train, y_train, random_state=42):
    categorical_columns = X_train.select_dtypes(
        exclude=[np.number]
    ).columns.tolist()
    categorical_indices = [
        X_train.columns.get_loc(column) for column in categorical_columns
    ]

    sampler = SMOTENC(
        categorical_features=categorical_indices,
        random_state=random_state,
    )
    return sampler.fit_resample(X_train, y_train)


# 2. Undersample training data with RandomUnderSampler
def resample_with_random_under_sampler(X_train, y_train, random_state=42):
    sampler = RandomUnderSampler(random_state=random_state)
    return sampler.fit_resample(X_train, y_train)
