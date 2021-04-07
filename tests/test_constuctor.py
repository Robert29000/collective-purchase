import brownie


def test_constructor_even(accounts, CollectivePurchase):
    seller = accounts[0]
    purchase = CollectivePurchase.deploy("Skate", {'from': seller, 'value': 200})
    
    assert purchase.seller() == accounts[0]
    assert purchase.state() == 0
    assert purchase.valueOfItem() == 100
    assert purchase.collectiveFunds() == 0
    assert purchase.balance() == 200



def test_constructor_not_even(accounts, CollectivePurchase):
    seller = accounts[0]
    with brownie.reverts():
        purchase = CollectivePurchase.deploy("Skate", {'from': seller, 'value': 201})
    




    
