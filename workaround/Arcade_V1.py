import os
import json
from web3 import Web3
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timezone


load_dotenv()

root_dir = os.getenv('root_dir')
if root_dir == '' or root_dir == None:
    root_dir = os.getcwd()

# Connect to the Ethereum network using web3.py
infura_key = '7e452892f2204d6a90e814c4a03a7b1d'
w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infura_key}'))

# The address of the Arcade V1 contract
address = '0x59e57F9A313A2EB1c7357eCc331Ddca14209F403' 

"""
with open(f"{root_dir}/abis/arcade_v2.json") as f:
    info_json = json.load(f)

abi = info_json
"""
abi = '[{"inputs":[{"internalType":"contract IERC721","name":"_collateralToken","type":"address"},{"internalType":"contract IFeeController","name":"_feeController","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"FeesClaimed","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"collateralToken","type":"address"},{"indexed":false,"internalType":"address","name":"borrowerNote","type":"address"},{"indexed":false,"internalType":"address","name":"lenderNote","type":"address"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"loanId","type":"uint256"}],"name":"LoanClaimed","type":"event"},{"anonymous":false,"inputs":[{"components":[{"internalType":"uint256","name":"durationSecs","type":"uint256"},{"internalType":"uint256","name":"principal","type":"uint256"},{"internalType":"uint256","name":"interest","type":"uint256"},{"internalType":"uint256","name":"collateralTokenId","type":"uint256"},{"internalType":"address","name":"payableCurrency","type":"address"}],"indexed":false,"internalType":"struct LoanLibrary.LoanTerms","name":"terms","type":"tuple"},{"indexed":false,"internalType":"uint256","name":"loanId","type":"uint256"}],"name":"LoanCreated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"loanId","type":"uint256"}],"name":"LoanRepaid","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"loanId","type":"uint256"},{"indexed":false,"internalType":"address","name":"lender","type":"address"},{"indexed":false,"internalType":"address","name":"borrower","type":"address"}],"name":"LoanStarted","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"FEE_CLAIMER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ORIGINATOR_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REPAYER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"borrowerNote","outputs":[{"internalType":"contract IPromissoryNote","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"loanId","type":"uint256"}],"name":"claim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"token","type":"address"}],"name":"claimFees","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"collateralToken","outputs":[{"internalType":"contract IERC721","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"durationSecs","type":"uint256"},{"internalType":"uint256","name":"principal","type":"uint256"},{"internalType":"uint256","name":"interest","type":"uint256"},{"internalType":"uint256","name":"collateralTokenId","type":"uint256"},{"internalType":"address","name":"payableCurrency","type":"address"}],"internalType":"struct LoanLibrary.LoanTerms","name":"terms","type":"tuple"}],"name":"createLoan","outputs":[{"internalType":"uint256","name":"loanId","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"feeController","outputs":[{"internalType":"contract IFeeController","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"loanId","type":"uint256"}],"name":"getLoan","outputs":[{"components":[{"internalType":"uint256","name":"borrowerNoteId","type":"uint256"},{"internalType":"uint256","name":"lenderNoteId","type":"uint256"},{"components":[{"internalType":"uint256","name":"durationSecs","type":"uint256"},{"internalType":"uint256","name":"principal","type":"uint256"},{"internalType":"uint256","name":"interest","type":"uint256"},{"internalType":"uint256","name":"collateralTokenId","type":"uint256"},{"internalType":"address","name":"payableCurrency","type":"address"}],"internalType":"struct LoanLibrary.LoanTerms","name":"terms","type":"tuple"},{"internalType":"enum LoanLibrary.LoanState","name":"state","type":"uint8"},{"internalType":"uint256","name":"dueDate","type":"uint256"}],"internalType":"struct LoanLibrary.LoanData","name":"loanData","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lenderNote","outputs":[{"internalType":"contract IPromissoryNote","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"originationController","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"loanId","type":"uint256"}],"name":"repay","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"repaymentController","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IFeeController","name":"_newController","type":"address"}],"name":"setFeeController","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"lender","type":"address"},{"internalType":"address","name":"borrower","type":"address"},{"internalType":"uint256","name":"loanId","type":"uint256"}],"name":"startLoan","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

# Create a contract object
contract = w3.eth.contract(address=address, abi=abi)

"""
for i in contract.events:
    print(i)
"""

""" Retrive all txns form the contract """
from_block = 13129000   # 100 blocks before the first loan  CHECK !
current_block = w3.eth.blockNumber



startedloans = contract.events.LoanStarted.getLogs(fromBlock=from_block, toBlock=current_block)
createdloans = contract.events.LoanCreated.getLogs(fromBlock=from_block, toBlock=current_block)
repaidloans = contract.events.LoanRepaid.getLogs(fromBlock=from_block, toBlock=current_block)
#feespaid = contract.events.FeesClaimed.getLogs(fromBlock=from_block, toBlock=current_block)
#loanpaused = contract.events.Paused.getLogs(fromBlock=from_block, toBlock=current_block)
#loanunpaused = contract.events.Unpaused.getLogs(fromBlock=from_block, toBlock=current_block)
#modifiedloans = contract.events.LoanRolledOver.getLogs(fromBlock=from_block, toBlock=current_block)


