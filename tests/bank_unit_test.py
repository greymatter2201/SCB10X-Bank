from platformdirs import user_runtime_dir
from scripts.deploy_bank import deploy_bank
from scripts.scripts import (
    get_account,
    get_DAI_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS

)
from brownie import network, Wei, accounts
import pytest
from web3 import Web3

# Act, Arrange, Assert


def test_createAccount():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    DAI = get_DAI_contract()
    user_account = get_account()
    bank_contract = deploy_bank(user_account)

    username = Web3.toHex(b"USER1")

    #Create an account by specifing username
    bank_contract.createAccount(username, {"from": user_account})

    #Get account address from accountAddr mapping
    addr_on_contract = bank_contract.accountAddr(username)

    assert addr_on_contract == user_account.address

def test_ERC20_approve():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    DAI = get_DAI_contract()
    user_account = get_account()
    bank_contract = deploy_bank(user_account)

    amount = Wei("1 ether")

    #Approving bank contract for ERC20 transfer
    DAI.approve(bank_contract, amount, {"from": user_account})
    approved_amount = DAI.allowance(user_account, bank_contract)
    assert approved_amount == amount

def test_deposit():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    DAI = get_DAI_contract()
    user_account = get_account()
    bank_contract = deploy_bank(user_account)

    amount = Wei("1 ether")
    username = Web3.toHex(b"USER1")

    #Create Account
    bank_contract.createAccount(username, {"from": user_account})

    #Approving bank contract for ERC20 transfer from user_account
    DAI.approve(bank_contract, amount, {"from": user_account})

    #Transferring to bank contract 
    bank_contract.deposit(amount, DAI.address, username, {"from": user_account})

    bank_balance = DAI.balanceOf(bank_contract)
    bank_accountBalances = bank_contract.accountBalances(DAI.address, username)

    assert bank_balance == amount == bank_accountBalances

def test_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    DAI = get_DAI_contract()
    user_account = get_account()
    bank_contract = deploy_bank(user_account)

    amount = Wei("1 ether")
    username = Web3.toHex(b"USER1")

    #Create an account by specifing username
    bank_contract.createAccount(username, {"from": user_account})

    #Approving bank contract for ERC20 transfer from user_account
    DAI.approve(bank_contract, amount, {"from": user_account})

    #Transferring to bank contract
    bank_contract.deposit(amount, DAI.address, username, {"from": user_account})

    user_balance_b4 = DAI.balanceOf(user_account)

    #Caling withdraw
    bank_contract.withdraw(amount, DAI.address, username, {"from": user_account})

    user_balance_aft = DAI.balanceOf(user_account)

    assert (user_balance_aft - user_balance_b4) == amount

def test_transfer_by_name():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    DAI = get_DAI_contract()
    user_acc_1 = get_account()
    bank_contract = deploy_bank(user_acc_1)

    amount = Wei("1 ether")

    username_1 = Web3.toHex(b"JAMES-ACC1")
    username_2 = Web3.toHex(b"JAMES-ACC2")

    #Creating 2 accounts for the same address
    bank_contract.createAccount(username_1, {"from": user_acc_1})
    bank_contract.createAccount(username_2, {"from": user_acc_1})

    #Approving bank contract for ERC20 transfer from user_account
    DAI.approve(bank_contract, amount, {"from": user_acc_1})

    #Transferring to bank contract 
    bank_contract.deposit(amount, DAI.address, username_1, {"from": user_acc_1})

    #Transferring from username_1 to username_2
    bank_contract.transfer(amount, username_1, username_2, DAI.address, {"from": user_acc_1})

    #Getting balance of username_2
    username_2_balance = bank_contract.getAccountBalance(username_2, DAI.address)

    assert username_2_balance == amount

def test_transfer_fee_deduction():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    DAI = get_DAI_contract()
    user_acc_1 = get_account()
    test_acc_1 = accounts.load("test_account_1")
    bank_contract = deploy_bank(user_acc_1)

    amount = Wei("1 ether")
    amount_after_fee = amount - (amount * 0.1)

    user_name = Web3.toHex(b"COPPER")
    test_name = Web3.toHex(b"RAYMAN")

    #Creating accounts
    bank_contract.createAccount(user_name, {"from": user_acc_1})
    bank_contract.createAccount(test_name, {"from": test_acc_1})

    #Approving bank contract for ERC20 transfer from user_account
    DAI.approve(bank_contract, amount, {"from": user_acc_1})

    #Transferring to bank contract 
    bank_contract.deposit(amount, DAI.address, user_name, {"from": user_acc_1})

    #Transferring from user_name to test_name
    bank_contract.transfer(amount, user_name, test_name, DAI.address, {"from": user_acc_1})

    #Balance of test_name
    test_name_balance = bank_contract.getAccountBalance(test_name, DAI.address)

    assert test_name_balance == amount_after_fee