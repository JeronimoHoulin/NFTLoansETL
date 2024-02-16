import os
import json
import pandas as pd
from web3 import Web3
from datetime import datetime
from datetime import timezone
from dotenv import load_dotenv

load_dotenv()

root_dir = os.getenv('root_dir')

if root_dir == '' or root_dir == None:
    root_dir = 'C:/Users/jeron/OneDrive/Desktop/Zash/Scripts/NFT Lending'

# Connect to the Ethereum network using web3.py
infura_key = os.getenv('INFURA_TOKEN')
w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infura_key}'))

# The address of the ParaSpace contract
address = '0x638a98BBB92a7582d07C52ff407D49664DC8b3Ee'


with open(f"{root_dir}/abis/paraspace.json") as f:
    info_json = json.load(f)

abi = info_json

# Create a contract object
contract = w3.eth.contract(address=address, abi=abi)

#start block
from_block = 16976560-1000  #16088000   #contract creation = Dec-01-2022 ?
to_block = 16976560-900  #16579111
current_block = w3.eth.blockNumber #w3.eth.blockNumber


print("getting blocks...")
#Pooling events ERC20
supply_coin1 = contract.events.Supply.getLogs(fromBlock=from_block, toBlock=to_block)
supply_coin2 = contract.events.Supply.getLogs(fromBlock=to_block + 1, toBlock=current_block)

withdraw_coin1 = contract.events.Withdraw.getLogs(fromBlock=from_block, toBlock=to_block)
withdraw_coin2 = contract.events.Withdraw.getLogs(fromBlock=to_block + 1, toBlock=current_block)

liquidate_coin1 = contract.events.LiquidateERC20.getLogs(fromBlock=from_block, toBlock=to_block)
liquidate_coin2 = contract.events.LiquidateERC20.getLogs(fromBlock=to_block + 1, toBlock=current_block)

supply_coin = supply_coin1 + supply_coin2
withdraw_coin = withdraw_coin1 + withdraw_coin2
liquidate_coin = liquidate_coin1 + liquidate_coin2

#Pooling events ERC721
supply_nft1 = contract.events.SupplyERC721.getLogs(fromBlock=from_block, toBlock=to_block)
supply_nft2 = contract.events.SupplyERC721.getLogs(fromBlock=to_block + 1, toBlock=current_block)

withdraw_nft1 = contract.events.WithdrawERC721.getLogs(fromBlock=from_block, toBlock=to_block)
withdraw_nft2 = contract.events.WithdrawERC721.getLogs(fromBlock=to_block + 1, toBlock=current_block)

liquidate_nft1 = contract.events.LiquidateERC721.getLogs(fromBlock=from_block, toBlock=to_block)
liquidate_nft2 = contract.events.LiquidateERC721.getLogs(fromBlock=to_block + 1, toBlock=current_block)

supply_nft = supply_nft1 + supply_nft2
withdraw_nft = withdraw_nft1 + withdraw_nft2
liquidate_nft = liquidate_nft1 + liquidate_nft2


#Loaning events XXX

borrowed1 = contract.events.Borrow.getLogs(fromBlock=from_block, toBlock=to_block)
borrowed2 = contract.events.Borrow.getLogs(fromBlock=to_block + 1, toBlock=current_block)

repay1 = contract.events.Repay.getLogs(fromBlock=from_block, toBlock=to_block)
repay2 = contract.events.Repay.getLogs(fromBlock=to_block + 1, toBlock=current_block)

borrowed = borrowed1 + borrowed2  ##Emitted on borrow() and flashLoan() when debt needs to be opened
repaid = repay1 + repay2





""" Checker for COINS """

def check_coin(payment_token):
    
    if payment_token == '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2':
        paymnt_token = 'WETH'
        decimalz = 1e18
    elif payment_token == '0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0':
        paymnt_token = 'wstETH'
        decimalz = 1e18
    elif payment_token == '0xBe9895146f7AF43049ca1c1AE358B0541Ea49704':
        paymnt_token = 'cbETH'
        decimalz = 1e18 
    elif payment_token == '0xae78736cd615f374d3085123a210448e74fc6393':
        paymnt_token = 'rETH'
        decimalz = 1e18 
    elif payment_token == '0x030ba81f1c18d280636f32af80b9aad02cf0854e':
        paymnt_token = 'aETH'
        decimalz = 1e18
    elif payment_token == '0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84':
        paymnt_token = 'stETH'
        decimalz = 1e18
        
    #APE tokens:
    elif payment_token == '0x4d224452801ACEd8B2F0aebE155379bb5D594381':
        paymnt_token = 'APE'
        decimalz = 1e18
    elif payment_token == '0xC5c9fB6223A989208Df27dCEE33fC59ff5c26fFF':
        paymnt_token = 'cAPE'
        decimalz = 1e18
        
    #BTC:
    elif payment_token == '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599':
        paymnt_token = 'WBTC'
        decimalz = 1e8
        
    #Stablecoins: 
    elif payment_token == '0x6B175474E89094C44Da98b954EedeAC495271d0F':
        paymnt_token = 'DAI'
        decimalz = 1e18
    elif payment_token == '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48':
        paymnt_token = 'USDC'
        decimalz = 1e6
    elif payment_token == '0xdAC17F958D2ee523a2206206994597C13D831ec7':
        paymnt_token = 'USDT'
        decimalz = 1e6
    elif payment_token == '0x853d955aCEf822Db058eb8505911ED77F175b99e':
        paymnt_token = 'FRAX'
        decimalz = 1e18
        
    #Others
    elif payment_token == '0x5283D291DBCF85356A21bA090E6db59121208b44':
        paymnt_token = 'BLUR'
        decimalz = 1e18
    
    else: 
        print(f"this is a new COIN to add: {payment_token}")
        paymnt_token = '-'
        decimalz = 1
        
    return paymnt_token, decimalz


