import os
import json
from web3 import Web3
from dotenv import load_dotenv
from datetime import datetime, timezone


load_dotenv()

root_dir = os.getenv('root_dir')
if root_dir == '' or root_dir == None:
    root_dir = os.getcwd()

# Connect to the Ethereum network using web3.py
infura_key = '7e452892f2204d6a90e814c4a03a7b1d'
w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infura_key}'))

# The address of the Arcade V2 contract
address = '0x81b2F8Fc75Bab64A6b144aa6d2fAa127B4Fa7fD9' 

"""
Hey @Jerry - TheKid the new event for LoanCreated in the V2 set of contracts is LoanStarted and it is emitted by the LoanCore proxy @ 0x81b2F8Fc75Bab64A6b144aa6d2fAa127B4Fa7fD9
"""

"""
with open(f"{root_dir}/abis/arcade_v2.json") as f:
    info_json = json.load(f)

abi = info_json
"""
abi = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"uint256","name":"interestRate","type":"uint256"}],"name":"FIAC_InterestRate","type":"error"},{"inputs":[{"internalType":"address","name":"collateralAddress","type":"address"},{"internalType":"uint256","name":"collateralId","type":"uint256"}],"name":"LC_CollateralInUse","type":"error"},{"inputs":[{"internalType":"enum LoanLibrary.LoanState","name":"state","type":"uint8"}],"name":"LC_InvalidState","type":"error"},{"inputs":[],"name":"LC_LoanNotDefaulted","type":"error"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint160","name":"nonce","type":"uint160"}],"name":"LC_NonceUsed","type":"error"},{"inputs":[{"internalType":"uint256","name":"dueDate","type":"uint256"}],"name":"LC_NotExpired","type":"error"},{"inputs":[],"name":"LC_ReusedNote","type":"error"},{"inputs":[],"name":"LC_ZeroAddress","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"previousAdmin","type":"address"},{"indexed":false,"internalType":"address","name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"beacon","type":"address"}],"name":"BeaconUpgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"FeesClaimed","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"loanId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"repaidAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"remBalance","type":"uint256"}],"name":"InstallmentPaymentReceived","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"loanId","type":"uint256"}],"name":"LoanClaimed","type":"event"},{"anonymous":false,"inputs":[{"components":[{"internalType":"uint32","name":"durationSecs","type":"uint32"},{"internalType":"uint32","name":"deadline","type":"uint32"},{"internalType":"uint24","name":"numInstallments","type":"uint24"},{"internalType":"uint160","name":"interestRate","type":"uint160"},{"internalType":"uint256","name":"principal","type":"uint256"},{"internalType":"address","name":"collateralAddress","type":"address"},{"internalType":"uint256","name":"collateralId","type":"uint256"},{"internalType":"address","name":"payableCurrency","type":"address"}],"indexed":false,"internalType":"struct LoanLibrary.LoanTerms","name":"terms","type":"tuple"},{"indexed":false,"internalType":"uint256","name":"loanId","type":"uint256"}],"name":"LoanCreated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"loanId","type":"uint256"}],"name":"LoanRepaid","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"oldLoanId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newLoanId","type":"uint256"}],"name":"LoanRolledOver","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"loanId","type":"uint256"},{"indexed":false,"internalType":"address","name":"lender","type":"address"},{"indexed":false,"internalType":"address","name":"borrower","type":"address"}],"name":"LoanStarted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint160","name":"nonce","type":"uint160"}],"name":"NonceUsed","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"feeController","type":"address"}],"name":"SetFeeController","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"inputs":[],"name":"ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"BASIS_POINTS_DENOMINATOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"FEE_CLAIMER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"INSTALLMENT_PERIOD_MULTIPLIER","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"INTEREST_RATE_DENOMINATOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"LATE_FEE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ORIGINATOR_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REPAYER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"borrowerNote","outputs":[{"internalType":"contract IPromissoryNote","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"caller","type":"address"},{"internalType":"address","name":"vault","type":"address"}],"name":"canCallOn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint160","name":"nonce","type":"uint160"}],"name":"cancelNonce","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"loanId","type":"uint256"},{"internalType":"uint256","name":"currentInstallmentPeriod","type":"uint256"}],"name":"claim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IERC20Upgradeable","name":"token","type":"address"}],"name":"claimFees","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint160","name":"nonce","type":"uint160"}],"name":"consumeNonce","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"feeController","outputs":[{"internalType":"contract IFeeController","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"principal","type":"uint256"},{"internalType":"uint256","name":"interestRate","type":"uint256"}],"name":"getFullInterestAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"loanId","type":"uint256"}],"name":"getLoan","outputs":[{"components":[{"internalType":"enum LoanLibrary.LoanState","name":"state","type":"uint8"},{"internalType":"uint24","name":"numInstallmentsPaid","type":"uint24"},{"internalType":"uint160","name":"startDate","type":"uint160"},{"components":[{"internalType":"uint32","name":"durationSecs","type":"uint32"},{"internalType":"uint32","name":"deadline","type":"uint32"},{"internalType":"uint24","name":"numInstallments","type":"uint24"},{"internalType":"uint160","name":"interestRate","type":"uint160"},{"internalType":"uint256","name":"principal","type":"uint256"},{"internalType":"address","name":"collateralAddress","type":"address"},{"internalType":"uint256","name":"collateralId","type":"uint256"},{"internalType":"address","name":"payableCurrency","type":"address"}],"internalType":"struct LoanLibrary.LoanTerms","name":"terms","type":"tuple"},{"internalType":"uint256","name":"balance","type":"uint256"},{"internalType":"uint256","name":"balancePaid","type":"uint256"},{"internalType":"uint256","name":"lateFeesAccrued","type":"uint256"}],"internalType":"struct LoanLibrary.LoanData","name":"loanData","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"getRoleMember","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleMemberCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IFeeController","name":"_feeController","type":"address"},{"internalType":"contract IPromissoryNote","name":"_borrowerNote","type":"address"},{"internalType":"contract IPromissoryNote","name":"_lenderNote","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint160","name":"nonce","type":"uint160"}],"name":"isNonceUsed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lenderNote","outputs":[{"internalType":"contract IPromissoryNote","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"proxiableUUID","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"loanId","type":"uint256"}],"name":"repay","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_loanId","type":"uint256"},{"internalType":"uint256","name":"_currentMissedPayments","type":"uint256"},{"internalType":"uint256","name":"_paymentToPrincipal","type":"uint256"},{"internalType":"uint256","name":"_paymentToInterest","type":"uint256"},{"internalType":"uint256","name":"_paymentToLateFees","type":"uint256"}],"name":"repayPart","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"oldLoanId","type":"uint256"},{"internalType":"address","name":"borrower","type":"address"},{"internalType":"address","name":"lender","type":"address"},{"components":[{"internalType":"uint32","name":"durationSecs","type":"uint32"},{"internalType":"uint32","name":"deadline","type":"uint32"},{"internalType":"uint24","name":"numInstallments","type":"uint24"},{"internalType":"uint160","name":"interestRate","type":"uint160"},{"internalType":"uint256","name":"principal","type":"uint256"},{"internalType":"address","name":"collateralAddress","type":"address"},{"internalType":"uint256","name":"collateralId","type":"uint256"},{"internalType":"address","name":"payableCurrency","type":"address"}],"internalType":"struct LoanLibrary.LoanTerms","name":"terms","type":"tuple"},{"internalType":"uint256","name":"_settledAmount","type":"uint256"},{"internalType":"uint256","name":"_amountToOldLender","type":"uint256"},{"internalType":"uint256","name":"_amountToLender","type":"uint256"},{"internalType":"uint256","name":"_amountToBorrower","type":"uint256"}],"name":"rollover","outputs":[{"internalType":"uint256","name":"newLoanId","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IFeeController","name":"_newController","type":"address"}],"name":"setFeeController","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"setLock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"lender","type":"address"},{"internalType":"address","name":"borrower","type":"address"},{"components":[{"internalType":"uint32","name":"durationSecs","type":"uint32"},{"internalType":"uint32","name":"deadline","type":"uint32"},{"internalType":"uint24","name":"numInstallments","type":"uint24"},{"internalType":"uint160","name":"interestRate","type":"uint160"},{"internalType":"uint256","name":"principal","type":"uint256"},{"internalType":"address","name":"collateralAddress","type":"address"},{"internalType":"uint256","name":"collateralId","type":"uint256"},{"internalType":"address","name":"payableCurrency","type":"address"}],"internalType":"struct LoanLibrary.LoanTerms","name":"terms","type":"tuple"}],"name":"startLoan","outputs":[{"internalType":"uint256","name":"loanId","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"}],"name":"upgradeTo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint160","name":"","type":"uint160"}],"name":"usedNonces","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]'
# Create a contract object
contract = w3.eth.contract(address=address, abi=abi)

