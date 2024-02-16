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
        self.address = "0x59e57F9A313A2EB1c7357eCc331Ddca14209F403"
        if abi_file:
            self.abi_file = abi_file
        else:
            self.abi_file = "../abis/arcade_v1.json"
        self.contract_name = "arcade_v1"
        super().__init__()

    def get_logs(self, from_block, to_block):
        self.started_loans = self.contract.events.LoanStarted.getLogs(
            fromBlock=from_block, toBlock=to_block
        )
        self.created_loans = self.contract.events.LoanCreated.getLogs(
            fromBlock=from_block, toBlock=to_block
        )
        self.repaid_loans = self.contract.events.LoanRepaid.getLogs(
            fromBlock=from_block, toBlock=to_block
        )

        self.liquidated_expired_loans = self.contract.events.LoanClaimed.getLogs(
            fromBlock=from_block, toBlock=to_block
        )

    def parse_all_loans(self):
        parsed_started_loans = {}

        for hist in self.historical_active_arcade_v1_loans:
            loan_id = hist["loan_id"]
            parsed_started_loans[loan_id] = hist



        for i in self.started_loans:
            _txn = i.args
            loan_id = _txn["loanId"]
            lender = _txn["lender"]
            borrower = _txn["borrower"]

            parsed_started_loans[loan_id] = {
                "lender": lender,
                "borrower": borrower,
            }


        for i in self.created_loans:
            _txn = i.args
            terms = _txn["terms"]

            block_num = i["blockNumber"]
            loan_start_stamp = self.w3.eth.get_block(block_num).timestamp
            loan_start = datetime.fromtimestamp(loan_start_stamp, tz=timezone.utc)
            loan_end_stamp = loan_start_stamp + terms[0]
            loan_mat = datetime.fromtimestamp(loan_end_stamp, tz=timezone.utc)
            txn_hash = i["transactionHash"].hex()
            loan_id = _txn["loanId"]

            if loan_id in parsed_started_loans:
                lender = parsed_started_loans[loan_id]["lender"]
                borrower = parsed_started_loans[loan_id]["borrower"]

            collateral_contract = "-"

            collateral_id = "-"
            payment_token = terms[4]
            payment_token, decimalz = self.get_payment_token_info(
                payment_token=payment_token
            )

            principal = terms[1] / decimalz
            interest = terms[2] / decimalz
            max_repayment = principal + interest
            direct_rate = max_repayment / principal - 1
            loan_diff = terms[0] / 86400  # UNix day
            if loan_diff < 1:
                loan_days = round(
                    loan_diff, 1
                )  # rounding the elapsed "days" into 1 decimal in case theres intra-days
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
                "payment_token": payment_token,
                "final_payment": "-",
                "admin_fee": "-",
                "loan_end": "-",
                "effective_rate": "-",
            }

            parsed_started_loans[loan_id] = case

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