def check_nft(nft_token):

    if nft_token == '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D':
        nft = 'BAYC'
    elif nft_token == '0x60E4d786628Fea6478F785A6d7e704777c86a7c6':
        nft = 'MAYC'
    elif nft_token == '0xba30E5F9Bb24caa003E9f2f0497Ad287FDF95623':
        nft = 'BAKC'
    elif nft_token == '0x764AeebcF425d56800eF2c84F2578689415a2DAa':
        nft = 'SewerPass'
    elif nft_token == '0xBd3531dA5CF5857e7CfAA92426877b022e612cf8':
        nft = 'PudgyPenguins'
    elif nft_token == '0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e':
        nft = 'Doodles'
    elif nft_token == '0xb7F7F6C52F2e2fdb1963Eab30438024864c313F6':
        nft = 'WPUNKS'
    elif nft_token == '0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB':
        nft = 'CryptoPunks'
    elif nft_token == '0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B':
        nft = 'CloneX'
    elif nft_token == '0x34d85c9CDeB23FA97cb08333b511ac86E1C4E258':
        nft = 'Otherdeed'
    elif nft_token == '0xED5AF388653567Af2F388E6224dC7C4b3241C544':
        nft = 'Azuki'
    elif nft_token == '0x7Bd29408f11D2bFC23c34f18275bBf23bB716Bc7':
        nft = 'Meebits'
    elif nft_token == '0x23581767a106ae21c074b2276D25e5C3e136a68b':
        nft = 'Moonbirds'
    elif nft_token == '0xC36442b4a4522E871399CD717aBDD847Ab11FE88':
        nft = 'UniswapV3'
    elif nft_token == '0xE012Baf811CF9c05c408e879C399960D1f305903':
        nft = 'Otherside Koda'
    elif nft_token == '0x5b1085136a811e55b2Bb2CA1eA456bA82126A376':
        nft = 'Otherside Vessle'
    elif nft_token == '0x790B2cF29Ed4F310bf7641f013C65D4560d28371':
        nft = 'Otherdeed Expanded'
    elif nft_token == '0x306b1ea3ecdf94aB739F1910bbda052Ed4A9f949':
        nft = 'Beanz' 
    elif nft_token == '0x8821BeE2ba0dF28761AffF119D66390D594CD280':
        nft = 'DeGods'

    else:
        print(f"this is a new NFT to add: {nft_token}")
        nft = '-'

    return nft
    


## Checking for supplies, then all borrowed with that supply, then all withdrawn... (?)

print("running parsers...")

#Indexing Pooled ERC721's

parsed_supplied_nfts = []
parsed_withdrawed_nfts = []
parsed_liquidated_nfts = []


#paraspace NFT mapper here: https://dune.com/queries/1951928/3221263

for i in supply_nft: 
    _txn = i.args
    
    nft_token = _txn.reserve
    
    nft = check_nft(nft_token)
        
    user = _txn.user

    block_num = i.blockNumber
    start = datetime.fromtimestamp(w3.eth.getBlock(block_num).timestamp, tz=timezone.utc)
    start_stamp = w3.eth.getBlock(block_num).timestamp

    txn_hash = i.transactionHash.hex()
    
    """ In case we want to know exactly what NFTs they added.. lots of work done with this.
    token_ids = []
    for y in _txn.tokenData:
        token_ids.append(y[0])
    """
    tkn_amt = len(_txn.tokenData)
    
    case = {
                'method': 'supply',
                'venue': 'ParaSpace',
                'contractVersion': 'v1',        
                'hash': txn_hash,
                'blockNumber': block_num,
                'timestamp':start_stamp,
                'borrower': user,
                'date': start,
                'asset': nft,
                'amount': tkn_amt
            }

    
    parsed_supplied_nfts.append(case)
    
