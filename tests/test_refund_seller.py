import brownie


def test_refund_seller(accounts, purchase):
    balance_seller = accounts[0].balance()
    purchase.depositFunds({'from': accounts[1], 'value': 200})
    purchase.depositFunds({'from': accounts[2], 'value': 500})
    purchase.depositFunds({'from': accounts[3], 'value': 100})
    purchase.depositFunds({'from': accounts[4], 'value': 1000})
    purchase.depositFunds({'from': accounts[3], 'value': 200})

    purchase.setResponsible(accounts[2], {'from': accounts[1]})
    purchase.confirmPurchase({'from':accounts[2]})
    purchase.confirmReceived({'from':accounts[2]})
    purchase.refundSeller({'from':accounts[0]})

    assert accounts[0].balance() - balance_seller == 3000
    assert purchase.balance() == 0
    assert purchase.state() == 4


def test_refund_seller_not_seller(accounts, purchase):
    balance_seller = accounts[0].balance()
    purchase.depositFunds({'from': accounts[1], 'value': 200})
    purchase.depositFunds({'from': accounts[2], 'value': 500})
    purchase.depositFunds({'from': accounts[3], 'value': 100})
    purchase.depositFunds({'from': accounts[4], 'value': 1000})
    purchase.depositFunds({'from': accounts[3], 'value': 200})

    purchase.setResponsible(accounts[2], {'from': accounts[1]})
    purchase.confirmPurchase({'from':accounts[2]})
    purchase.confirmReceived({'from':accounts[2]})
    with brownie.reverts():
        purchase.refundSeller({'from':accounts[6]})
    
    assert balance_seller - accounts[0].balance() == 0