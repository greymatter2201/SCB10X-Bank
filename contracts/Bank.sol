// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
  function allowance(address owner, address spender) external view returns (uint256 remaining);
  function approve(address spender, uint256 value) external returns (bool success);
  function balanceOf(address owner) external view returns (uint256 balance);
  function decimals() external view returns (uint8 decimalPlaces);
  function decreaseApproval(address spender, uint256 addedValue) external returns (bool success);
  function increaseApproval(address spender, uint256 subtractedValue) external;
  function name() external view returns (string memory tokenName);
  function symbol() external view returns (string memory tokenSymbol);
  function totalSupply() external view returns (uint256 totalTokensIssued);
  function transfer(address to, uint256 value) external returns (bool success);
  function transferFrom(address from, address to, uint256 value) external returns (bool success);
}

contract Bank {
  // Contract Address -> (Client Address -> Balance)
  mapping(address => mapping(address => uint256)) private clientBalance;

  // Client Account Name -> Client Address
  mapping(bytes32 => address) private clientNames;

  address owner;
  modifier onlyOwner
  {
    require(msg.sender == owner);
    _;
  }

  constructor() {
    owner = msg.sender;
  }

  function createAccount(bytes32 name, address clientAddr) external onlyOwner {
    clientNames[name] = clientAddr;
  }

  function deposit(uint256 amount, address contractAddr) external returns (bool) {
    uint256 allowance = IERC20(contractAddr).allowance(msg.sender, address(this));
    require(amount <= allowance, "Not enough allowance!");

    bool deposited = IERC20(contractAddr).transferFrom(msg.sender, address(this), amount);
    clientBalance[contractAddr][msg.sender] += amount;

    return deposited;

  }

  function withdraw(uint256 amount, address contractAddr) external returns (bool) {
    uint256 balance = clientBalance[contractAddr][msg.sender];
    require(amount <= balance, "Not enough balance!");

    clientBalance[contractAddr][msg.sender] -= amount;
    bool withdrawn = IERC20(contractAddr).transferFrom(address(this), msg.sender, amount);

    return withdrawn;

  }

  function _transfer(uint256 amount, address to, address contractAddr) public returns (bool) {
    uint256 balance = clientBalance[contractAddr][msg.sender];
    require(amount <= balance, "Not enough balance!");

    clientBalance[contractAddr][msg.sender] -= amount;
    clientBalance[contractAddr][to] += amount;
  }

  function transfer(uint256 amount, bytes32 name, address contractAddr) external returns (bool) {
    address clientAddr = clientNames[name];
    transfer()

    return;
  }

}