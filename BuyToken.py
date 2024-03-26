"BUY A SPECIFIC TOKEN ON PancakeSwap"

"NOTE this script doesn't work for certain tokensupporting transfer fees I have to manually calculate the amount out token "

print("Loading...")

from web3 import Web3
import json
import time
import sys
import config2




# allows different colour text to be used


class style():  # Class of different text colours - default is white
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




# -------------------------------- INITIALISE ------------------------------------------

#web3 = Web3(Web3.HTTPProvider("https://pancake-bnb.rpc.blxrbdn.com")) #BSC
web3 = Web3(Web3.HTTPProvider("https://rpc.ankr.com/base/")) #BASE

if web3.is_connected():
    #print(style.YELLOW + " BSC Node successfully connected")
    print(style.YELLOW + " Base Node successfully connected")
balance = web3.eth.get_balance(config2.WalletAddress) # here balance is in wei
b =web3.from_wei(balance,"ether")

# pancakeswap factory
#pancake_factory = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73'  #Testnet  #0x6725F303b657a9451d8BA641348b6761A6CC7a17
#Feel free to get official ABI from pancake trust none:
#pancake_factory_abi = load_abi_from_file("pancake_factory_abi.json")
# contract = web3.eth.contract(address=pancake_factory, abi=pancake_factory_abi)

"""Connection to Pancakeswap"""


#pancakeSwapRouterAddress = '0x10ED43C718714eb63d5aA57B78B54704E256024E' # BSC
#pancake_abi = load_abi_from_file("pancake_abi.json")

pancakeSwapRouterAddress = '0x8cFe327CEc66d1C090Dd72bd0FF11d690C33a2Eb' # BASE
pancake_abi = load_abi_from_file("abi/pancake_base_router.abi.json")

#listeningABI = load_abi_from_file("listening_abi.json")
tokenNameABI = load_abi_from_file("tokenNameABI.json")


def load_abi_from_file(file_path):
    with open(file_path, "r") as file:
        abi = json.load(file)
    return abi


def updateTitle():
    walletBalance = web3.from_wei(web3.eth.get_balance(config2.WalletAddress), 'ether')  # There are references to ether in the code but it's set to BNB, its just how Web3 was originally designed
    walletBalance = round(walletBalance, -(int("{:e}".format(walletBalance).split('e')[1]) - 4))  # the number '4' is the wallet balance significant figures + 1, so shows 5 sig figs
    ## ctypes.windll.kernel32.SetConsoleTitleW("BSCTokenSniper | Tokens Detected: " + str(numTokensDetected) + " | Tokens Bought: " + str(numTokensBought) + " | Wallet Balance: " + str(walletBalance) + " BNB")
    #sys.stdout.write(  "FishingONCHAIN  | Wallet Balance: " + str(walletBalance) + " BNB")
    sys.stdout.write(  "FishingONCHAIN  | Wallet Balance: " + str(walletBalance) + " ETH")
    sys.stdout.flush()

updateTitle()
pancakeABI = load_abi_from_file("abi/pancake_base_router.abi.json")
listeningABI = load_abi_from_file("listening_abi.json")
tokenNameABI = load_abi_from_file("tokenNameABI.json")

#snipeBNBAmount = (input("\nEnter Amount in BNB you want to spend: "))
snipeETHAmount = (input("\nEnter Amount in BNB you want to spend: "))

def Buy():
    tokenAddress = input("\nEnter the token address you want to buy: ") #INPUT Token Address when run script.
    tokenAddress = web3.to_checksum_address(tokenAddress)
    contract = web3.eth.contract(address=pancakeSwapRouterAddress, abi=pancakeABI)

    getTokenName = web3.eth.contract(address=tokenAddress, abi=tokenNameABI)
    tokenSymbol = getTokenName.functions.symbol().call()
    print("\nTrying to buy... ", tokenSymbol)

    tokenToBuy = web3.to_checksum_address(tokenAddress)
    #usdt_mainet = "0x55d398326f99059fF775485246999027B3197955" #BSC
    #bnb_mainet = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c" #BSC
    #usdc_base = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913" 
    weth_base = "0x4200000000000000000000000000000000000006"
    #spend = web3.to_checksum_address(bnb_mainet)  # wbnb contract address
    spend = web3.to_checksum_address(weth_base)  # weth contract address

    nonce = web3.eth.get_transaction_count(config2.WalletAddress)

    # Calculate the expected amount of tokens to receive
    #bnb_amount = web3.to_wei(snipeBNBAmount, 'ether')
    eth_amount = web3.to_wei(snipeETHAmount, 'ether')
    path = [spend, tokenToBuy]
    amounts_out = contract.functions.getAmountsOut(eth_amount, path).call()
    amount_out_min = amounts_out[-1]  # The last element in the amounts_out list is the expected token amount

    # Apply a slippage tolerance (e.g., 1%)
    slippage_tolerance = 0.1  # %Slipage
    amount_out_min = int(amount_out_min * (1 - slippage_tolerance))

    pancakeswap2_txn = contract.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
        amount_out_min,
        path,
        config2.WalletAddress,
        (int(time.time()) + 10000)
    ).build_transaction({
        'from': config2.WalletAddress,
        'value': eth_amount, #bnb_amount
        'gas': 200000,  # Modify gas here
        'gasPrice': web3.to_wei('1', 'gwei'),
        'nonce': nonce,
    })

    # Sign transaction with private key here
    try:
        signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=config2.private2) #Load private from config2.py
        print(style.GREEN + "Transaction Sent")
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)  # BUY THE TOKEN
        txHash = web3.to_hex(tx_token)

        print(
            #style.GREEN + " Successfully Bought " + tokenSymbol + " for " + style.GREEN + " BNB - TX ID: ",
            style.GREEN + " Successfully Bought " + tokenSymbol + " for " + style.GREEN + " ETH - TX ID: ",
            'https://basescan.org/tx/' + txHash) #https://basescan.org/tx/ https://www.bscscan.com/tx/
    except Exception as e:
        print(style.RED + " Transaction failed. Error:", str(e))

if __name__ == '__main__':
    Buy()
