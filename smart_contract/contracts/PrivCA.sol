// SPDX-License-Identifier: MIT
// Tells the Solidity compiler to compile only from v0.8.13 to v0.9.0
pragma solidity ^0.8.13;

import "./owned.sol";
// This is just a simple example of a coin-like contract.
// It is not ERC20 compatible and cannot be expected to talk to other
// coin/token contracts.

contract PrivCA is Owned {
	Transaction[] private transactions;
	mapping (uint => bool) private revocations;

	struct Transaction {
		string operation;
		string identity;
        string publicKey;
		string signatures;
    }

	constructor() {
		owner = msg.sender;
	}

	// CA validates identity and verifies registration, then calls register
	function register(string memory domain, string memory publicKey, string memory signatures) public onlyOwner returns(uint){
		Transaction memory tr = Transaction("register", domain, publicKey, signatures);
		transactions.push(tr);

		return transactions.length - 1;
	}

	// Anyone can post updates, this will be used in certificate verification
	function update(string memory publicKey, string memory signatures) public returns(uint){
		// add more pushed info later
		Transaction memory tr = Transaction("update", "", publicKey, signatures);
		transactions.push(tr);

		return transactions.length - 1;
	}

	// CA can revoke certain transactions, users can request CA to revoke
	function revoke(uint id) public onlyOwner returns(bool){
		if (id >= transactions.length) return false;
		revocations[id] = true;
		return true;
	} 

	function get(uint id) public view returns(Transaction memory){
		if (revocations[id]) return Transaction("revoked", "", "", "");
		return transactions[id];
	}
}