"""  FUNCTIONS """
"""
for i in contract.functions:
    print(i)
"""
""" Retrive all txns form the contract """
from_block = 0   # 100 blocks before the first loan  CHECK !
current_block = w3.eth.blockNumber



startedloans = contract.events.LoanStarted.getLogs(fromBlock=from_block, toBlock=current_block)
""" NO LOANS CREATED IN THE V2 CONTRACT"""
#createdloans = contract.events.LoanCreated.getLogs(fromBlock=from_block, toBlock=current_block)
repaidloans = contract.events.LoanRepaid.getLogs(fromBlock=from_block, toBlock=current_block)
feespaid = contract.events.FeesClaimed.getLogs(fromBlock=from_block, toBlock=current_block)
#loanpaused = contract.events.Paused.getLogs(fromBlock=from_block, toBlock=current_block)
#loanunpaused = contract.events.Unpaused.getLogs(fromBlock=from_block, toBlock=current_block)

#LoanLibrary.sol has loanState that points to repaid or defaulted 
liquidated_expired_loans = contract.events.RoleAdminChanged.getLogs(fromBlock=from_block, toBlock=current_block)


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
    tx_hash = i['transactionHash']
    block_num = i['blockNumber']
    
    
    initial_loan_events[f'{loan_id}'] = {
            'lender': lender,
            'borrower': borrower,
            'hash': tx_hash,
            'block_num': block_num
        }

    
