import brownie


def test_confirm_received(accounts, purchase):
    balance_seller = accounts[0].balance()
    balance1 = accounts[1].balance()
    balance2 = accounts[2].balance()
    balance3 = accounts[3].balance()
    balance4 = accounts[4].balance()
    purchase.depositFunds({'from': accounts[1], 'value': 200})
    purchase.depositFunds({'from': accounts[2], 'value': 500})
    purchase.depositFunds({'from': accounts[3], 'value': 100})
    purchase.depositFunds({'from': accounts[4], 'value': 1000})
    purchase.depositFunds({'from': accounts[3], 'value': 200})

    purchase.setResponsible(accounts[2], {'from': accounts[1]})
    purchase.confirmPurchase({'from':accounts[2]})
    purchase.confirmReceived({'from':accounts[2]})

    assert purchase.state() == 3
    assert balance1 - accounts[1].balance() == 100
    assert balance2 - accounts[2].balance() == 250
    assert balance3 - accounts[3].balance() == 150
    assert balance4 - accounts[4].balance() == 500
    assert balance_seller - accounts[0].balance() == 0
    assert purchase.balance() == 3000


def test_confirm_received_not_responsible(accounts, purchase):
    purchase.depositFunds({'from': accounts[1], 'value': 200})
    purchase.depositFunds({'from': accounts[2], 'value': 500})
    purchase.depositFunds({'from': accounts[3], 'value': 100})
    purchase.depositFunds({'from': accounts[4], 'value': 1000})
    purchase.depositFunds({'from': accounts[3], 'value': 200})

    purchase.setResponsible(accounts[2], {'from': accounts[1]})
    purchase.confirmPurchase({'from':accounts[2]})
    with brownie.reverts():
        purchase.confirmReceived({'from':accounts[4]})