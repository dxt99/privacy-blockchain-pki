const PrivCA = artifacts.require("PrivCA");

contract('PrivCA', (accounts) => {
  it('should register sucessfully', async () => {
    const privCaInstance = await PrivCA.deployed();
    const id = await privCaInstance.registerCert.call("b", "c");
    
    assert.equal(id , 0);
  });

  it('should throw if sender is not owner', async () => {
    const privCaInstance = await PrivCA.deployed();
    try {
      await privCaInstance.registerCert.call("b", "c", {from: accounts[1]})
      assert.fail("The transaction should have thrown an error");
    }
    catch (err) {
      assert.include(err.message, "revert", "The error message should contain 'revert'");
    }
  });

  it('should return proper certificate', async() => {
    const privCaInstance = await PrivCA.deployed();
    await privCaInstance.registerCert.sendTransaction("b", "c");
    const cert = await privCaInstance.getCert.call(0);
    assert.equal(cert.domain, "b");
    console.log(cert);
  })
});
