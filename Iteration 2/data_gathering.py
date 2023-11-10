# Function that gather data and store in the database created earlier

import time
import os
from web3 import Web3, HTTPProvider
import Database  

# API Key
INFURA_PROJECT_ID = os.getenv('Brownie-Detector')
CONTRACT_ADDRESS = os.getenv('28d6fc2451a94161a52d57214eb9153f')

# connection to the Ethereum  Infra
infura_url = f'https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}'
web3 = Web3(HTTPProvider(infura_url))


contract_address = Web3.toChecksumAddress(CONTRACT_ADDRESS)

# This is the function that do the collection
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
                # This is were data is suppposed to inserted in Database created in database.py
                Database.insert_transaction(tx.hash.hex(), tx_receipt.gasUsed, block.timestamp)
    except Exception as e:
        # Log creation for the user
        print(f"An error occurred: {e}")
    finally:
        # Infra key have limit on key request
        time.sleep(10) 

# Run the data collection function
# TODO: Change for to while
for _ in range(10): 
    collect_gas_usage()
    time.sleep(14)  
    # Ethereum typically has a new block every ~15 seconds
