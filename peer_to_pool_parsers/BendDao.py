from datetime import datetime, timezone
from peer_to_pool_parsers.BaseParser import BaseParser
from zashcore.log import get_logger
import pandas as pd
from db_accessors.redshift_accessor import get_active_loans_by_venue

log = get_logger()


class BendDaoParser(BaseParser):
    def __init__(self, abi_file=None):
        self.address = "0x70b97A0da65C15dfb0FFA02aEE6FA36e507C2762"
        if abi_file:
            self.abi_file = abi_file
        else:
            self.abi_file = "../abis/benddao.json"
        self.contract_name = "benddao"
        super().__init__()

    def get_logs(self, from_block, to_block):
        borrowed1 = self.contract.events.Borrow.getLogs(
            fromBlock=from_block,
            toBlock=to_block,
        )
        repaid1 = self.contract.events.Repay.getLogs(
            fromBlock=from_block,
            toBlock=to_block,
        )
        liquidated1 = self.contract.events.Liquidate.getLogs(
            fromBlock=from_block,
            toBlock=to_block,
        )
        self.borrowed = borrowed1  # + borrowed2
        self.repaid = repaid1  # + repaid2
        self.liquidated = liquidated1  # + liquidated2

    def parse_all_loans(self):
        parsed_loans_dict = {}
        for event in self.borrowed:
            _txn = event.args
            interest = _txn.borrowRate / (10**27)
            payment_token, decimalz = self.get_payment_token_info(
                (_txn.reserve).lower()
            )
            principal = _txn.amount / decimalz
            max_repayment = principal * (1 + interest / 100)
            user = _txn.onBehalfOf
            loan_id = _txn.loanId
            block_number = event.blockNumber
            start = datetime.fromtimestamp(
                self.w3.eth.getBlock(block_number).timestamp, tz=timezone.utc
            )
            start_stamp = self.w3.eth.getBlock(block_number).timestamp
            txn_hash = event.transactionHash.hex()
            collateral_contract = _txn.nftAsset
            collateral_id = _txn.nftTokenId

            case = {
                "venue": "benddao",
                "contract_version": "v1",
                "status": "active",
                "block_number": block_number,
                "loan_hash": txn_hash,
                "loan_id": loan_id,
                "lender": "0x3b968d2d299b895a5fcf3bba7a64ad0f566e6f88",  # This is BendDao pool
                "borrower": user,
                "collateral_contract": collateral_contract,
                "collateral_id": collateral_id,
                "principal": principal,
                "max_repayment": max_repayment,
                "loan_start": start,
                "timestamp": start_stamp,
                "loan_maturity": "-",
                "loan_duration": "-",
                "direct_rate": "-",
                "apy": interest,
                "payment_token": payment_token,
                "final_payment": 0,  # extra field
                "admin_fee": "-",
                "loan_end": "-",
                "effective_rate": "-",
            }

            if loan_id in parsed_loans_dict:
                existing_one = parsed_loans_dict[loan_id]
                existing_one["principal"] = (
                    existing_one["principal"] + case["principal"]
                )
                existing_one["max_repayment"] = (
                    existing_one["max_repayment"] + case["max_repayment"]
                )
            else:
                parsed_loans_dict[loan_id] = case

        for loan in self.historical_active_benddao_loans:
            if loan["loan_id"] in parsed_loans_dict:
                loan["principal"] = (
                    loan["principal"] + parsed_loans_dict[loan["loan_id"]]["principal"]
                )
                loan["max_repayment"] = (
                    loan["max_repayment"]
                    + parsed_loans_dict[loan["loan_id"]]["max_repayment"]
                )

            parsed_loans_dict[loan["loan_id"]] = loan

        for event in self.repaid:
            _txn = event.args
            loan_id = _txn.loanId
            payment_token, decimalz = self.get_payment_token_info(
                (_txn.reserve).lower()
            )
            final_payment = _txn.amount / decimalz
            block_number = event.blockNumber
            end = datetime.fromtimestamp(
                self.w3.eth.getBlock(block_number).timestamp, tz=timezone.utc
            )
            txn_hash = event.transactionHash.hex()

            if loan_id in parsed_loans_dict:
                existing_loan = parsed_loans_dict[loan_id]

                existing_loan["final_payment"] = (
                    existing_loan["final_payment"] + final_payment
                )

                if existing_loan["final_payment"] >= existing_loan["principal"]:
                    effective_rate = (
                        existing_loan["final_payment"] / existing_loan["principal"] - 1
                    )
                    loan_duration = (
                        end - existing_loan["loan_start"]
                    ).days  # this is two dt object that give you days between.
                    if loan_duration == 0:
                        loan_duration = 1
                    linear_apy = (effective_rate / loan_duration) * 365

                    existing_loan["status"] = "repaid"
                    existing_loan["admin_fee"] = "-"  # cant see the fee in logs...
                    existing_loan["effective_rate"] = effective_rate
                    existing_loan["loan_end"] = end
                    existing_loan["loan_duration"] = loan_duration
                    existing_loan["apy"] = linear_apy

        for event in self.liquidated:
            _txn = event.args
            loan_id = _txn.loanId
            block_number = event.blockNumber
            end = datetime.fromtimestamp(
                self.w3.eth.getBlock(block_number).timestamp, tz=timezone.utc
            )
            txn_hash = event.transactionHash.hex()

            if loan_id in parsed_loans_dict:
                existing_loan = parsed_loans_dict[loan_id]
                existing_loan["status"] = "liquidated"
                existing_loan["effective_rate"] = 0
                existing_loan["loan_end"] = end

        return parsed_loans_dict.values()

    def extract(self, from_block, to_block):
        self.historical_active_benddao_loans = get_active_loans_by_venue(
            venue="benddao"
        )

        self.get_logs(from_block=from_block, to_block=to_block)
        parsed_loans = self.parse_all_loans()
        df_loans = pd.DataFrame(parsed_loans)
        return df_loans
