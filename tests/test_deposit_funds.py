import brownie

def test_deposit_funds_even(accounts, purchase):
    balance = accounts[1].balance()
    purchase.depositFunds({'from': accounts[1], 'value': 200})

    buyer = purchase.buyers(accounts[1])
    assert buyer[0] == 100
    assert buyer[1] == 100
    assert buyer[2] == True
    assert balance - accounts[1].balance() == 200


def test_deposit_funds_contract(accounts, purchase):
    purchase.depositFunds({'from': accounts[1], 'value': 200})

    assert purchase.collectiveFunds() == 100
    assert purchase.balance() == 2200


def test_deposit_funds_not_even(accounts, purchase):
    with brownie.reverts():
        purchase.depositFunds({'from': accounts[1], 'value': 201})


def test_deposit_funds_multiple(accounts, purchase):
    purchase.depositFunds({'from': accounts[1], 'value': 200})
    purchase.depositFunds({'from': accounts[2], 'value': 500})
    purchase.depositFunds({'from': accounts[3], 'value': 50})
    purchase.depositFunds({'from': accounts[4], 'value': 100})

    assert purchase.collectiveFunds() == 425
    addrs = purchase.getBuyersAddresses()
    assert len(addrs) == 4
    assert purchase.balance() == 2850


def test_deposit_funds_again(accounts, purchase):
    purchase.depositFunds({'from': accounts[1], 'value': 200})
    purchase.depositFunds({'from': accounts[2], 'value': 500})
    purchase.depositFunds({'from': accounts[3], 'value': 50})

    assert purchase.collectiveFunds() == 375
    addrs = purchase.getBuyersAddresses()
    assert len(addrs) == 3

    purchase.depositFunds({'from': accounts[1], 'value': 500})

    assert purchase.collectiveFunds() == 625
    addrs = purchase.getBuyersAddresses()
    assert len(addrs) == 3
    assert purchase.balance() == 3250

    buyer = purchase.buyers(accounts[1])
    assert buyer[0] == 350
    assert buyer[1] == 350
    assert buyer[2] == True


def test_deposit_funds_equal(accounts, purchase):
    purchase.depositFunds({'from': accounts[1], 'value': 200})
    purchase.depositFunds({'from': accounts[2], 'value': 500})
    purchase.depositFunds({'from': accounts[3], 'value': 100})
    purchase.depositFunds({'from': accounts[4], 'value': 1000})
    
    assert purchase.valueOfItem() == 1000
    assert purchase.collectiveFunds() == 900
    assert purchase.balance() == 3800
    assert purchase.state() == 0

    purchase.depositFunds({'from': accounts[3], 'value': 200})

    assert purchase.valueOfItem() == 1000
    assert purchase.collectiveFunds() == 1000
    assert purchase.balance() == 4000
    assert purchase.state() == 1


def test_deposit_funds_overflow(accounts, purchase):
    purchase.depositFunds({'from': accounts[1], 'value': 200})
    purchase.depositFunds({'from': accounts[2], 'value': 500})
    purchase.depositFunds({'from': accounts[3], 'value': 100})
    purchase.depositFunds({'from': accounts[4], 'value': 1000})

    assert purchase.valueOfItem() == 1000
    assert purchase.collectiveFunds() == 900
    assert purchase.balance() == 3800
    assert purchase.state() == 0

    balance = accounts[5].balance()
    purchase.depositFunds({'from': accounts[5], 'value': 300})

    assert purchase.valueOfItem() == 1000
    assert purchase.collectiveFunds() == 1000
    assert purchase.balance() == 4000
    assert purchase.state() == 1

    buyer = purchase.buyers(accounts[5])
    assert balance - accounts[5].balance() == 200
    assert buyer[0] == 100
    assert buyer[1] == 100
    assert buyer[2] == True