for i in withdraw_nft:
    _txn = i.args
    

    nft_token = _txn.reserve
    
    nft = check_nft(nft_token)
        
    user = _txn.user

    block_num = i.blockNumber
    start = datetime.fromtimestamp(w3.eth.getBlock(block_num).timestamp, tz=timezone.utc)
    start_stamp = w3.eth.getBlock(block_num).timestamp

    txn_hash = i.transactionHash.hex()
    
    """ In case we want to know exactly what NFTs they added.. lots of work done with this.
    token_ids = []
    for y in _txn.tokenData:
        token_ids.append(y[0])
    """

    tkn_amt = len(_txn.tokenIds)
    
    case = {
                'method': 'withdraw',
                'venue': 'ParaSpace',
                'contractVersion': 'v1',        
                'hash': txn_hash,
                'blockNumber': block_num,
                'timestamp':start_stamp,
                'borrower': user,
                'date': start,
                'asset': nft,
                'amount': tkn_amt
            }

    parsed_withdrawed_nfts.append(case)

#Notes here: https://dune.com/queries/2143378/3515219 
for i in liquidate_nft:
    _txn = i.args
    
    liquidated_user = _txn.borrower
    
    collateral_nft = _txn.collateralAsset
    borrowed_asset = _txn.liquidationAsset #Confusing names..
    
    borrowed_token = borrowed_asset
    
    paymnt_token, decimalz = check_coin(borrowed_asset)
        
    borrowed_amount = _txn.liquidationAmount/decimalz
    
    nft_token = collateral_nft
    
    nft = check_nft(nft_token)
    
    amount = 1

    block_num = i.blockNumber
    start = datetime.fromtimestamp(w3.eth.getBlock(block_num).timestamp, tz=timezone.utc)
    start_stamp = w3.eth.getBlock(block_num).timestamp

    txn_hash = i.transactionHash.hex()
        
    
    case = {
            'method': 'liquidated_nft',
            'venue': 'ParaSpace',
            'contractVersion': 'v1',        
            'hash': txn_hash,
            'blockNumber': block_num,
            'timestamp':start_stamp,
            'borrower': liquidated_user,
            'liquidatedDate': start,
            'borrowedAsset': paymnt_token,
            'borrowedAmount': borrowed_amount,
            'liquidatedAsset': nft,
            'liquidatedAmount': amount
    }

    parsed_liquidated_nfts.append(case)
    
    


    
#Indexing Pooled ERC20's

parsed_supplied_coins = []
parsed_withdrawed_coins = []
parsed_liquidated_coins = []

for i in supply_coin:
    _txn = i.args
    
    supplied_coin = _txn.reserve
    user = _txn.user

    block_num = i.blockNumber
    start = datetime.fromtimestamp(w3.eth.getBlock(block_num).timestamp, tz=timezone.utc)
    start_stamp = w3.eth.getBlock(block_num).timestamp

    txn_hash = i.transactionHash.hex()
    
    payment_token = supplied_coin
    
    paymnt_token, decimalz = check_coin(borrowed_asset)
    
    amount = _txn.amount / decimalz
    
    
    case = {
                'method': 'supply',
                'venue': 'ParaSpace',
                'contractVersion': 'v1',        
                'hash': txn_hash,
                'blockNumber': block_num,
                'timestamp':start_stamp,
                'lender': user,
                'date': start,
                'asset': paymnt_token,
                'amount': amount
    }


    parsed_supplied_coins.append(case)
    
    
    
     
for i in withdraw_coin:
    _txn = i.args
    
    withdrawn_coin = _txn.reserve
    user = _txn.user

    block_num = i.blockNumber
    start = datetime.fromtimestamp(w3.eth.getBlock(block_num).timestamp, tz=timezone.utc)
    start_stamp = w3.eth.getBlock(block_num).timestamp

    txn_hash = i.transactionHash.hex()
    
    payment_token = withdrawn_coin
    
    paymnt_token, decimalz = check_coin(borrowed_asset)
    
    amount = _txn.amount / decimalz
    
    case = {
                'method': 'withdraw',
                'venue': 'ParaSpace',
                'contractVersion': 'v1',        
                'hash': txn_hash,
                'blockNumber': block_num,
                'timestamp':start_stamp,
                'lender': user,
                'date': start,
                'asset': paymnt_token,
                'amount': amount
    }

    parsed_withdrawed_coins.append(case)
    
    
    
