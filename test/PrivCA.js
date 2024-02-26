const PrivCA = artifacts.require("PrivCA");

contract('PrivCA', (accounts) => {
  let privCaInstance;
  const activeTransactionId = 0;
  const revokedTransactionId = 1;
  const ownerAccount = accounts[0];
  const userAccount = accounts[1];

  before(async () => {
    privCaInstance = await PrivCA.deployed();
    await privCaInstance.register.sendTransaction("www.firstone.com", "pubKey01");
    await privCaInstance.register.sendTransaction("www.secondone.com", "revokedPubKey02");
    await privCaInstance.revoke.sendTransaction(1);
  });

  it('should register sucessfully', async () => {
    const result = await privCaInstance.register.call("b", "c");
    assert.equal(result , 2);
  });

  it('should throw on register if sender is not owner', async () => {
    try {
      await privCaInstance.register.call("b", "c", {from: userAccount})
      assert.fail("The transaction should have thrown an error");
    }
    catch (err) {
      assert.include(err.message, "revert", "The error message should contain 'revert'");
    }
  });

  it('should return proper transaction', async() => {
    const tr = await privCaInstance.get.call(activeTransactionId);
    assert.equal(tr.operation, "register");
  });

  it('should revoke existing transaction', async () => {
    const res = await privCaInstance.revoke.call(activeTransactionId);
    assert.equal(res, true);
  });

  it('should not revoke non-existing transaction', async() => {
    const res = await privCaInstance.revoke.call(99);
    assert.equal(res, false);
  });

  it('should throw on revoke if sender is not owner', async () => {
    try {
      await privCaInstance.revoke.call(activeTransactionId, {from: userAccount})
      assert.fail("The transaction should have thrown an error");
    }
    catch (err) {
      assert.include(err.message, "revert", "The error message should contain 'revert'");
    }
  });

  it('should return revoked transactions', async() => {
    const tr = await privCaInstance.get.call(revokedTransactionId);
    assert.equal(tr.operation, "revoked");
  });
});
