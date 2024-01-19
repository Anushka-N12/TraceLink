# Importing required packages 
from solcx import compile_standard, install_solc   # To compile solidity contract
import json                                        # To save & retreive JSON file
from web3 import Web3                              # To deploy contract & interact with it
from dotenv import load_dotenv                     # To access environment variables
import os                                          # To access environment variables

# Particular version mentioned in contract
install_solc("0.6.0")

with open('TraceLink.sol', 'r') as contract:
    file = contract.read()
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"TraceLink.sol": {"content": file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                    }
                }
            },
        },
        evm_version="0.6.0",
    )

with open('compiled_code.json', 'w') as cfile:
    json.dump(compiled_sol, cfile)

bytecode = compiled_sol['contracts']['TraceLink.sol']['TraceLink']['evm']['bytecode']['object']
ABI = json.loads(
    compiled_sol["contracts"]["TraceLink.sol"]["TraceLink"]["metadata"]
)["output"]["abi"]

# Loading environment variables
load_dotenv('.env')

# Main chain details given by Ganache / any other API provider, and account details
w3 = Web3(Web3.HTTPProvider(os.getenv('HTTPProvider')))
chain_id = int(os.getenv('chain_id'))
my_address = os.getenv('address')
private_key = os.getenv('private_key')  # should start with 0x

TraceLink = w3.eth.contract(abi=ABI, bytecode=bytecode)

# Deploying contract
tx_hash = TraceLink.constructor().transact({
    "from": my_address,
    "gas": 6_000_000,  # Adjust the gas limit as needed
})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt["contractAddress"]
TraceLink = w3.eth.contract(address=contract_address, abi=ABI)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

# Working with deployed contract
trace_link = w3.eth.contract(address=contract_address, abi=ABI)
funcs = trace_link.functions

# Function to be used by other functions for transactions
def txn_steps(txn):
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    txn_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Function to update count & return product details from given product ID
def showDetails(pid, pnum):
    try:
        funcs.updateCount(pid, pnum).transact({'from':w3.eth.accounts[0]})
        return(funcs.showPDetails().call())
    except:
        return 0     # If product not found

# Function to return company 
def showC(section):
    funcs.updateCft(section[0], section[1]).transact({'from':w3.eth.accounts[0]})
    return(funcs.showC().call())

# Function to add product
def addP(company, name, desc, quant, fid, tid, e_id, e, task, loc):
    funcs.StoreProduct(company, name, desc, quant, fid, tid, e_id, e, task, loc).transact({'from':w3.eth.accounts[0]})
    return(funcs.showCP().call()[1])

# Function to store product log
def storePi(pid, fid, tid, e_id, e, task, loc):
    funcs.StoreSCS(pid, fid, tid, e_id, e, task, loc).transact({'from':w3.eth.accounts[0]})

# Test to execute only if this file is executed directly
if __name__ == '__main__':
    print(showDetails(5,3))
    print((funcs.showCP().call()))
    # print(addP(11, 'trial', 'blah', 'idk', 10, 11, 10, 'm002', 'trail dude', 'dxb'))