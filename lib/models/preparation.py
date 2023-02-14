from typing import Any, Dict

import pandas as pd
from prophet import Prophet

def get_prophet_cv_horizon(dates: Dict[Any, Any], resampling: Dict[Any, Any]) -> str:
    """Returns cross-validation horizon at the right format for Prophet cross_validation function.

    Parameters
    ----------
    dates : Dict
        Dictionary containing cross-validation information.
    resampling : Dict
        Dictionary containing dataset frequency information.

    Returns
    -------
    str
        Cross-validation horizon at the right format for Prophet cross_validation function.
    """
    freq = resampling["freq"][-1]
    horizon = dates["folds_horizon"]
    if freq in ["s", "H"]:
        prophet_horizon = f"{convert_into_nb_of_seconds(freq, horizon)} seconds"
    else:
        prophet_horizon = f"{convert_into_nb_of_days(freq, horizon)} days"
    return prophet_horizon