import json, os
from scripts.scripts import get_account, get_local_account
from brownie import Bank

def deploy_bank(deployer_addr):
    bank_contract = Bank.deploy({"from": deployer_addr})
    return bank_contract

def main():
    account = get_account()
    bank_contract = deploy_bank(account)

    
    
    
    