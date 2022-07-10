from brownie import (
    network,
    accounts,
    config,
    Contract,
)
from web3 import Web3
import os, json

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development', 'rinkeby-local', 'rinkeby-private', 'rinkeby-local-fork']

def get_local_account(index=0):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[index]
    
def get_account():
    return accounts.add(config['wallets']['from_key'])

def get_rand_account():
    return accounts.add()

def get_bank_contract():
    return Contract("0xfdfaA2483E69fdbCd93faC9B128741F31f875F4d")

def get_DAI_contract():
    current_path = os.path.abspath(os.path.dirname(__file__))
    file_path = str(os.path.join(current_path, 'DAI.json'))

    with open(file_path) as f:
        abi_info = json.load(f)
    
    abi = abi_info["result"]

    DAI = Contract.from_abi("DAI", "0x5eD8BD53B0c3fa3dEaBd345430B1A3a6A4e8BD7C", abi)
    return DAI

def createAccount(username, user_addr):
    username = Web3.toHex(username.encode('utf-8'))
    bank_contract = get_bank_contract()

    created = bank_contract.createAccount(username, {"from": user_addr})

    return created

def balanceDAI(username):
    username = Web3.toHex(username.encode('utf-8'))

    bank_contract = get_bank_contract()
    DAI_contract = get_DAI_contract()

    balance = bank_contract.getAccountBalance(username, DAI_contract.address)

    return balance

def depositDAI(amount, username, user_addr):
    username = Web3.toHex(username.encode('utf-8'))
    amount = int(amount)

    bank_contract = get_bank_contract()
    DAI_contract = get_DAI_contract()

    approve = DAI_contract.approve(bank_contract, amount,{"from": user_addr})
    deposit = bank_contract.deposit(amount, DAI_contract.address, username, {"from": user_addr})

    return (approve and deposit)

def withdrawDAI(amount, username, user_addr):
    username = Web3.toHex(username.encode('utf-8'))
    amount = int(amount)

    bank_contract = get_bank_contract()
    DAI_contract = get_DAI_contract()

    withdraw = bank_contract.withdraw(amount, DAI_contract.address, username, {"from": user_addr})

    return withdraw

def transferDAI(amount, from_name, to_name, user_addr):
    from_name = Web3.toHex(from_name.encode('utf-8'))
    to_name = Web3.toHex(to_name.encode('utf-8'))

    amount = int(amount)

    bank_contract = get_bank_contract()
    DAI_contract = get_DAI_contract()

    transfer = bank_contract.transfer(
        amount, from_name, to_name, DAI_contract.address, {"from": user_addr}
    )

    return transfer

def multiTransferDAI(amount, from_name, to_name_arr, user_addr):
    from_name = Web3.toHex(from_name.encode('utf-8'))
    to_name_arr = [Web3.toHex(name.encode('utf-8')) for name in to_name_arr]
    
    bank_contract = get_bank_contract()
    DAI_contract = get_DAI_contract()

    multiTransfer = bank_contract.multiTransfer(
        amount, from_name, to_name_arr, DAI_contract.address, {"from": user_addr}
    )

    return multiTransfer