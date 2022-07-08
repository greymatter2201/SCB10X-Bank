from scripts.deploy_bank import deploy_bank
from scripts.scripts import (
    get_account,
    get_rand_account,
    get_DAI_contract,
    get_w3_provider, 
    LOCAL_BLOCKCHAIN_ENVIRONMENTS

)
from brownie import network, Wei
import pytest

# Act, Arrange, Assert


def test_createAccount():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    DAI = get_DAI_contract()
    user_account = get_account()
    bank_contract = deploy_bank(user_account)

    username = "USER1".encode('utf-8')

    #Create Account
    bank_contract.createAccount(username, user_account, {"from": user_account})

    #Getting address from the clientNames mapping
    address = bank_contract.clientNames(username)

    assert user_account.address == address

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

    #Approving bank contract for ERC20 transfer from user_account
    DAI.approve(bank_contract, amount, {"from": user_account})

    #Transferring to bank contract and checking balance via ERC20 contract
    bank_contract.deposit(amount, DAI.address, {"from": user_account})
    bank_balance = DAI.balanceOf(bank_contract)
    assert bank_balance == amount

def test_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    DAI = get_DAI_contract()
    user_account = get_account()
    bank_contract = deploy_bank(user_account)

    amount = Wei("1 ether")

    #Approving bank contract for ERC20 transfer from user_account
    DAI.approve(bank_contract, amount, {"from": user_account})

    #Transferring to bank contract
    bank_contract.deposit(amount, DAI.address, {"from": user_account})

    user_balance_b4 = DAI.balanceOf(user_account)

    #Caling withdraw
    bank_contract.withdraw(amount, DAI.address, {"from": user_account})

    user_balance_aft = DAI.balanceOf(user_account)

    assert (user_balance_aft - user_balance_b4) == amount

def test_transfer_by_name():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    DAI = get_DAI_contract()
    user_acc_1 = get_account()
    user_acc_2 = get_rand_account()
    bank_contract = deploy_bank(user_acc_1)

    amount = Wei("1 ether")

    user1 = "JAMES-ACC1".encode('utf-8')
    user2 = "JAMES-ACC2".encode('utf-8')

    #Creating accounts for both users
    bank_contract.createAccount(user1, user_acc_1, {"from": user_acc_1})
    bank_contract.createAccount(user2, user_acc_1, {"from": user_acc_1})

    #Approving bank contract for ERC20 transfer from user_acc_1
    DAI.approve(bank_contract, amount, {"from": user_acc_1})

    #Transferring to bank contract
    bank_contract.deposit(amount, DAI.address, {"from": user_acc_1})

    #Transferring to other account by account name
    bank_contract.transfer(amount, user2, DAI.address, {"from": user_acc_1})

    #Getting balance of user2 in the contract
    user2_balance = bank_contract.clientTotalBalance(DAI.address, user_acc_2)

    assert user2_balance == amount


