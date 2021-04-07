// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "@openzeppelin/contracts/math/SafeMath.sol";

contract CollectivePurchase {

    using SafeMath for uint;

    struct Buyer {
        uint funds;
        uint guarantee;
        bool exist;
    }

    uint public valueOfItem;
    uint public collectiveFunds;
    string public item;
    address payable public seller;
    address payable public responsibleForBuy;
    mapping(address => Buyer) public buyers;
    address[] public addresses;
    enum State {Created, Responsible, Locked, Release, Inactive }
    State public state = State.Created;

    modifier checkIfEven() {
        uint value = msg.value / 2;
        require((2 * value) == msg.value, "Value has to be even.");
        _;
    }

    modifier inState(State _state) {
        require(state == _state, "Invalid state.");
        _;
    }

    modifier onlyResponsible() {
        require(msg.sender == responsibleForBuy, "Only responsible can call this.");
        _;
    }

    constructor(string memory _item) payable { 
        seller = payable(msg.sender);
        valueOfItem = msg.value / 2;
        item = _item;
        collectiveFunds = 0;
        require((2 * valueOfItem) == msg.value, "Value has to be even");
    }

    function depositFunds() public 
                inState(State.Created) 
                checkIfEven
                payable
    {
        uint _value = msg.value / 2;
        collectiveFunds = collectiveFunds.add(_value);

        if (collectiveFunds > valueOfItem) {
            uint _rest = collectiveFunds.sub(valueOfItem);
            collectiveFunds = valueOfItem;
            _value = _value.sub(_rest);
            state = State.Responsible;
            payable(msg.sender).transfer(2 * _rest);
        } else if (collectiveFunds == valueOfItem) {
            state = State.Responsible;
        }

        if (buyers[msg.sender].exist) {
            Buyer storage buyer = buyers[msg.sender];
            buyer.funds = buyer.funds.add(_value);
            buyer.guarantee = buyer.guarantee.add(_value);
        } else {
            buyers[msg.sender] = Buyer(_value, _value, true);
            addresses.push(msg.sender);
        }
    }

    function setResponsible(address _responsibleForBuy) public 
            inState(State.Responsible)
    {
        require(buyers[msg.sender].exist, "Only buyers can set responsible.");
	    require(buyers[_responsibleForBuy].exist, "Only buyers can be responsible");
        responsibleForBuy = payable(_responsibleForBuy);
    }

    function confirmPurchase() public
            inState(State.Responsible)
            onlyResponsible
    {
        state = State.Locked;
    }

    function confirmReceived() public 
            inState(State.Locked)
            onlyResponsible
    {
        state = State.Release;

        for (uint i = 0; i < addresses.length; i++) {
            address payable temp = payable(addresses[i]);
            temp.transfer(buyers[temp].guarantee);
        }
    }

    function refundSeller() public 
            inState(State.Release)
    {
        require(seller == msg.sender, "Only seller can call this.");

        state = State.Inactive;

        seller.transfer(3 * valueOfItem);
    }

    function getBuyersAddresses() public view returns (address[] memory) {
        return addresses;
    }
}