import datetime
def convertToDate(timestamp):
    # Convert the timestamp to a datetime object
    datetime_obj = datetime.datetime.utcfromtimestamp(timestamp)
    target_date_str = '2023-09-11 04:57:48 UTC'
    target_date = datetime.datetime.strptime(target_date_str, '%Y-%m-%d %H:%M:%S UTC')
    if datetime_obj< target_date:
        return False
    return True