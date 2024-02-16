import os
import json
import pandas as pd
from web3 import Web3
from datetime import datetime
from datetime import timezone
from dotenv import load_dotenv
from zashcore.log import get_logger

from parsers.BaseParser import BaseParser

load_dotenv()
log = get_logger()


class NFTFiParser(BaseParser):
    def __init__(self, abi_file=None):
        self.address = "0x88341d1a8F672D2780C8dC725902AAe72F143B0c"
        if abi_file:
            self.abi_file = abi_file
        else:
            self.abi_file = "../abis/nftfi_v1.json"
        self.contract_name = "nftfi_v1"
        super().__init__()

    def get_logs(self, from_block, to_block):
        self.started_loans = self.contract.events.LoanStarted.getLogs(
            fromBlock=from_block,
            toBlock=to_block,
        )
        self.liquidated_loans = self.contract.events.LoanLiquidated.getLogs(
            fromBlock=from_block,
            toBlock=to_block,
        )
        self.repaid_loans = self.contract.events.LoanRepaid.getLogs(
            fromBlock=from_block,
            toBlock=to_block,
        )

        self.repaid_loans_dict = {}
        self.liquidated_loans_dict = {}

        for loan in self.repaid_loans:
            self.repaid_loans_dict[loan.args["loanId"]] = loan.args

        for loan in self.liquidated_loans:
            self.liquidated_loans_dict[loan.args["loanId"]] = loan.args

        self.parsed_active_loans = []
        self.parsed_liquidated_loans = []
        self.parsed_repaid_loans = []
        self.parsed_expired_loans = []

    def parse_historical_started_loans(self, loan):
        loan_id = loan.get("loan_id")
        payment_token = loan.get("payment_token")
        decimalz = self.payment_token_decimalz_map(payment_token)
        principal = loan.get("principal", 0)
        loan_mat = loan.get("loan_maturity", 0)

        if loan_id in self.repaid_loans_dict:
            _repay = self.repaid_loans_dict[loan_id]

            payment = _repay["amountPaidToLender"] / decimalz
            admin_fee = _repay["adminFee"] / decimalz
            real_rate = payment / principal - 1

            loan["status"] = "repaid"
            loan["final_payment"] = payment
            loan["admin_fee"] = admin_fee
            loan["effective_rate"] = real_rate

            self.parsed_repaid_loans.append(loan)

        elif loan_id in self.liquidated_loans_dict:
            _liquidate = self.liquidated_loans_dict[loan_id]

            loan_liquidation = datetime.fromtimestamp(
                _liquidate["loanLiquidationDate"], tz=timezone.utc
            )

            loan["status"] = "liquidated"
            loan["effective_rate"] = 0
            loan["loan_end"] = loan_liquidation

            self.parsed_liquidated_loans.append(loan)

        elif (
            loan_id not in self.repaid_loans_dict
            and loan_id not in self.liquidated_loans_dict
        ) and loan_mat < datetime.now(timezone.utc):
            loan["status"] = "expired"
            loan["effective_rate"] = 0
            loan["loan_end"] = loan_mat

            self.parsed_expired_loans.append(loan)

    def parse(self, _txn, loan):
        payment_token, decimalz = self.get_payment_token_info(
            _txn["loanERC20Denomination"].lower()
        )

        if payment_token is None:
            return

        block_num = loan.blockNumber
        txn_hash = loan.transactionHash.hex()
        loan_id = _txn["loanId"]
        lender = _txn["lender"]
        borrower = _txn["borrower"]
        collateral_contract = _txn["nftCollateralContract"]
        collateral_id = _txn["nftCollateralId"]
        principal = _txn["loanPrincipalAmount"] / decimalz
        max_repayment = _txn["maximumRepaymentAmount"] / decimalz
        loan_start = datetime.fromtimestamp(_txn["loanStartTime"], tz=timezone.utc)
        loan_start_stamp = _txn["loanStartTime"]
        loan_mat = datetime.fromtimestamp(
            (_txn["loanStartTime"] + _txn["loanDuration"]), tz=timezone.utc
        )
        loan_diff = (loan_mat - loan_start).days

        direct_rate, compound_apy, linear_apy = self.calculate_rates(
            loan_start=loan_start,
            loan_mat=loan_mat,
            principal=principal,
            max_repayment=max_repayment,
            loan_diff=loan_diff,
        )
        if direct_rate is None and compound_apy is None and linear_apy is None:
            return

        base_case = {
            "venue": "nftfi",
            "contract_version": "v1",
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
            "loan_duration": loan_diff,
            "direct_rate": direct_rate,
            "apy": linear_apy,
            "payment_token": payment_token,
            "final_payment": "-",
            "admin_fee": "-",
            "loan_end": "-",
            "effective_rate": "-",
        }

        if loan_id in self.repaid_loans_dict:
            _repay = self.repaid_loans_dict[loan_id]

            payment = _repay["amountPaidToLender"] / decimalz
            admin_fee = _repay["adminFee"] / decimalz
            real_rate = payment / principal - 1

            base_case["status"] = "repaid"
            base_case["final_payment"] = payment
            base_case["admin_fee"] = admin_fee
            base_case["effective_rate"] = real_rate

            self.parsed_repaid_loans.append(base_case)

        elif loan_id in self.liquidated_loans_dict:
            _liquidate = self.liquidated_loans_dict[loan_id]

            loan_liquidation = datetime.fromtimestamp(
                _liquidate["loanLiquidationDate"], tz=timezone.utc
            )

            base_case["status"] = "liquidated"
            base_case["effective_rate"] = 0
            base_case["loan_end"] = loan_liquidation

            self.parsed_liquidated_loans.append(base_case)

        elif (
            loan_id not in self.repaid_loans_dict
            and loan_id not in self.liquidated_loans_dict
        ) and loan_mat < datetime.now(timezone.utc):
            base_case["status"] = "expired"
            base_case["effective_rate"] = 0
            base_case["loan_end"] = loan_mat

            self.parsed_expired_loans.append(base_case)
        else:
            base_case["status"] = "active"
            base_case["final_payment"] = "-"

            self.parsed_active_loans.append(base_case)

    def extract(self, from_block, to_block):
        self.get_logs(from_block=from_block, to_block=to_block)

        for loan in self.started_loans:
            _txn = loan.args
            self.parse(_txn, loan)

        for loan in self.historical_active_nftfi_v1_loans:
            self.parse_historical_started_loans(loan)

        all_loans_v1 = (
            self.parsed_liquidated_loans
            + self.parsed_repaid_loans
            + self.parsed_expired_loans
        )

        df = pd.DataFrame(all_loans_v1)

        return df
