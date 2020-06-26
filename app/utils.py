import requests
import pandas as pd
import numpy as np
import datetime
import plotly.express as px

base_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"


def rename_columns(input_data):
    output_data = input_data.rename(columns={'Country/Region': 'Country'})
    return (output_data)


def fill_missing(input_data):
    output_data = input_data.fillna(value={'Province/State': ''})
    return (output_data)


#melt permit to unpivot the data
def melt_data(input_data, value_name_case):
    output_data = input_data.melt(
        id_vars=['Country', 'Province/State', 'Lat', 'Long'],
        var_name='Date',
        value_name=value_name_case)
    return (output_data)


def convert_dates(input_data):
    output_data = input_data.assign(
        date=pd.to_datetime(input_data.Date, format='%m/%d/%y'))
    output_data.drop(columns=['Date'], inplace=True)
    return (output_data)


def rearrange_data(input_data, value_name_case):
    output_data = input_data.filter([
        'Country', 'Province/State', 'date', 'Lat', 'Long', value_name_case
    ]).sort_values(['Country', 'Province/State', 'date', 'Lat', 'Long'])
    return (output_data)


def get_data(input_url, value_name_case):
    data = pd.read_csv(input_url)
    data = rename_columns(data)
    data = fill_missing(data)
    data = melt_data(data, value_name_case)
    data = convert_dates(data)
    data = rearrange_data(data, value_name_case)
    return (data)


def get_data_covid():
    url_confirmed = '{url}time_series_covid19_confirmed_global.csv'.format(
        url=base_url)
    url_deaths = '{url}time_series_covid19_deaths_global.csv'.format(
        url=base_url)
    url_recovered = '{url}time_series_covid19_recovered_global.csv'.format(
        url=base_url)
    confirmed_df = get_data(url_confirmed, 'Confirmed')
    deaths_df = get_data(url_deaths, 'Dead')
    recovered_df = get_data(url_recovered, 'Recovered')
    country_df = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv'
    )

    #drop colomn to remove dupplicate column
    recovered_df.drop(columns=['Lat', 'Long'], inplace=True)
    deaths_df.drop(columns=['Lat', 'Long'], inplace=True)

    #Merge the data to one df
    covid_df = (confirmed_df.merge(
        deaths_df, on=['Country', 'Province/State', 'date'],
        how='left').merge(recovered_df,
                          on=['Country', 'Province/State', 'date'],
                          how='left'))
    #Calculate new cases
    covid_df['new_cases'] = (covid_df.sort_values(
        by=['Country', 'Province/State', 'date']).filter([
            'Country', 'Province/State', 'date', 'Confirmed'
        ]).groupby(['Country', 'Province/State']).Confirmed.diff())
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    covid_data_Yesterday = (covid_df[covid_df['date'] == pd.Timestamp(
        yesterday)].groupby('Country').agg('sum').sort_values(
            'Confirmed', ascending=False).reset_index())

    confirmed_by_date_US_xUS = (covid_df.assign(
        US_flg=np.where((covid_df.Country == 'US') | (
            covid_df.Country == 'Brazil'), 'US & Brazil', 'Others')).filter([
                'date', 'Confirmed', 'US_flg'
            ]).groupby(['date', 'US_flg']).agg('sum').reset_index())

    confirmed_top_countries = (covid_df.filter([
        'date', 'Country', 'Confirmed'
    ]).query('Country in ["US","Brazil","Russia","India","France"] ').groupby(
        ['date', 'Country']).agg('sum').reset_index())

    Top10_country = (covid_data_Yesterday.filter(
        ['Country', 'Confirmed']).groupby('Country').agg('sum').sort_values(
            'Confirmed', ascending=False).reset_index()).head(10)

    return {
        'covid_df': covid_df,
        'covid_data_Yesterday': covid_data_Yesterday,
        "confirmed_by_date_US_xUS": confirmed_by_date_US_xUS,
        "confirmed_top_countries": confirmed_top_countries,
        "Top10_country": Top10_country,
        "country_df":country_df,
    }
