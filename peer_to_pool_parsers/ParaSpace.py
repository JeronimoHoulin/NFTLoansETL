from datetime import datetime, timezone
from peer_to_pool_parsers.BaseParser import BaseParser

import pandas as pd


class ParaSpaceParser(BaseParser):
    def __init__(self, address, abi_file, from_block, to_block):
        super().__init__(address, abi_file, from_block, to_block)

    def get_logs(self, from_block, to_block):
        current_block = self.w3.eth.blockNumber
        # from_block = 16976560 - 1000
        # to_block = 16976560 - 900
        """
        supply_coin1 = self.contract.events.Supply.getLogs(
            fromBlock=from_block, toBlock=to_block
        )
        supply_coin2 = self.contract.events.Supply.getLogs(
            fromBlock=to_block + 1, toBlock=current_block
        )

        withdraw_coin1 = self.contract.events.Withdraw.getLogs(
            fromBlock=from_block, toBlock=to_block
        )
        withdraw_coin2 = self.contract.events.Withdraw.getLogs(
            fromBlock=to_block + 1, toBlock=current_block
        )
        """
        """
        liquidate_coin1 = self.contract.events.LiquidateERC20.getLogs(
            fromBlock=from_block, toBlock=to_block
        )
        liquidate_coin2 = self.contract.events.LiquidateERC20.getLogs(
            fromBlock=to_block + 1, toBlock=current_block
        )
        """
        """
        # Pooling events ERC721
        supply_nft1 = self.contract.events.SupplyERC721.getLogs(
            fromBlock=from_block, toBlock=to_block
        )
        supply_nft2 = self.contract.events.SupplyERC721.getLogs(
            fromBlock=to_block + 1, toBlock=current_block
        )

        withdraw_nft1 = self.contract.events.WithdrawERC721.getLogs(
            fromBlock=from_block, toBlock=to_block
        )
        withdraw_nft2 = self.contract.events.WithdrawERC721.getLogs(
            fromBlock=to_block + 1, toBlock=current_block
        )
        """

        liquidate_nft1 = self.contract.events.LiquidateERC721.getLogs(
            fromBlock=from_block, toBlock=to_block
        )
        liquidate_nft2 = self.contract.events.LiquidateERC721.getLogs(
            fromBlock=to_block + 1, toBlock=current_block
        )
        """
        self.supply_coin = supply_coin1 + supply_coin2
        self.withdraw_coin = withdraw_coin1 + withdraw_coin2
        """
        #self.liquidate_coin = liquidate_coin1 + liquidate_coin2
        """
        self.supply_nft = supply_nft1 + supply_nft2
        self.withdraw_nft = withdraw_nft1 + withdraw_nft2
        """
        self.liquidate_nft = liquidate_nft1 + liquidate_nft2

        borrowed1 = self.contract.events.Borrow.getLogs(
            fromBlock=from_block, toBlock=to_block
        )
        borrowed2 = self.contract.events.Borrow.getLogs(
            fromBlock=to_block + 1, toBlock=current_block
        )

        repay1 = self.contract.events.Repay.getLogs(
            fromBlock=from_block, toBlock=to_block
        )
        repay2 = self.contract.events.Repay.getLogs(
            fromBlock=to_block + 1, toBlock=current_block
        )

        self.borrowed = (
            borrowed1 + borrowed2
        )  ##Emitted on borrow() and flashLoan() when debt needs to be opened
        self.repaid = repay1 + repay2
    """
    def parse_supplied_nfts(self):
        parsed_supplied = []
        for event in self.supply_nft:
            _txn = event.args
            supplied_token = _txn.reserve
            user = _txn.user
            block_num = event.blockNumber
            start = datetime.fromtimestamp(
                self.w3.eth.getBlock(block_num).timestamp, tz=timezone.utc
            )
            start_stamp = self.w3.eth.getBlock(block_num).timestamp
            txn_hash = event.transactionHash.hex()
            tkn_amt = len(_txn.tokenData)
            payment_token, decimalz = self.get_payment_token_info(
                supplied_token.lower()
            )

            case = {
                "method": "supply",
                "venue": "ParaSpace",
                "contractVersion": "v1",
                "hash": txn_hash,
                "blockNumber": block_num,
                "timestamp": start_stamp,
                "borrower": user,
                "date": start,
                "asset": payment_token,
                "amount": tkn_amt,
            }

            parsed_supplied.append(case)
        return parsed_supplied
    """
    """
    def parse_withdrawn_nfts(self):
        parsed_withdrawn = []
        for event in self.withdraw_nft:
            _txn = event.args
            withdrawn_token = _txn.reserve
            user = _txn.user
            block_num = event.blockNumber
            start = datetime.fromtimestamp(
                self.w3.eth.getBlock(block_num).timestamp, tz=timezone.utc
            )
            start_stamp = self.w3.eth.getBlock(block_num).timestamp
            txn_hash = event.transactionHash.hex()
            tkn_amt = len(_txn.tokenIds)
            payment_token, decimalz = self.get_payment_token_info(
                withdrawn_token.lower()
            )

            case = {
                "method": "withdraw",
                "venue": "ParaSpace",
                "contractVersion": "v1",
                "hash": txn_hash,
                "blockNumber": block_num,
                "timestamp": start_stamp,
                "borrower": user,
                "date": start,
                "asset": payment_token,
                "amount": tkn_amt,
            }

            parsed_withdrawn.append(case)
        return parsed_withdrawn
    """
    """
    def parse_supplied_coins(self):
        parsed_supplied_coins = []
        for event in self.supply_coin:
            _txn = event.args
            supplied_coin = _txn.reserve
            user = _txn.user
            block_num = event.blockNumber
            start = datetime.fromtimestamp(
                self.w3.eth.getBlock(block_num).timestamp, tz=timezone.utc
            )
            start_stamp = self.w3.eth.getBlock(block_num).timestamp
            txn_hash = event.transactionHash.hex()

            payment_token, decimalz = self.get_payment_token_info(supplied_coin.lower())

            amount = _txn.amount / decimalz

            case = {
                "method": "supply",
                "venue": "ParaSpace",
                "contractVersion": "v1",
                "hash": txn_hash,
                "blockNumber": block_num,
                "timestamp": start_stamp,
                "lender": user,
                "date": start,
                "asset": payment_token,
                "amount": amount,
            }

            parsed_supplied_coins.append(case)
        return parsed_supplied_coins
    """
    """
    def parse_withdrawn_coins(self):
        parsed_withdrawn_coins = []
        for event in self.withdraw_coin:
            _txn = event.args
            withdrawn_coin = _txn.reserve
            user = _txn.user
            block_num = event.blockNumber
            start = datetime.fromtimestamp(
                self.w3.eth.getBlock(block_num).timestamp, tz=timezone.utc
            )
            start_stamp = self.w3.eth.getBlock(block_num).timestamp
            txn_hash = event.transactionHash.hex()
            payment_token, decimalz = self.get_payment_token_info(
                withdrawn_coin.lower()
            )
            amount = _txn.amount / decimalz

            case = {
                "method": "withdraw",
                "venue": "ParaSpace",
                "contractVersion": "v1",
                "hash": txn_hash,
                "blockNumber": block_num,
                "timestamp": start_stamp,
                "lender": user,
                "date": start,
                "asset": payment_token,
                "amount": amount,
            }

            parsed_withdrawn_coins.append(case)
        return parsed_withdrawn_coins
    """
    """
    def parse_liq_coins(self):
        parsed_liq_coins = []
        for event in self.liquidate_coin:
            _txn = event.args
            liquidated_user = _txn.borrower
            collateral_coin = _txn.collateralAsset
            borrowed_asset = _txn.liquidationAsset
            borrowed_token, decimalz = self.get_payment_token_info(
                borrowed_asset.lower()
            )

            borrowed_amount = _txn.liquidationAmount / decimalz
            payment_token, decimalz = self.get_payment_token_info(
                collateral_coin.lower()
            )

            amount = _txn.liquidatedCollateralAmount / decimalz

            block_num = event.blockNumber
            start = datetime.fromtimestamp(
                self.w3.eth.getBlock(block_num).timestamp, tz=timezone.utc
            )
            start_stamp = self.w3.eth.getBlock(block_num).timestamp
            txn_hash = event.transactionHash.hex()

            case = {
                "method": "liquidate_coin",
                "venue": "ParaSpace",
                "contractVersion": "v1",
                "hash": txn_hash,
                "blockNumber": block_num,
                "timestamp": start_stamp,
                "borrower": liquidated_user,
                "liquidatedDate": start,
                "borrowedAsset": borrowed_token,
                "borrowedAmount": borrowed_amount,
                "liquidatedAsset": payment_token,
                "liquidatedAmount": amount,
            }

            parsed_liq_coins.append(case)
        return parsed_liq_coins
    """
    def parse_borrowed(self):
        parsed_loans_dict = {}

        for event in self.borrowed:
            _txn = event.args
            payment_token, decimalz = self.get_payment_token_info(
                (_txn.reserve).lower()
            )
            interest = _txn.borrowRate / (10**27)
            principal = _txn.amount / decimalz

            max_repayment = principal * (1 + interest / 100)
            user = _txn.user

            block_num = event.blockNumber
            start = datetime.fromtimestamp(
                self.w3.eth.getBlock(block_num).timestamp, tz=timezone.utc
            )
            start_stamp = self.w3.eth.getBlock(block_num).timestamp

            txn_hash = event.transactionHash.hex()

            case = {
                "venue": "ParaSpace",
                "contractVersion": "v1",
                "status": "active",
                "blockNumber": block_num,
                "loanHash": txn_hash,
                "loanId": '-', #No loan ID in paraspace.. we should check if user deposited an NFT.. then use that as COLLATERAL..
                "lender": '0x638a98BBB92a7582d07C52ff407D49664DC8b3Ee', #This is ParaSpace pool
                "borrower": user,
                "collateralContract": '-',
                "collateralId": '-',
                "principal": principal,
                "maxRepayment": max_repayment,
                "loanStart": start,
                "timestamp": start_stamp,
                "loanMaturity": '-',
                "loanDuration": '-',
                "directRate": interest, #Check direct rate @Jerry
                "compoundAPY": '-',
                "linearAPY": '-',
                "paymentToken": payment_token,
                "finalPayment": '-',
                "adminFee": "-",
                "loanEnd": "-",
                "effectiveRate": "-",
            }

            parsed_loans_dict[loan_id] = case


        parsed_repaid = []
        for event in self.repaid:
            _txn = event.args
            payment_token, decimalz = self.get_payment_token_info(
                (_txn.reserve).lower()
            )
            block_num = event.blockNumber
            start = datetime.fromtimestamp(
                self.w3.eth.getBlock(block_num).timestamp, tz=timezone.utc
            )
            start_stamp = self.w3.eth.getBlock(block_num).timestamp

            max_repayment = _txn.amount / decimalz
            user = _txn.user

            txn_hash = event.transactionHash.hex()

            payment_datetime = datetime.fromtimestamp(
                self.w3.eth.getBlock(block_num).timestamp, tz=timezone.utc
            )

            case = {
                "method": "repaid",
                "venue": "ParaSpace",
                "contractVersion": "v1",
                "hash": txn_hash,
                "blockNumber": block_num,
                "timestamp": start_stamp,
                "borrower": user,
                "asset": payment_token,
                "repayment": max_repayment,
                "repaidDate": payment_datetime,
            }

            parsed_repaid.append(case)
    

        parsed_liquidated = []
        for event in self.liquidate_nft:
            _txn = event.args
            liquidated_user = _txn.borrower
            collateral_nft = _txn.collateralAsset
            borrowed_asset = _txn.liquidationAsset
            borrowed_token, decimalz = self.get_payment_token_info(
                borrowed_asset.lower()
            )

            borrowed_amount = _txn.liquidationAmount / decimalz
            payment_token, decimalz = self.get_payment_token_info(
                collateral_nft.lower()
            )

            amount = 1

            block_num = event.blockNumber
            start = datetime.fromtimestamp(
                self.w3.eth.getBlock(block_num).timestamp, tz=timezone.utc
            )
            start_stamp = self.w3.eth.getBlock(block_num).timestamp
            txn_hash = event.transactionHash.hex()

            case = {
                "method": "liquidated_nft",
                "venue": "ParaSpace",
                "contractVersion": "v1",
                "hash": txn_hash,
                "blockNumber": block_num,
                "timestamp": start_stamp,
                "borrower": liquidated_user,
                "liquidatedDate": start,
                "borrowedAsset": borrowed_token,
                "borrowedAmount": borrowed_amount,
                "liquidatedAsset": payment_token,
                "liquidatedAmount": amount,
            }

            parsed_liquidated.append(case)




        return parsed_loanss


    def get_loans(self, from_block, to_block):
        self.get_logs(from_block=from_block, to_block=to_block)

        """
        df_supplied_coins = pd.DataFrame(self.parse_supplied_coins())
        df_supplied_nfts = pd.DataFrame(self.parse_supplied_nfts())

        df_withdrawn_coins = pd.DataFrame(self.parse_withdrawn_coins())
        df_withdrawn_nfts = pd.DataFrame(self.parse_withdrawn_nfts())

        df_liq_coins = pd.DataFrame(self.parse_liq_coins())

        """
        parsed_loans = pd.DataFrame(self.parse_borrowed())
        #df_repaid = pd.DataFrame(self.parse_repaid())
        #df_liquidations = pd.DataFrame(self.parse_liquidated_nfts())
        return parsed_loans
