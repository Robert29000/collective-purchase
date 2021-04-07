import brownie


def test_set_responsible_state(accounts, purchase):
    purchase.depositFunds({'from': accounts[1], 'value': 200})
    purchase.depositFunds({'from': accounts[2], 'value': 500})
    purchase.depositFunds({'from': accounts[3], 'value': 100})
    purchase.depositFunds({'from': accounts[4], 'value': 1000})
    purchase.depositFunds({'from': accounts[3], 'value': 200})

    purchase.setResponsible(accounts[2], {'from': accounts[1]})
    assert purchase.responsibleForBuy() == accounts[2]
    assert purchase.state() == 1
    assert purchase.collectiveFunds() == purchase.valueOfItem()


def test_set_responsible_incorrect_state(accounts, purchase):
    purchase.depositFunds({'from': accounts[1], 'value': 200})
    purchase.depositFunds({'from': accounts[2], 'value': 500})
    purchase.depositFunds({'from': accounts[3], 'value': 100})
    purchase.depositFunds({'from': accounts[4], 'value': 1000})

    assert purchase.state() == 0

    with brownie.reverts():
        purchase.setResponsible(accounts[2], {'from': accounts[1]})


def test_set_responsible_set_not_buyer(accounts, purchase):
    purchase.depositFunds({'from': accounts[1], 'value': 200})
    purchase.depositFunds({'from': accounts[2], 'value': 500})
    purchase.depositFunds({'from': accounts[3], 'value': 100})
    purchase.depositFunds({'from': accounts[4], 'value': 1000})
    purchase.depositFunds({'from': accounts[3], 'value': 200})

    with brownie.reverts():
        purchase.setResponsible(accounts[6], {'from': accounts[1]})


def test_set_responsible_set_by_not_buyer(accounts, purchase):
    purchase.depositFunds({'from': accounts[1], 'value': 200})
    purchase.depositFunds({'from': accounts[2], 'value': 500})
    purchase.depositFunds({'from': accounts[3], 'value': 100})
    purchase.depositFunds({'from': accounts[4], 'value': 1000})
    purchase.depositFunds({'from': accounts[3], 'value': 200})

    with brownie.reverts():
        purchase.setResponsible(accounts[2], {'from': accounts[9]})


def test_confirm_purchase(accounts, purchase):
    purchase.depositFunds({'from': accounts[1], 'value': 200})
    purchase.depositFunds({'from': accounts[2], 'value': 500})
    purchase.depositFunds({'from': accounts[3], 'value': 100})
    purchase.depositFunds({'from': accounts[4], 'value': 1000})
    purchase.depositFunds({'from': accounts[3], 'value': 200})

    purchase.setResponsible(accounts[2], {'from': accounts[1]})

    purchase.confirmPurchase({'from':accounts[2]})
    assert purchase.state() == 2


def test_confirm_purchase_not_responsible(accounts, purchase):
    purchase.depositFunds({'from': accounts[1], 'value': 200})
    purchase.depositFunds({'from': accounts[2], 'value': 500})
    purchase.depositFunds({'from': accounts[3], 'value': 100})
    purchase.depositFunds({'from': accounts[4], 'value': 1000})
    purchase.depositFunds({'from': accounts[3], 'value': 200})

    purchase.setResponsible(accounts[2], {'from': accounts[1]})

    with brownie.reverts():
        purchase.confirmPurchase({'from':accounts[3]})



    