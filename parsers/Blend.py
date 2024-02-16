from datetime import datetime, timezone
from parsers.BaseParser import BaseParser
from db_accessors.redshift_accessor import get_active_loans_by_venue

import pandas as pd
import math


class BlendParser(BaseParser):
    def __init__(self, abi_file=None):
        self.address = "0x29469395eAf6f95920E59F858042f0e28D98a20B"
        if abi_file:
            self.abi_file = abi_file
        else:
            self.abi_file = "../abis/blend.json"
        self.contract_name = "blend"
        super().__init__()

    def get_logs(self, from_block, to_block):
        self.loans_started = self.contract.events.LoanOfferTaken.getLogs(
            fromBlock=from_block, toBlock=to_block
        )
        self.repaid_loans = self.contract.events.Repay.getLogs(
            fromBlock=from_block,
            toBlock=to_block,
        )
        self.refinanced_loans = self.contract.events.Refinance.getLogs(
            fromBlock=from_block,
            toBlock=to_block,
        )
        self.seized_loans = self.contract.events.Seize.getLogs(
            fromBlock=from_block,
            toBlock=to_block,
        )

    def parse_all_loans(self):
        parsed_loans_dict = {}

        for loan in self.loans_started:
            _txn = loan.args
            block_num = loan.blockNumber
            txn_hash = loan.transactionHash.hex()
            loan_id = _txn["lienId"]
            lender = _txn["lender"]
            borrower = _txn["borrower"]
            collateral_contract = _txn["collection"]
            collateral_id = _txn["tokenId"]
            principal = _txn["loanAmount"] / 1e18
            annual_rate = _txn["rate"] / 10000
            loan_diff = _txn["auctionDuration"] / 86400
            if loan_diff < 1:
                loan_days = round(
                    loan_diff, 1
                )  # rounding the elapsed "days" into 1 decimal in case theres intra-days
            else:
                loan_days = round(loan_diff)

            max_repayment = principal * math.exp(loan_days * annual_rate / 365)

            direct_rate = max_repayment / principal - 1
            if direct_rate < 0:
                direct_rate = 0

            loan_start_stamp = self.w3.eth.get_block(block_num).timestamp
            loan_start = datetime.fromtimestamp(loan_start_stamp, tz=timezone.utc)
            loan_end_stamp = loan_start_stamp + _txn["auctionDuration"]
            loan_mat = datetime.fromtimestamp(loan_end_stamp, tz=timezone.utc)

            case = {
                "venue": "blend",
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
                "payment_token": "ETH",
                "final_payment": "-",
                "admin_fee": "-",  # No admin fees ? https://twitter.com/blur_io/status/1653420586188812288
                "loan_end": "-",
                "effective_rate": "-",
            }

            parsed_loans_dict[loan_id] = case

        for loan in self.historical_active_blend_loans:
            parsed_loans_dict[loan["loan_id"]] = loan

        for loan in self.refinanced_loans:
            _txn = loan.args
            block_num = loan.blockNumber
            loan_id = _txn["lienId"]
            lender = _txn["newLender"]
            principal = _txn["newAmount"] / 1e18
            annual_rate = _txn["newRate"] / 10000
            loan_start_stamp = self.w3.eth.get_block(block_num).timestamp
            loan_start = datetime.fromtimestamp(loan_start_stamp, tz=timezone.utc)
            loan_end_stamp = loan_start_stamp + _txn["newAuctionDuration"]
            loan_mat = datetime.fromtimestamp(loan_end_stamp, tz=timezone.utc)
            loan_diff = _txn["newAuctionDuration"] / 86400  # 1 day = 86400 UNIX
            if loan_diff < 1:
                loan_days = round(
                    loan_diff, 1
                )  # rounding the elapsed "days" into 1 decimal in case theres intra-days
            else:
                loan_days = round(loan_diff)
            max_repayment = principal * math.exp(loan_days * annual_rate / 365)

            if loan_id in parsed_loans_dict:
                existing_loan = parsed_loans_dict[loan_id]

                direct_rate = max_repayment / existing_loan["principal"] - 1

                if direct_rate < 0:
                    direct_rate = 0

                existing_loan["lender"] = lender
                existing_loan["max_repayment"] = max_repayment
                existing_loan["apy"] = (
                    existing_loan["apy"] + annual_rate
                ) / 2  # Here we could do an average of all historical APYs...WDYTH @Suleyman?
                existing_loan["direct_rate"] = (
                    direct_rate + existing_loan["direct_rate"]
                )
                existing_loan["loan_maturity"] = loan_mat
                existing_loan["loan_duration"] = (
                    existing_loan["loan_duration"] + loan_days
                )

        for loan in self.repaid_loans:
            _txn = loan.args
            txn_hash = loan.transactionHash.hex()
            loan_id = _txn["lienId"]
            block_num = loan.blockNumber
            loan_end_stamp = self.w3.eth.get_block(block_num).timestamp
            loan_end = datetime.fromtimestamp(loan_end_stamp, tz=timezone.utc)

            if loan_id in parsed_loans_dict:
                existing_loan = parsed_loans_dict[loan_id]

                loan_diff = (
                    loan_end_stamp - existing_loan["timestamp"]
                )  # End - Start = UNIX difference.
                loan_days = loan_diff / 86400  # 1 day = 86400 UNIX
                if loan_days < 1:
                    loan_days = round(
                        loan_days, 1
                    )  # rounding the elapsed "days" into 1 decimal in case theres intra-days
                else:
                    loan_days = round(loan_days)

                current_debt = existing_loan["principal"] * math.exp(
                    loan_days * existing_loan["apy"] / 365
                )
                effective_rate = current_debt / existing_loan["principal"] - 1
                existing_loan["status"] = "repaid"
                existing_loan["final_payment"] = current_debt
                existing_loan["admin_fee"] = "-"
                existing_loan["loan_end"] = loan_end
                existing_loan["effective_rate"] = effective_rate
                existing_loan["loan_duration"] = loan_days

        return parsed_loans_dict.values()

    def extract(self, from_block, to_block):
        self.historical_active_blend_loans = get_active_loans_by_venue(venue="blend")
        self.get_logs(from_block=from_block, to_block=to_block)
        parsed_loans = self.parse_all_loans()
        df_loans = pd.DataFrame(parsed_loans)
        return df_loans
