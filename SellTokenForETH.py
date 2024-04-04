from web3 import Web3
import json
import config2
import time

class Style():  # Class of different text colours - default is white
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

bsc = "https://pancake-bnb.rpc.blxrbdn.com"
web3 = Web3(Web3.HTTPProvider(bsc))

print(web3.is_connected())

# Pancakeswap router
panRouterContractAddress = '0x10ED43C718714eb63d5aA57B78B54704E256024E'

# Load ABI
def read_abi_from_file(file_path):
    with open(file_path, 'r') as file:
        abi = json.load(file)
    return abi

# def read_abi_from_file(file_path):
#     with open(file_path, 'r') as file:
#         abi = file.read()
#     return abi

abi_file_path = 'abi/panabi.json'  
panabi = read_abi_from_file(abi_file_path)

sender_address = '0x......'  # TokenAddress of holder
spend = web3.to_checksum_address("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")  # WBNB Address

balance = web3.eth.get_balance(sender_address)
print(Style.YELLOW + "BNB Balance:" + Style.RESET, balance)

humanReadable = web3.from_wei(balance, 'ether')
print(Style.YELLOW + "BNB Balance (Human Readable):" + Style.RESET, humanReadable)

contract_id = web3.to_checksum_address("Contract Token Addess")

contract = web3.eth.contract(address=panRouterContractAddress, abi=panabi)

sellAbi_file_path = 'abi/sellabi.json'  
sellAbi = read_abi_from_file(sellAbi_file_path)

sellTokenContract = web3.eth.contract(contract_id, abi=sellAbi)

balance = sellTokenContract.functions.balanceOf(sender_address).call()
symbol = sellTokenContract.functions.symbol().call()
readable = web3.from_wei(balance, 'ether')
print(Style.YELLOW + "Balance:" + Style.RESET, str(readable) + " " + symbol)

tokenValue = web3.to_wei(input(Style.YELLOW + "Enter amount of " + symbol + " you want to sell:" + Style.RESET), 'ether')

tokenValue2 = web3.from_wei(tokenValue, 'ether')
start = time.time()

approve = sellTokenContract.functions.approve(panRouterContractAddress, balance).build_transaction({
    'from': sender_address,
    'gasPrice': web3.to_wei('3', 'gwei'),
    'nonce': web3.eth.get_transaction_count(sender_address),
})

signed_txn = web3.eth.account.sign_transaction(approve, private_key=config2.private2)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(Style.GREEN + "Approved" + Style.RESET)

time.sleep(10)
print(f"Swapping {tokenValue2} {symbol} for BNB")

pancakeswap2_txn = contract.functions.swapExactTokensForETH(
    tokenValue, 0,
    [contract_id, spend],
    sender_address,
    (int(time.time()) + 1000000)
).build_transaction({
    'from': sender_address,
    'gasPrice': web3.to_wei('3', 'gwei'),
    'nonce': web3.eth.get_transaction_count(sender_address),
})

signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=config2.private2)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

print(Style.GREEN + f"Sold {symbol}:" + Style.RESET, "https://bscscan.com/tx/" + web3.to_hex(tx_token))
