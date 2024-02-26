const PrivCA = artifacts.require("PrivCA");

contract('PrivCA', (accounts) => {
  it('should register sucessfully', async () => {
    const privCaInstance = await PrivCA.deployed();
    const result = await privCaInstance.register.call(2, "b", "c");
    
    assert.equal(result , true);
  });

  it('should fail registration with same id', async () => {
    const privCaInstance = await PrivCA.deployed();
    await privCaInstance.register.sendTransaction(2, "b", "c");
    const result = await privCaInstance.register.call(2, "d", "e");
    
    assert.equal(result , false);
  });

  it('should throw if sender is not owner', async () => {
    const privCaInstance = await PrivCA.deployed();
    try {
      await privCaInstance.register.call(2, "b", "c", {from: accounts[1]})
      assert.fail("The transaction should have thrown an error");
    }
    catch (err) {
      assert.include(err.message, "revert", "The error message should contain 'revert'");
    }
  });

  it('should return proper transaction', async() => {
    const privCaInstance = await PrivCA.deployed();
    await privCaInstance.register.sendTransaction(3, "b", "c");
    const tr = await privCaInstance.get.call(3);
    assert.equal(tr.operation, "register");
  })
});