#LoanLibrary.sol has loanState that points to repaid or defaulted 
liquidated_expired_loans = contract.events.LoanClaimed.getLogs(fromBlock=from_block, toBlock=current_block)



"""
        struct LoanTerms {
            
            // The number of seconds representing relative due date of the loan
            uint256 durationSecs;
            
            // The amount of principal in terms of the payableCurrency
            uint256 principal;
            
            // The amount of interest in terms of the payableCurrency
            uint256 interest;
            
            // The tokenID of the collateral bundle
            uint256 collateralTokenId;
            
            // The payable currency for the loan principal and interest
            address payableCurrency;
        }
"""
initial_loan_events = {}

for i in startedloans:
    #print('\n')
    #print(i)
    _txn = i.args
    loan_id = _txn['loanId']
    lender = _txn['lender']
    borrower = _txn['borrower']
    
    
    initial_loan_events[f'{loan_id}'] = {
            'lender': lender,
            'borrower': borrower,
        }
    
    
    
parsed_started_loans = {}

for i in createdloans:

    _txn = i.args
    terms = _txn['terms']
    
    block_num = i['blockNumber']
    loan_start_stamp = w3.eth.get_block(block_num).timestamp
    loan_start = datetime.fromtimestamp(loan_start_stamp, tz=timezone.utc)
    loan_end_stamp = loan_start_stamp + terms[0] 
    loan_mat = datetime.fromtimestamp(loan_end_stamp, tz=timezone.utc)
    txn_hash = i['transactionHash'].hex()
    loan_id = _txn['loanId']
    
    #these we havce to look for in loansstarted not created...
    if loan_id in initial_loan_events.keys():
        lender = initial_loan_events[loan_id]['lender']
        borrower = initial_loan_events[loan_id]['borrower']
    
    collateral_contract = '-'                                  #cant find the ocllateral (NFT) address
    
    collateral_id = '-'
    payment_token = terms[4]
    if payment_token == '0x6B175474E89094C44Da98b954EedeAC495271d0F':
        paymnt_token = 'DAI'
        decimalz = 1e18
    elif payment_token == '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48':
        paymnt_token = 'USDC'
        decimalz = 1e6
    elif payment_token == '0xdAC17F958D2ee523a2206206994597C13D831ec7':
        paymnt_token = 'USDT'
        decimalz = 1e6
    elif payment_token == '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2':
        paymnt_token = 'WETH'
        decimalz = 1e18
        
    principal = terms[1] / decimalz
    interest = terms[2] / decimalz
    max_repayment = principal+interest
    direct_rate = max_repayment/principal -1
    loan_diff = terms[0] / 86400 #UNix day
    if loan_diff < 1:
        loan_days = round(loan_diff,1) #rounding the elapsed "days" into 1 decimal in case theres intra-days
    else:
        loan_days = round(loan_diff)
    
    annual_rate = (direct_rate / loan_days) * 365
    
    
    case = {
        "venue": "arcade",
        "contract_version": "v1",
        "status": "active",
        "block_number": block_num,
        "loan_hash": txn_hash,
        "loan_id": loan_id,
        "lender": lender,
        "borrower": borrower,
        "collateral_contract": collateral_contract,
        "collateral_id": collateral_id,
        "principal": principal,
        "max_repayment": max_repayment,
        "loan_start": loan_start,
        "timestamp": loan_start_stamp,
        "loan_maturity": loan_mat,
        "loan_duration": loan_days,
        "direct_rate": direct_rate,
        "apy": annual_rate,
        "payment_token": paymnt_token,
        "final_payment": "-",
        "admin_fee": "-",
        "loan_end": "-",
        "effective_rate": "-",
    }
    
    print('\n')
    print(case)
    
    
    parsed_started_loans[f'{loan_id}'] = case
    
    
for i in repaidloans:
    _txn = i.args
    
    loan_id = _txn['loanId']
    block_num = i['blockNumber']

    loan_end_stamp = w3.eth.get_block(block_num).timestamp
    loan_end = datetime.fromtimestamp(loan_start_stamp, tz=timezone.utc)
    
    if loan_id in parsed_started_loans.keys():
        parsed_started_loans[i]['final_payment'] = parsed_started_loans[i]['max_repayment'] 
        parsed_started_loans[i]['loan_end'] = loan_end
        parsed_started_loans[i]['effective_rate'] = parsed_started_loans[i]['direct_rate'] 
        parsed_started_loans[i]['status'] = 'repaid'
        
        
        

    
    
for i in liquidated_expired_loans:
    _txn = i.args
    
    loan_id = _txn['loanId']
    block_num = i['blockNumber']
    
    loan_end_stamp = w3.eth.get_block(block_num).timestamp
    loan_end = datetime.fromtimestamp(loan_start_stamp, tz=timezone.utc)
    
    if loan_id in parsed_started_loans.keys():
        parsed_started_loans[i]['loan_end'] = loan_end
        parsed_started_loans[i]['status'] = 'liquidated'
    