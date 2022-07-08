from web3 import Web3, WebsocketProvider, HTTPProvider
from web3.middleware import geth_poa_middleware
import json, os
from scripts.scripts import get_account, get_local_account
from brownie import Bank


def get_web3(address):
    w3 = Web3(HTTPProvider(address))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3

def get_DAI_contract(w3, contract_addr, abi):
    contract = w3.eth.contract(contract_addr, abi=abi)
    return contract

def get_DAI_abi():
    current_path = os.path.abspath(os.path.dirname(__file__))
    file_path = str(os.path.join(current_path, 'DAI.json'))

    with open(file_path) as f:
        abi_info = json.load(f)
    
    abi = abi_info["result"]

    return abi

def deploy_bank(deployer_addr):
    bank_deploy = Bank.deploy({"from": deployer_addr})
    return bank_deploy


def main():

    # local_account = get_local_account()
    # main_account = get_account()
    # main_account_str = str(main_account)

    # bank_contract = deploy_bank(main_account)
    # bank_addr = str(bank_contract)

    # DAI_addr = "0x5eD8BD53B0c3fa3dEaBd345430B1A3a6A4e8BD7C"
    # w3 = get_web3("https://rinkeby.infura.io/v3/b5ad7d0fbc744c4688841ebd4bfde736")

    # assert True is w3.isConnected()
    # print("Connected")

    # abi = get_DAI_abi()
    # DAI = get_DAI_contract(w3, DAI_addr, abi)  

    # balance = DAI.functions.balanceOf(main_account_str).call()
    # print(balance)

    # allowance = DAI.functions.allowance(str(main_account), bank_addr).call()
    # print(allowance)
 
    # tx_hash = DAI.functions.approve(str(bank_addr), 200).transact({"from": main_account_str})
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # allowance = DAI.functions.allowance(str(main_account), bank_addr).call()
    # print(allowance)
    

    