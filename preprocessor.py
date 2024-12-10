import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    # Define the regex pattern to split messages and extract dates
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?[APMapm]{2}\s-\s'

    # Split messages and extract dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Convert 12-hour format with AM/PM to 24-hour format
    new_dates = []
    for date_str in dates:
        date_str = date_str.strip(' -')
        in_time = datetime.strptime(date_str, "%d/%m/%y, %I:%M %p")
        out_time = in_time.strftime("%d/%m/%Y, %H:%M:%S")
        new_dates.append(out_time)

    # Check if the number of extracted dates matches the number of messages
    if len(new_dates) != len(messages):
        raise ValueError("The number of dates and messages extracted do not match. Please check the input data format.")

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': new_dates})

    # Convert message_date to datetime object
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M:%S')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if len(entry) > 2:  # username is present
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract date components
    df['only_date'] = df['date'].dt.strftime('%d/%m/%Y')
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['second'] = df['date'].dt.second

    # Calculate periods
    df['period'] = df['hour'].apply(lambda x: f"{x:02d}-{(x + 1) % 24:02d}")

    return df
