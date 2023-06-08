import requests
from datetime import datetime
import datetime
import pytz


def check_incoming_transactions(wallet_address, transaction_sum, since_timestamp):
    api_url = f'https://api.trongrid.io/v1/accounts/{wallet_address}/transactions/trc20'
    params = {
        'limit': 100,  # Adjust the limit as per your requirement
        'order_by': 'block_timestamp,desc',
        'only_confirmed': 'true',
        'contract_address': 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t'
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        transactions = data['data']

        # Get the Europe/Moscow timezone
        moscow_timezone = pytz.timezone('Europe/Moscow')

        for transaction in transactions:
            transaction_sum_usdt = int(transaction['value']) / 10 ** 6
            transaction_timestamp = transaction['block_timestamp'] / 1000

            if transaction_sum_usdt == transaction_sum and transaction_timestamp >= int(since_timestamp):
                transaction_id = transaction['transaction_id']
                utc_timestamp = datetime.datetime.utcfromtimestamp(transaction_timestamp)
                moscow_timestamp = utc_timestamp.replace(tzinfo=pytz.utc).astimezone(moscow_timezone)
                timestamp = moscow_timestamp.strftime('%Y-%m-%d %H:%M:%S')
                sender_address = transaction['from']

                print(f"Incoming transaction found:")
                print(f"Transaction ID: {transaction_id}")
                print(f"Timestamp (Europe/Moscow): {timestamp}")
                print(f"Sender Address: {sender_address}")
                print(f"Amount: {transaction_sum_usdt} USDT")
                print("-------------------------------")
                return True

        print("End of transactions.")
        return False

    else:
        print(f"Failed to retrieve transactions. Error: {response.status_code}")
        return False


# # Example usage
# wallet_address = 'THLLZCpaXjQuTXcX8UCh1iyKzZB7bxrqyL'
# transaction_sum = 186  # USDT
# since_timestamp = 1683972060  # Unix timestamp representing the desired start time
#
# check_incoming_transactions('TSTbcGNyVv6a92iXKmSfpZMBg8qP7EAMAs', 0.99057, 1685717737)
