// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
  function allowance(address owner, address spender) external view returns (uint256 remaining);
  function transfer(address to, uint256 value) external returns (bool success);
  function transferFrom(address from, address to, uint256 value) external returns (bool success);
}

contract Bank {
  // Contract Address -> (Client Account Name -> Balance)
  mapping(address => mapping(bytes32 => uint256)) public accountBalances;

  // Client Account Name -> Client Address
  mapping(bytes32 => address) public accountAddr;

  function createAccount(bytes32 name) external returns(bool) {
    address clientAddress = msg.sender;
    accountAddr[name] = clientAddress;
    return true;
  }

  function getAccountBalance(bytes32 accountName, address contractAddr) external view returns(uint256) {
    return accountBalances[contractAddr][accountName];
  }


  function deposit(uint256 amount, address contractAddr, bytes32 name) external returns (bool) {
    
    address clientAddress = accountAddr[name];
    require(clientAddress != address(0x0)); // dev: Account does not exist
    
    uint256 allowance = IERC20(contractAddr).allowance(msg.sender, address(this));
    require(amount <= allowance); // dev: Not enough allowance

    bool deposited = IERC20(contractAddr).transferFrom(msg.sender, address(this), amount);
    accountBalances[contractAddr][name] += amount;

    return deposited;

  }

  function withdraw(uint256 amount, address contractAddr, bytes32 name) external returns (bool) {
    address clientAddress = accountAddr[name];
    require(msg.sender == clientAddress); // dev: Account not owned by caller

    uint256 balance = accountBalances[contractAddr][name];
    require(amount <= balance); // dev: Amount more than balance

    accountBalances[contractAddr][name] -= amount;
    bool withdrawn = IERC20(contractAddr).transfer(msg.sender, amount);

    return withdrawn;

  }

  function _transfer(uint256 amount, bytes32 from, bytes32 to, address contractAddr) public returns (bool) {
    
    uint256 balance = accountBalances[contractAddr][from];
    require(amount <= balance); // dev: Amount more than balance

    accountBalances[contractAddr][from] -= amount;
    accountBalances[contractAddr][to] += amount;

    return true;
  }

  function calculateFee(uint256 amount) public pure returns (uint256) {
    return amount - amount * 1/10;
  }

  function transfer(uint256 amount, bytes32 from, bytes32 to, address contractAddr) public returns (bool) {
    
    address senderAddr = accountAddr[from];
    require(senderAddr == msg.sender); // dev: Account does not belong to caller

    address recipientAddr = accountAddr[to];

    if (recipientAddr != msg.sender) {
      amount = calculateFee(amount);
    }

    bool transferred = _transfer(amount, from, to, contractAddr);

    return transferred;
  }

  function multiTransfer(uint256 amount, bytes32 from, bytes32[5] calldata _to, address contractAddr) external returns (bool) {
    for (uint i=0; i<_to.length; i++) {
      bytes32 to = _to[i];
      
      if (to != 0) {
        transfer(amount, from, to, contractAddr);
      }
      
    }

    return true;
  }

}