parsed_started_loans = {}

for key, value in initial_loan_events.items():
    
    loan = contract.functions.getLoan(int(key)).call()
    
    
    loan_start_stamp = w3.eth.get_block(value['block_num']).timestamp
    loan_start = datetime.fromtimestamp(loan_start_stamp, tz=timezone.utc)
    loan_end_stamp = loan_start_stamp + loan[3][0]
    loan_mat = datetime.fromtimestamp(loan_end_stamp, tz=timezone.utc)
    txn_hash = value['hash']
    loan_id = key

    
    collateral_contract = loan[3][5]
    collateral_id = loan[3][6]
    
    payment_token = loan[3][7]
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
        
    principal = loan[3][4] / decimalz 
    direct_rate =  loan[3][3] / 1e22
    interest = principal * direct_rate
    # 0.01% is the minimum interest rate allowed by the protocol.
    max_repayment = principal+interest
    loan_diff = loan[3][0] / 86400 #UNix 1 day
    
    if loan_diff < 1:
        loan_days = round(loan_diff,1) #rounding the elapsed "days" into 1 decimal in case theres intra-days
    else:
        loan_days = round(loan_diff)
    
    annual_rate = (direct_rate / loan_days) * 365
    
    
    case = {
        "venue": "arcade",
        "contract_version": "v2",
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

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    





