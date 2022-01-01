// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract MagicNum {
    address public solver;

    constructor() public {}

    function setSolver(address _solver) public {
        solver = _solver;
    }

    /*
    ____________/\\\_______/\\\\\\\\\_____        
     __________/\\\\\_____/\\\///////\\\___       
      ________/\\\/\\\____\///______\//\\\__      
       ______/\\\/\/\\\______________/\\\/___     
        ____/\\\/__\/\\\___________/\\\//_____    
         __/\\\\\\\\\\\\\\\\_____/\\\//________   
          _\///////////\\\//____/\\\/___________  
           ___________\/\\\_____/\\\\\\\\\\\\\\\_ 
            ___________\///_____\///////////////__
  */
}

interface IMagicNum {
    function setSolver(address _solver) external;
}

contract MagicNumAttacker {
    IMagicNum magicNum;
    address solverAddress;

    constructor(address _magicNum) public {
        magicNum = IMagicNum(_magicNum);
    }

    function attack() public {
        bytes
            memory bytecode = hex"600a600c600039600a6000f3602a60005260206000f3";
        bytes32 salt = 0;
        address solver;

        assembly {
            solver := create2(0, add(bytecode, 0x20), mload(bytecode), salt)
        }

        solverAddress = solver;

        magicNum.setSolver(solver);
    }

    function getCodeSize() public view returns (uint256 x) {
        address addr = solverAddress;
        assembly {
            x := extcodesize(addr)
        }
    }
}
