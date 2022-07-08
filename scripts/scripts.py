from brownie import (
    network,
    accounts,
    config
)

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development', 'rinkeby-local, rinkeby-private']

def get_local_account(index=0):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[index]
    
def get_account():
    return accounts.add(config['wallets']['from_key'])
