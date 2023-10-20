# Import all required directries
import re
from dateutil.parser import parse
from datetime import datetime, date

# -----------------------------------------------
# function to get dates from text 
def get_dates(text):
    date_pattern = r'\d{2,4} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2,4}|\d{2,4} \w{3}\.\d{2,4}|\d{2,4}\/\d{2}\/\d{2,4}|\d{2,4}\-\d{2}\-\d{2,4}'
    dates = re.findall(date_pattern, text)
    return dates

# Convert date strings to datetime objects
def convert_text_to_date(dates):
    try:
        date = parse(dates, fuzzy=True)
        return date.strftime('%d/%m/%Y')
    except ValueError:
        return None

def format_dates(dates):
    formatted_dates = []
    for date in dates:
        try:
            formatted_date = datetime.strptime(date, '%d/%m/%Y')
            formatted_dates.append(formatted_date.strftime('%Y-%m-%d'))
        except ValueError:
            try:
                formatted_date = datetime.strptime(date, '%d/%m/%y')
                formatted_dates.append(formatted_date.strftime('%Y-%m-%d'))
            except ValueError:
                print(f"Unable to parse date: {date}")
    return formatted_dates