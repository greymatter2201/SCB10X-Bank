from platformdirs import user_runtime_dir
from scripts.deploy_bank import deploy_bank
from scripts.scripts import (
    get_account,
    get_local_account,
    get_DAI_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS

)
from brownie import network, Wei, accounts
import pytest
from web3 import Web3

# -- Tests are done on a Local Rinkeby Fork --

# Create new bank account specifying account name
def test_createAccount():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    DAI = get_DAI_contract()
    user_account = get_local_account()
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
    user_account = get_local_account()
    bank_contract = deploy_bank(user_account)

    amount = Wei("1 ether")

    #Funding account with DAI
    DAI.mint(user_account, amount, {"from": user_account})

    #Approving bank contract for ERC20 transfer
    DAI.approve(bank_contract, amount, {"from": user_account})
    approved_amount = DAI.allowance(user_account, bank_contract)
    assert approved_amount == amount

# Recharge/Deposit arbitary amount of ERC20 
def test_deposit():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    DAI = get_DAI_contract()
    user_account = get_local_account()
    bank_contract = deploy_bank(user_account)

    amount = Wei("1 ether")
    username = Web3.toHex(b"USER1")

    #Funding account with DAI
    DAI.mint(user_account, amount, {"from": user_account})

    #Create Account
    bank_contract.createAccount(username, {"from": user_account})

    #Approving bank contract for ERC20 transfer from user_account
    DAI.approve(bank_contract, amount, {"from": user_account})

    #Transferring to bank contract 
    bank_contract.deposit(amount, DAI.address, username, {"from": user_account})

    bank_balance = DAI.balanceOf(bank_contract)
    bank_accountBalances = bank_contract.accountBalances(DAI.address, username)

    assert bank_balance == amount == bank_accountBalances

# Withdraw an arbitary amount of ERC20 from balance
def test_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    DAI = get_DAI_contract()
    user_account = get_local_account()
    bank_contract = deploy_bank(user_account)

    amount = Wei("1 ether")
    username = Web3.toHex(b"USER1")

    #Funding account with DAI
    DAI.mint(user_account, amount, {"from": user_account})

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

# Transfer to another account by account name
def test_transfer_by_name():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    DAI = get_DAI_contract()
    user_acc_1 = get_local_account()
    bank_contract = deploy_bank(user_acc_1)

    amount = Wei("1 ether")

    #Funding account with DAI
    DAI.mint(user_acc_1, amount, {"from": user_acc_1})

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

# Transfers to accounts not owned by caller results in a 1% fee
def test_transfer_fee_deduction():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    DAI = get_DAI_contract()
    user_acc_1 = get_local_account()
    #Test account prefunded with eth for gas
    test_acc_1 = get_local_account(1)
    bank_contract = deploy_bank(user_acc_1)

    amount = Wei("1 ether")
    amount_after_fee = amount - (amount * 0.1)

    #Funding account with DAI
    DAI.mint(user_acc_1, amount, {"from": user_acc_1})
    
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

# Transfer amount in balance to multiple account names
def test_multiTransfer():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    DAI = get_DAI_contract()
    user_account = get_local_account()
    bank_contract = deploy_bank(user_account)

    amount = Wei("5 ether")

    #Funding account with DAI
    DAI.mint(user_account, amount, {"from": user_account})

    main_user = Web3.toHex(b'HADES')
    usernames = [b'POSEIDON', b'ZEUS', b'ARES', b'ATHENA', b'DIONYSUS']
    usernames_hex = [Web3.toHex(name) for name in usernames]

    bank_contract.createAccount(main_user, {"from": user_account})

    #Create 5 accounts with different names
    for username in usernames_hex:
        bank_contract.createAccount(username, {"from": user_account})

    #Approving bank contract for ERC20 transfer from user_account
    DAI.approve(bank_contract, amount, {"from": user_account})

    #Transferring to bank contract 
    bank_contract.deposit(amount, DAI.address, main_user, {"from": user_account})

    #Transferring to multiple acccounts by name
    bank_contract.multiTransfer(
        Wei("1 ether"), main_user, usernames_hex, DAI.address, {"from": user_account}
    )

    account_balances = []
    for username in usernames_hex:
        balance = bank_contract.getAccountBalance(username, DAI.address)
        account_balances.append(balance)
    
    expected_balances = [Wei("1 ether") for _ in range(5)]

    assert expected_balances == account_balances