import os
import json
import pandas as pd
from web3 import Web3
from datetime import datetime
from datetime import timezone
from dotenv import load_dotenv
from parsers.BaseParser import BaseParser
from db_accessors.redshift_accessor import get_active_loans_by_venue_and_version

load_dotenv()


class NFTFiV2NewParser(BaseParser):
    def __init__(self, abi_file=None):
        self.address = "0x81b2F8Fc75Bab64A6b144aa6d2fAa127B4Fa7fD9"
        if abi_file:
            self.abi_file = abi_file
        else:
            self.abi_file = "../abis/arcade_v2.json"
        self.contract_name = "arcade_v2"
        super().__init__()

    def get_logs(self, from_block, to_block):
        self.started_loans = self.contract.events.LoanStarted.getLogs(
            fromBlock=from_block, toBlock=to_block
        )
        self.repaid_loans = self.contract.events.LoanRepaid.getLogs(
            fromBlock=from_block, toBlock=to_block
        )
        self.fees_paid = self.contract.events.FeesClaimed.getLogs(
            fromBlock=from_block, toBlock=to_block
        )

        self.liquidated_expired_loans = self.contract.events.RoleAdminChanged.getLogs(
            fromBlock=from_block, toBlock=to_block
        )

    def parse_all_loans(self):
        parsed_started_loans = {}

        for hist in self.historical_active_arcade_v1_loans:
            loan_id = hist["loan_id"]
            parsed_started_loans[loan_id] = hist

        for i in self.started_loans:
            _txn = i.args
            key = _txn["loanId"]
            lender = _txn["lender"]
            borrower = _txn["borrower"]
            value = {
                "lender": lender,
                "borrower": borrower,
                "hash": i["transactionHash"],
                "block_num": i["blockNumber"],
            }

            loan = self.contract.functions.getLoan(int(key)).call()

            loan_start_stamp = self.w3.eth.get_block(value["block_num"]).timestamp
            loan_start = datetime.fromtimestamp(loan_start_stamp, tz=timezone.utc)
            loan_end_stamp = loan_start_stamp + loan[3][0]
            loan_mat = datetime.fromtimestamp(loan_end_stamp, tz=timezone.utc)
            txn_hash = value["hash"]
            loan_id = key

            collateral_contract = loan[3][5]
            collateral_id = loan[3][6]

            payment_token = loan[3][7]
            payment_token, decimalz = self.get_payment_token_info(payment_token)

            principal = loan[3][4] / decimalz
            direct_rate = loan[3][3] / 1e22
            interest = principal * direct_rate
            # 0.01% is the minimum interest rate allowed by the protocol.
            max_repayment = principal + interest
            loan_diff = loan[3][0] / 86400  # UNix 1 day

            if loan_diff < 1:
                loan_days = round(
                    loan_diff, 1
                )  # rounding the elapsed "days" into 1 decimal in case theres intra-days
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
                "payment_token": payment_token,
                "final_payment": "-",
                "admin_fee": "-",
                "loan_end": "-",
                "effective_rate": "-",
            }

            print("\n")
            print(case)

            parsed_started_loans[f"{loan_id}"] = case

        for i in self.repaid_loans:
            _txn = i.args

            loan_id = _txn["loanId"]
            block_num = i["blockNumber"]

            loan_end_stamp = self.w3.eth.get_block(block_num).timestamp
            loan_end = datetime.fromtimestamp(loan_start_stamp, tz=timezone.utc)

            if loan_id in parsed_started_loans:
                parsed_started_loans[loan_id]["final_payment"] = parsed_started_loans[
                    loan_id
                ]["max_repayment"]
                parsed_started_loans[loan_id]["loan_end"] = loan_end
                parsed_started_loans[loan_id]["effective_rate"] = parsed_started_loans[
                    loan_id
                ]["direct_rate"]
                parsed_started_loans[loan_id]["status"] = "repaid"

        for i in self.liquidated_expired_loans:
            _txn = i.args

            loan_id = _txn["loanId"]
            block_num = i["blockNumber"]

            loan_end_stamp = self.w3.eth.get_block(block_num).timestamp
            loan_end = datetime.fromtimestamp(loan_start_stamp, tz=timezone.utc)

            if loan_id in parsed_started_loans:
                parsed_started_loans[loan_id]["loan_end"] = loan_end
                parsed_started_loans[loan_id]["status"] = "liquidated"

        return parsed_started_loans.values()

    def extract(self, from_block, to_block):
        self.historical_active_arcade_v1_loans = get_active_loans_by_venue_and_version(
            venue="arcade", version="v1"
        )
        self.get_logs(from_block=from_block, to_block=to_block)
        self.parsed_started_loans = self.parse_all_loans()
        df = pd.DataFrame(self.parsed_started_loans)
        return df