#Notes here: https://dune.com/queries/2143378/3515219 
for i in liquidate_coin: 
    _txn = i.args
    
    liquidated_user = _txn.borrower
    borrowed_asset = _txn.liquidationAsset #Confusing names..
        
    borrwed_tkn, decimalz = check_coin(borrowed_asset)
    borrowed_amount = _txn.liquidationAmount/decimalz
    
    payment_token = _txn.collateralAsset

    paymnt_token, decimalz = check_coin(payment_token)
    
    amount = _txn.liquidatedCollateralAmount / decimalz

    block_num = i.blockNumber
    start = datetime.fromtimestamp(w3.eth.getBlock(block_num).timestamp, tz=timezone.utc)
    start_stamp = w3.eth.getBlock(block_num).timestamp

    txn_hash = i.transactionHash.hex()
        
    
    case = {
            'method': 'liquidate_coin',
            'venue': 'ParaSpace',
            'contractVersion': 'v1',        
            'hash': txn_hash,
            'blockNumber': block_num,
            'timestamp':start_stamp,
            'borrower': liquidated_user,
            'liquidatedDate': start,
            'borrowedAsset': borrwed_tkn,
            'borrowedAmount': borrowed_amount,
            'liquidatedAsset': paymnt_token,
            'liquidatedAmount': amount
    }

    parsed_liquidated_coins.append(case)
    
    
    
#Indexing Loaned tokens

parsed_borrowed = []
parsed_repaid = []

for i in borrowed:
    _txn = i.args
    
    payment_token = _txn.reserve
    
    paymnt_token, decimalz = check_coin(payment_token)

    
    interest = _txn.borrowRate/(10**27)
    principal = _txn.amount/decimalz
    
    max_repayment = principal *(1+interest/100)
    user = _txn.user
    
    block_num = i.blockNumber
    start = datetime.fromtimestamp(w3.eth.getBlock(block_num).timestamp, tz=timezone.utc)
    start_stamp = w3.eth.getBlock(block_num).timestamp

    txn_hash = i.transactionHash.hex()
   

    case = {
                'method': 'borrowed',
                'venue': 'ParaSpace',
                'contractVersion': 'v1',        
                'hash': txn_hash,
                'blockNumber': block_num,
                'timestamp':start_stamp,
                'borrower': user,
                'asset': paymnt_token,
                'principal': principal,
                'maxRepayment': max_repayment,
                'directRate': interest,
                'loanStart': start,
    }

    parsed_borrowed.append(case)

for i in repaid:
    _txn = i.args
    
    payment_token = _txn.reserve
    
    paymnt_token, decimalz = check_coin(payment_token)

    block_num = i.blockNumber
    start = datetime.fromtimestamp(w3.eth.getBlock(block_num).timestamp, tz=timezone.utc)
    start_stamp = w3.eth.getBlock(block_num).timestamp

    max_repayment = _txn.amount/decimalz 
    user = _txn.user

    
    block_number = i.blockNumber

    txn_hash = i.transactionHash.hex()

        
    payment_datetime = datetime.fromtimestamp(w3.eth.getBlock(block_num).timestamp, tz=timezone.utc)
    
    case = {
                'method': 'repaid',
                'venue': 'ParaSpace',
                'contractVersion': 'v1',
                'hash': txn_hash,
                'blockNumber': block_num,
                'timestamp':start_stamp,
                'borrower': user,
                'asset': paymnt_token,
                'repayment': max_repayment,
                'repaidDate': payment_datetime
    }

    parsed_repaid.append(case)




#concating everything to get her

# Pooled assets

df_supplied_coins = pd.DataFrame(parsed_supplied_coins)
df_supplied_nfts = pd.DataFrame(parsed_supplied_nfts)

df_withdrawn_coins = pd.DataFrame(parsed_withdrawed_coins)
df_withdrawn_nfts = pd.DataFrame(parsed_withdrawed_nfts)


df_lenders = pd.concat([df_supplied_coins, df_supplied_nfts, df_withdrawn_coins, df_withdrawn_nfts])




# Loaned Assets
df_borrowed = pd.DataFrame(parsed_borrowed)
df_repaid = pd.DataFrame(parsed_repaid)

df_liquidated_coins = pd.DataFrame(parsed_liquidated_coins)
df_liquidated_nfts = pd.DataFrame(parsed_liquidated_nfts)


df_borrowers = pd.concat([df_borrowed, df_repaid, df_liquidated_coins, df_liquidated_nfts])

os.chdir(f"{root_dir}/tests/p2pool")

print("saving...")

df_paraspace = pd.concat([df_borrowers, df_lenders])

df_paraspace.to_csv('ParaSpace_loans_Test.csv')


""" Checks:
df_spec_1 = df_borrowed[df_borrowed['user'] == '0xf3aFc2383a0B45ae73D77B49dF7F2184B1Ad4B90']

df_spec_2 = df_repaid[df_repaid['user'] == '0xf3aFc2383a0B45ae73D77B49dF7F2184B1Ad4B90']

"""
