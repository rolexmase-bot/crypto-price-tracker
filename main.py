import requests
import pandas as pd

url = 'https://api.coingecko.com/api/v3/coins/markets'

params = {
    'vs_currency': 'usd',
    'ids': (
        'bitcoin,ethereum,solana,dogecoin,'
        'ripple,cardano,tron,chainlink,'
        'litecoin,avalanche-2'
    ),
    'order': 'market_cap_desc',
    'per_page': 10,
    'page': 1,
    'sparkline': 'false'
}

headers = {
    'User-Agent': 'Mozilla/5.0'
}

print('Fetching crypto market data...\n')

try:
    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    crypto_data = []

    for coin in data:

        name = coin['name']
        symbol = coin['symbol'].upper()
        price = coin['current_price']

        # Format market cap with commas
        market_cap = f"{coin['market_cap']:,}"

        print(f'{name} ({symbol}) - ${price}')

        crypto_data.append({
            'Name': name,
            'Symbol': symbol,
            'Price (USD)': price,
            'Market Cap': market_cap
        })

    # Create DataFrame
    df = pd.DataFrame(crypto_data)

    # Export Excel
    output_file = 'crypto_prices.xlsx'

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:

        df.to_excel(writer, index=False, sheet_name='Crypto Prices')

        worksheet = writer.sheets['Crypto Prices']

        # Auto adjust column width
        for column in worksheet.columns:

            max_length = 0
            column_letter = column[0].column_letter

            for cell in column:

                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass

            adjusted_width = max_length + 5

            worksheet.column_dimensions[column_letter].width = adjusted_width

    print(f'\nSuccessfully saved data to {output_file}')

except requests.exceptions.RequestException as e:
    print(f'Error: {e}')