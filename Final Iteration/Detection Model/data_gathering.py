import time
import os
from web3 import Web3, HTTPProvider
import Database  
import app

# API Key and contract details
INFURA_PROJECT_ID = os.getenv('Brownie-Detector')
CONTRACT_ADDRESS = os.getenv(app.form_data['blockchain'])

# Connect to the Ethereum Infrastructure
infura_url = f'https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}'
web3 = Web3(HTTPProvider(infura_url))
contract_address = Web3.toChecksumAddress(CONTRACT_ADDRESS)

# Function to collect gas usage data
def collect_gas_usage():
    if not web3.isConnected():
        print("Failed to connect to Infura. Retrying...")
        time.sleep(10)
        return

    try:
        block = web3.eth.get_block('latest', full_transactions=True)
        for tx in block.transactions:
            if tx.to and Web3.toChecksumAddress(tx.to) == contract_address:
                tx_receipt = web3.eth.getTransactionReceipt(tx.hash)
                # Insert the transaction data into the current_transactions table
                Database.insert_current_transaction(tx.hash.hex(), tx_receipt.gasUsed, block.timestamp)
                break
            
        total_transactions = len(block.transactions)
        n = app.form_data['num_transactions']- 1 

        if n > total_transactions:
            n= total_transactions

        # Insert rest of the transaction in the historical transactioins table
        for i in range(1, n):
            Database.store_historical_transactions(block.transactions[-i])

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        time.sleep(10)  # Limit key requests



if __name__ == "__main__":
    collect_gas_usage() 
    # time.sleep(14)  # Ethereum typically has a new block every ~15 seconds

    # time is for iteratively running the program
