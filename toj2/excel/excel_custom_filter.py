from openpyxl import utils
from datetime import datetime

def excel_time(excel_value, format='%Y/%m/%d'):

    dt_object = None

    if isinstance(excel_value, datetime):
        dt_object = excel_value
    elif isinstance(excel_value, int) or isinstance(excel_value, float):
        dt_object = utils.datetime.from_excel(excel_value)
    else:
        return excel_value

    return dt_object.strftime(format)
