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
#If there's a prob, add export before each declaration
w3 = Web3(Web3.HTTPProvider(os.getenv('HTTPProvider')))
chain_id = int(os.getenv('chain_id'))
my_address = os.getenv('address')
private_key = os.getenv('private_key')    #should start with 0x

TraceLink = w3.eth.contract(abi=ABI, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(my_address)

txn = TraceLink.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
signed_txn = w3.eth.account.sign_transaction(txn, private_key)
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

# Working with deployed Contracts
trace_link = w3.eth.contract(address=my_address, abi=ABI)
funcs = trace_link.functions

def txn_steps(txn):
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    txn_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# def showDetails(num):
#     pid, pnum = num.split('x')
#     pid, pnum = int(pid), int(pnum)
#     txn = funcs.updateCount(pid, pnum).build_transaction({
#         "chainId": chain_id,
#         "gasPrice": w3.eth.gas_price,
#         "from": my_address,
#         "nonce": nonce + 1,
#     })
#     txn_steps(txn)
#     print('Count updated!')
#     print(funcs.showPDetails(pid).call())
# showDetails('1x3')
print(funcs.showPDetails().call())

