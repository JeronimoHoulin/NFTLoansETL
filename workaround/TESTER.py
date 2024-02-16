import os
import pandas as pd
from web3 import Web3
from datetime import datetime
from dotenv import load_dotenv
import json

load_dotenv()


infura_key = "7e452892f2204d6a90e814c4a03a7b1d"
w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{infura_key}"))


address1 = "0x29469395eAf6f95920E59F858042f0e28D98a20B"

# get abi from abis/blend.json
abi1 = os.path.join(os.path.dirname(__file__), "../abis/blend.json")
with open(abi1) as f:
    info_json = json.load(f)
abi1 = info_json
# Instance of the contract
contract = w3.eth.contract(address=address1, abi=abi1)


from_block = 17300050  # Mar-23-2022 few blocks before contract creation
to_block = 17350053

current_block = w3.eth.blockNumber

loans_started = contract.events.LoanOfferTaken.getLogs(
    fromBlock=from_block, toBlock=to_block
)
# repaid_loans = contract.events.Repay.getLogs(
#     fromBlock=from_block,
#     toBlock=to_block,
# )
refinanced_loans = contract.events.Refinance.getLogs(
    fromBlock=from_block,
    toBlock=to_block,
)
# seized_loans = contract.events.Seize.getLogs(
#     fromBlock=from_block,
#     toBlock=to_block,
# )

import math

for i in loans_started:
    _txn = i.args
    if (
        _txn["lienId"] == 4917
        and _txn["collection"] == "0x8821BeE2ba0dF28761AffF119D66390D594CD280"
    ):
        loan_diff = _txn["auctionDuration"] / 86400
        if loan_diff < 1:
            loan_days = round(
                loan_diff, 1
            )  # rounding the elapsed "days" into 1 decimal in case theres intra-days
        else:
            loan_days = round(loan_diff)
        principal = _txn["loanAmount"] / 1e18
        annual_rate = _txn["rate"] / 10000

        max_repayment = principal * math.exp(loan_days * annual_rate / 365)
        print(i, "started")
        print(loan_diff, " loan diff")
        print(loan_days, " loan days")
        print(max_repayment, " max repayment")
        print(annual_rate, " annual rate")
        print(principal, " principal")
        print("------------------")


for i in refinanced_loans:
    _txn = i.args
    if (
        _txn["lienId"] == 4917
        and _txn["collection"] == "0x8821BeE2ba0dF28761AffF119D66390D594CD280"
    ):
        loan_diff = _txn["newAuctionDuration"] / 86400
        if loan_diff < 1:
            loan_days = round(
                loan_diff, 1
            )  # rounding the elapsed "days" into 1 decimal in case theres intra-days
        else:
            loan_days = round(loan_diff)
        principal = _txn["newAmount"] / 1e18
        annual_rate = _txn["newRate"] / 10000

        max_repayment = principal * math.exp(loan_days * annual_rate / 365)
        print(i, "refinanced")
        print(loan_diff, " loan diff")
        print(loan_days, " loan days")
        print(max_repayment, " max repayment")
        print(annual_rate, " annual rate")
        print(principal, " principal")
        print("------------------")
