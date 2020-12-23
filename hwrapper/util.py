from datetime import datetime

def time_format(t):
    return datetime.utcfromtimestamp(t).strftime('%m-%d-%Y')