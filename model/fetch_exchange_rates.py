import requests
import pandas as pd
from datetime import datetime, timedelta

api_key = '4229ab1419bd4525b0a7db1e14bc1022'
base_url = 'https://openexchangerates.org/api/historical/'

base_currency = 'USD'
target_currency = 'INR'

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 5, 28)  
data = []
current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime('%Y-%m-%d')
    url = f'{base_url}{date_str}.json?app_id={api_key}&base={base_currency}&symbols={target_currency}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        rate = response.json()['rates'][target_currency]
        data.append({'date': date_str, 'exchange_rate': rate})
    except requests.exceptions.RequestException as e:
        print(f'Failed to fetch data for {date_str}: {e}')
    
    current_date += timedelta(days=1)

# Convert the list to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('historical_exchange_rates.csv', index=False)

print("Data fetching complete. CSV file saved as 'historical_exchange_rates.csv'.")
