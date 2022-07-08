from brownie import (
    network,
    accounts,
    config,
    Contract
)

from web3 import Web3, WebsocketProvider
import os, json

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development', 'rinkeby-local', 'rinkeby-private', 'rinkeby-local-fork']

def get_local_account(index=0):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[index]
    
def get_account():
    return accounts.add(config['wallets']['from_key'])

def get_rand_account():
    return accounts.add()

def get_DAI_contract():
    current_path = os.path.abspath(os.path.dirname(__file__))
    file_path = str(os.path.join(current_path, 'DAI.json'))

    with open(file_path) as f:
        abi_info = json.load(f)
    
    abi = abi_info["result"]

    DAI = Contract.from_abi("DAI", "0x5eD8BD53B0c3fa3dEaBd345430B1A3a6A4e8BD7C", abi)
    return DAI

def get_w3_provider():
    w3 = Web3(WebsocketProvider("ws://127.0.0.1:8545"))
    return w3

def main():
   pass
