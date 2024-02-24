// SPDX-License-Identifier: MIT
// Tells the Solidity compiler to compile only from v0.8.13 to v0.9.0
pragma solidity ^0.8.13;

import "./owned.sol";
// This is just a simple example of a coin-like contract.
// It is not ERC20 compatible and cannot be expected to talk to other
// coin/token contracts.

contract PrivCA is Owned {
	Certificate[] private certificates;

	struct Certificate {
        string domain;
        string publicKey;
    }

	constructor() {
		owner = msg.sender;
	}

	function registerCert(string memory domain, string memory publicKey) public onlyOwner returns(uint newId){
		Certificate memory cert = Certificate(domain, publicKey);
		certificates.push(cert);
		newId = certificates.length - 1;
	}

	function getCert(uint id) public view returns(Certificate memory){
		return certificates[id];
	}
}
