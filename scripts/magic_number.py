from brownie import accounts, MagicNum, MagicNumAttacker

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0x328C1e8187172D7672688CAc97ea65ca695ad662"
magic_num = MagicNum.at(instance_address)

# ---------------------------------------------------------------
# to pass this level our hacker contracts need to contain at most
# 10 opcodes
# ---------------------------------------------------------------


def level_completed():
    return hacker.getCodeSize() == 10


def exploit():
    # deploy hacker contract
    hacker = MagicNumAttacker.deploy(instance_address, {"from": account})

    # check the solver
    print(f"Solver is equal to: {magic_num.solver()}")

    # call attack function in hacker contract
    tx = hacker.attack({"from": account})
    tx.wait(1)

    # check the solver
    print(f"Solver is equal to: {magic_num.solver()}")

    # confirm we have completed the level
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
