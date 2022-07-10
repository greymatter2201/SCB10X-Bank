# SCB 10X Bank

A simple bank contract with a frontend

Contract Deployed at: 0xfdfaA2483E69fdbCd93faC9B128741F31f875F4d

## Contract Features
* Account Creation 
* Deposit ERC20
* Withdraw ERC20
* Transfer ERC20 by Account Name
* Multiple ERC20 Transfer by Account Name
* 1% fee for transfers to account names not owned by caller
* Able to work with and keep balance of any ERC20 Contract (Not implemented on the frontend)

### Dependencies

You will need
* eth-brownie
* flask
* ganache

### Installing

* Install requirements from requirements txt file

### Executing program
* CD into project folder

```
export FLASK_APP=web.py
flask run
```

### Running tests (Local Rinkeby Fork)

* Set up RPC node for a rinkeby fork
* Add network configuration to brownie networks
```
brownie test --network $NETWORK_NAME
```

### Issues
* ~~Clicking withdraw in the UI somehow calls the deposit function and vice versa~~ 
