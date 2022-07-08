import json, os
from scripts.scripts import get_account, get_local_account
from brownie import Bank, Contract


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
    abi = get_DAI_abi()
    main_account = get_account()
    bank_contract = deploy_bank(main_account)

    DAI = Contract.from_abi("DAI", "0x5eD8BD53B0c3fa3dEaBd345430B1A3a6A4e8BD7C", abi)
    print(DAI)

    allowance = DAI.allowance(main_account, bank_contract.address)
    print(allowance)
    tx = DAI.approve(bank_contract.address, 1000000000000000000, {"from": main_account})
    tx.wait(1)
    allowance = DAI.allowance(main_account, bank_contract.address)
    print(allowance)

    bank_allowance = bank_contract.checkAllowance(main_account, bank_contract.address, "0x5eD8BD53B0c3fa3dEaBd345430B1A3a6A4e8BD7C")
    print(bank_allowance)
    
    