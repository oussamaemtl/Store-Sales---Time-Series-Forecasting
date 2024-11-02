from os import listdir
from os.path import isfile, join

import pandas as pd
from config import (
    FILE_CORRESPONDANCE_HB,
    FILE_CORRESPONDANCE_SLG,
    FILE_DEMAND_AIF,
    FILE_MARKET_TREND,
    PATH_DEMAND_AIF,
    PATH_GROUP_SM,
    PATH_HOLIDAYS,
    PATH_MARKET_TREND,
    PATH_SALES,
)


def import_sales(mypath=PATH_SALES):
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    return pd.concat(
        [
            pd.read_parquet(f"{mypath}{f}")
            for f in listdir(mypath)
            if isfile(join(mypath, f))
        ]
    )


def import_group_sm(path=PATH_GROUP_SM):
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    return pd.concat(
        [
            pd.read_excel(f"{path}{FILE_CORRESPONDANCE_HB}")[
                ["group", "SM"]
            ].drop_duplicates(),
            pd.read_excel(f"{path}{FILE_CORRESPONDANCE_SLG}")[
                ["group", "SM"]
            ].drop_duplicates(),
        ]
    ).drop_duplicates()


def import_market_trend(path=PATH_MARKET_TREND):
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    return pd.read_parquet(f"{path}{FILE_MARKET_TREND}")


def import_demand_aif(mypath=PATH_DEMAND_AIF):
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    df_demand = pd.read_parquet(f"{mypath}{FILE_DEMAND_AIF}")
    df_demand["day_week"] = pd.to_datetime(df_demand.week_id)
    df_demand["week_id"] = pd.to_datetime(df_demand["week_id"])
    df_demand = df_demand[
        (df_demand["day_week"] > "2020-12-31") & (df_demand["day_week"] < "2025-01-01")
    ]
    df_demand["sm"] = df_demand["style_color_code"].apply(lambda x: x[:-4])
    df_demand["day_week"] = df_demand["day_week"].dt.tz_localize(None)
    df_demand["week_id"] = df_demand["week_id"].dt.tz_localize(None)

    return df_demand


def import_holidays(date_flag, mypath=PATH_HOLIDAYS):
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    onlyfiles = [
        f.replace(".xlsx", "") for f in listdir(mypath) if isfile(join(mypath, f))
    ]
    dico_calendar_merch = {}
    for file in onlyfiles:
        dico_calendar_merch[file] = pd.read_excel(f"{mypath}{file}.xlsx")

    dico_replace = {
        "MiddleEast": "AED",
        "China": "CNY",
        "Europe": "EUR",
        "HongKong": "HKD",
        "Japan": "JPY",
        "Korea": "KRW",
        "USA": "USD",
    }

    dico_calendar_merch["holiday"]["currency"] = dico_calendar_merch["holiday"][
        "rfc_channel_desc"
    ].replace(dico_replace)
    holidays = dico_calendar_merch["holiday"][
        (dico_calendar_merch["holiday"]["ds"] >= date_flag)
    ]
    holidays["macrozone_desc"] = holidays["rfc_channel_desc"]
    return holidays


def filter_sales(df_sales, time_axis, group_id, currency, date_flag):
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    df_sales_study = df_sales[
        (df_sales["group"] == group_id)
        & (df_sales["currency"] == currency)
        & (df_sales[time_axis] >= date_flag)
    ]

    df_sales_study.set_index("purchase_date", inplace=True)
    # df_sales_study['week_sunday'] = (df_sales_study.index - pd.DateOffset(days=1)).to_period('W-SUN')
    df_sales_study["week_id"] = df_sales_study.index.to_period("W-SUN")

    # Grouper par "group", "shape", "type", "line", "currency" et par semaine
    df_sales_study = df_sales_study.groupby(
        ["type", "line", "group", "week_id"], as_index=False
    ).agg(
        {
            "qty": "sum",
            "qty_stockout_free": "sum",
            "qty_lockdown_free": "sum",
            "qty_redressed": "sum",
        }
    )
    df_sales_study["week_id"] = df_sales_study["week_id"].dt.to_timestamp()
    df_sales_study["week_id"] = df_sales_study["week_id"] + pd.DateOffset(
        days=-1
    )  # Move from Monday to Sunday
    df_sales_study["week_id"] = df_sales_study["week_id"].dt.tz_localize(None)
    return df_sales_study


def filter_df_flag(df_flag, group_id, currency, date_flag):
    return df_flag[
        (df_flag["group"] == group_id)
        & (df_flag["currency"] == currency)
        & ((df_flag["price_var"] > 0) | (df_flag["price_var"] < 0))
        & (df_flag["start_date"] >= date_flag)
    ]


def filter_market_trend(df_market_trend_aif, market, date_flag, dept, subdpt):
    df_market_trend_study = df_market_trend_aif[
        df_market_trend_aif.subregion_desc == market
    ]
    df_market_trend_study["date_week"] = pd.to_datetime(
        df_market_trend_study["week_id"]
    )
    df_market_trend_study["date_week"] = df_market_trend_study[
        "date_week"
    ].dt.tz_localize(None)
    df_market_trend_study = df_market_trend_study[
        df_market_trend_study.week_id >= date_flag
    ]
    df_market_trend_study = df_market_trend_study[
        df_market_trend_study.department_desc == dept
    ]
    df_market_trend_study = df_market_trend_study[
        df_market_trend_study.subdepartment_desc == subdpt
    ]
    df_market_trend_study = df_market_trend_study.drop_duplicates(
        subset=["market_trend", "date_week"]
    )
    df_market_trend_study = df_market_trend_study.sort_values(by="date_week")

    return df_market_trend_study


def filter_holiday(holidays, currency):
    _holidays = holidays[holidays["currency"] == currency]
    _holidays["ds"] = pd.to_datetime(_holidays["ds"])
    _holidays = _holidays[["ds", "holiday"]]
    return _holidays
