const PrivCA = artifacts.require("PrivCA");

contract('PrivCA', (accounts) => {
  let privCaInstance;
  const activeTransactionId = 1;
  const revokedTransactionId = 0;
  const ownerAccount = accounts[0];
  const userAccount = accounts[1];

  before(async () => {
    privCaInstance = await PrivCA.deployed();
    await privCaInstance.register.sendTransaction("www.firstone.com", "pubKey01", "23df9923424");
    await privCaInstance.register.sendTransaction("www.secondone.com", "revokedPubKey02", "9acbd2039092");
    await privCaInstance.revoke.sendTransaction(revokedTransactionId);
  });

  it('should register sucessfully', async () => {
    const result = await privCaInstance.register.call("b", "c", "abcdef", {from: ownerAccount});
    assert.equal(result , 2);
  });

  it('should throw on register if sender is not owner', async () => {
    try {
      await privCaInstance.register.call("b", "c", "abcdef", {from: userAccount})
      assert.fail("The transaction should have thrown an error");
    }
    catch (err) {
      assert.include(err.message, "revert", "The error message should contain 'revert'");
    }
  });

  it('should return proper transaction', async() => {
    const tr = await privCaInstance.get.call(activeTransactionId);
    assert.equal(tr.identity, "www.secondone.com");
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
    const tr = await privCaInstance.isRevoked.call(revokedTransactionId);
    assert.equal(tr, true);
  });

  it('should return non-revoked transactions', async() => {
    const tr = await privCaInstance.isRevoked.call(98);
    assert.equal(tr, false);
  });
});
