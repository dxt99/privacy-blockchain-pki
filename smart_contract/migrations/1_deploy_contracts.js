const PrivCA = artifacts.require("PrivCA");
const owned = artifacts.require("owned");

module.exports = function(deployer) {
  deployer.deploy(owned);
  deployer.link(owned, PrivCA);
  deployer.deploy(PrivCA);
};
