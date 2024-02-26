// SPDX-License-Identifier: MIT
// Tells the Solidity compiler to compile only from v0.8.13 to v0.9.0
pragma solidity ^0.8.13;

import "./owned.sol";
// This is just a simple example of a coin-like contract.
// It is not ERC20 compatible and cannot be expected to talk to other
// coin/token contracts.

contract PrivCA is Owned {
	mapping (uint => Transaction) private transactions;
	mapping (uint => bool) private revocations;

	struct Transaction {
		string operation;
		string identity;
        string publicKey;
    }

	constructor() {
		owner = msg.sender;
	}

	function register(uint id, string memory domain, string memory publicKey) public onlyOwner returns(bool){
		if (bytes(transactions[id].operation).length != 0) return false;
		
		Transaction memory tr = Transaction("register", domain, publicKey);
		transactions[id] = tr;

		return true;
	}

	function get(uint id) public view returns(Transaction memory){
		return transactions[id];
	}
}
