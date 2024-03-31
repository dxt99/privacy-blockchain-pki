# Privacy-Aware Log-Based Public Key Infrastructure
This is a POC codebase for the author's thesis. This codebase is made to run on Windows, but it can also run perfectly fine on Linux. Simply skip running the Windows pipeline script and do the actions specified inside manually instead.

## Dependencies
- [Python](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/engine/install/)
- [Truffle](https://archive.trufflesuite.com/docs/truffle/how-to/install/)
- [Ganache](https://archive.trufflesuite.com/ganache/)

## Setup
This repo consists of two different services, `smart_contract` containing the ethereum smart contract, and the `certificate_authority` containing the CA service.

##### Smart contract
Simply modify `smart_contract/truffle-config.js` as needed. No modification is required to run and deploy the smart contract. By default, it will deploy to the local Ganache chain. Note that you need to run the Ganache application manually.

##### Certificate authority
Add `certificate_authority/config/account.json` using the given template in `certificate_authority/config/account.json.example`. Modify the address and private key to match the CA account in the Ethereum chain. If you are using the default truffle config with the local Ganache chain, the CA account will be the first account in the chain. 

## Deployment
Simply run `pipeline.ps1` using powershell. This script will check whether some required dependencies exist, run some unit tests, then deploy the smart contract using the configured Truffle settings. The build result will be stored in `smart_contract/build/contracts/`, and the CA smart contract build result will also be sent to `certificate_authority/config/contracts/`, where the ABI and the smart contract address are stored.


To skip unit tests, run `pipeline.ps1 -no-test`.
To skip smart contract deployment, run `pipeline.ps1 -no-deploy`.


**IMPORTANT NOTE** - if you redeploy the smart contract, the existing transaction data will be gone, and the neweest smart contract will be used. Technically, the old smart contract still exists in the chain and can be destroyed, but this improvement is not yet implemented, and is not in priority, as this may only be relevant in development phase.