from solcx import compile_standard, install_solc
import json
from web3 import Web3
from dotenv import load_dotenv
import os

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

load_dotenv('.env')
# If there's a prob, add export before each declaration
w3 = Web3(Web3.HTTPProvider(os.getenv('HTTPProvider')))
chain_id = int(os.getenv('chain_id'))
my_address = os.getenv('address')
private_key = os.getenv('private_key')  # should start with 0x

TraceLink = w3.eth.contract(abi=ABI, bytecode=bytecode)

# Deploy the contract
tx_hash = TraceLink.constructor().transact({
    "from": my_address,
    "gas": 6_000_000,  # Adjust the gas limit as needed
})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt["contractAddress"]
TraceLink = w3.eth.contract(address=contract_address, abi=ABI)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

# Working with deployed Contracts
trace_link = w3.eth.contract(address=contract_address, abi=ABI)
funcs = trace_link.functions

def txn_steps(txn):
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    txn_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Uncomment and modify the following function call as needed
def showDetails(pid, pnum):
    funcs.updateCount(pid, pnum).transact({'from':w3.eth.accounts[0]})
    #build_transaction({
        # "chainId": chain_id,
        # "gasPrice": 5_000_000_000, #w3.eth.gas_price*50,
    #     "from": my_address,
    #     "nonce": w3.eth.get_transaction_count(my_address) + 1,
    # })
    # txn_steps(txn)
    # print('Count updated!')
    return(funcs.showPDetails().call())

def showC(section):
    funcs.updateCft(section[0], section[1]).transact({'from':w3.eth.accounts[0]})
    return(funcs.showC().call())

#Uncomment and modify the following function call as needed
# showDetails('1x3')
# showDetails('1x3')
# def sendData():
    # return(funcs.showPDetails().call())