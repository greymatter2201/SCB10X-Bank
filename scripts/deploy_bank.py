import json, os
from scripts.scripts import get_account, get_local_account
from brownie import Bank, config, network

def deploy_bank(deployer_addr):
    publish_source = config['networks'][network.show_active()].get("verify", False)
    bank_contract = Bank.deploy(
        {"from": deployer_addr},
        publish_source = publish_source
    )
    return bank_contract

def main():
   deployer_acc = get_account()
   deploy_bank(deployer_acc)


    
    
    
    