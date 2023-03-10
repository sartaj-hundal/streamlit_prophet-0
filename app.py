from typing import Any, Dict, List

import snowflake.connector
import matplotlib.pyplot as plt
import numpy as np
import prophet

import pandas as pd
import streamlit as st
from lib.dataprep.clean import clean_df
from lib.dataprep.format import (
    add_cap_and_floor_cols,
    check_dataset_size,
    filter_and_aggregate_df,
    format_date_and_target,
    format_datetime,
    print_empty_cols,
    print_removed_cols,
    remove_empty_cols,
    resample_df,
)
from lib.dataprep.split import get_train_set, get_train_val_sets
from lib.exposition.export import display_links, display_save_experiment_button
from lib.exposition.visualize import (
    plot_components,
    plot_future,
    plot_overview,
    plot_performance,
)
from lib.inputs.dataprep import input_cleaning, input_dimensions, input_resampling
from lib.inputs.dataset import (
    input_columns,
    input_dataset,
    input_future_regressors,
)
from lib.inputs.dates import (
    input_cv,
    input_forecast_dates,
    input_train_dates,
    input_val_dates,
)
from lib.inputs.eval import input_metrics, input_scope_eval
from lib.inputs.params import (
    input_holidays_params,
    input_other_params,
    input_prior_scale_params,
    input_regressors,
    input_seasonality_params,
)
from lib.models.prophet import forecast_workflow
from lib.utils.load import load_config, load_image

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

cs = conn.cursor()
#try:
#    cs.execute("SELECT current_version()")
#    one_row = cs.fetchone()
#    st.write(one_row[0])
#finally:
#    cs.close()
#cs.close()

#arr = np.random.normal(1, 1, size=100)
#fig, ax = plt.subplots()
#ax.hist(arr, bins=20)

#st.pyplot(fig)

m = prophet.Prophet(daily_seasonality=True)

try:
    cs.execute("SELECT DATE, SALES FROM MODEL_DATA;")
    df = pd.DataFrame(cs.fetchall(), columns = ['DATE', 'SALES'])
    #max_sales = df['SALES'].max()
    #st.write(max_sales)

    #df['ds'] = df['DATE']
    #df['y'] = df['SALES']
    #df.columns = ['ds', 'y']
    df['ds'] = pd.to_datetime(df['DATE'])
    df['y'] = df['SALES']

    # split data 
    train = df[df['ds'] < pd.Timestamp('2016-03-23')]
    test = df[df['ds'] >= pd.Timestamp('2016-03-23')]
 
    st.write(len(train))
    st.write(len(test))

    m.fit(train)
    #future = m.make_future_dataframe(periods=60)
    #forecast = m.predict(future)


    #st.write(forecast.head())

    #fig_m = m.plot(forecast)
    #plt.legend(['Actual', 'Prediction', 'Uncertainty interval'])
    #plt.show()

    #st.pyplot(fig_m)
    
    #df.set_index('DATE')
    #df.asfreq('D')

    #m.fit(df[df['DATA_SPLIT'] == 'TRAIN'])



finally:
    cs.close()
cs.close()