import pandas as pd
import os
from web3 import Web3
from db_accessors.redshift_accessor import (
    read_latest_block_from_redshift,
    load,
)
from config import settings
from zashcore.log import get_logger

from parsers.BaseParser import BaseParser
from parsers.NFTFi_V1 import NFTFiParser
from parsers.NFTFi_V2 import NFTFiV2Parser
from parsers.NFTFi_V2_Old import NFTFiV2OldParser
from parsers.NFTFi_V2_New import NFTFiV2NewParser
from parsers.X2Y2_V1 import X2Y2V1Parser
from parsers.X2Y2_V2 import X2Y2V2Parser
from parsers.X2Y2_V3 import X2Y2V3Parser
from parsers.Blend import BlendParser

log = get_logger()


def set_peer_to_peer_parser_list() -> list[BaseParser]:
    parser_list = [
        NFTFiParser(),
        NFTFiV2Parser(),
        NFTFiV2OldParser(),
        NFTFiV2NewParser(),
        X2Y2V1Parser(),
        X2Y2V2Parser(),
        X2Y2V3Parser(),
        BlendParser(),
    ]

    return parser_list


def _transform(df: pd.DataFrame):
    if len(df) == 0:
        return

    lower_fields = [
        "loan_hash",
        "venue",
        "lender",
        "borrower",
        "collateral_contract",
    ]
    for field in lower_fields:
        df[field] = df[field].str.lower()

    none_fields = [
        "final_payment",
        "loan_start",
        "loan_maturity",
        "loan_end",
        "apy",
        "effective_rate",
        "loan_duration",
        "direct_rate",
        "admin_fee",
    ]
    for field in none_fields:
        df[field] = df[field].apply(lambda x: None if x == "-" else x)

    na_fields = [
        "collateral_id",
        "principal",
        "max_repayment",
        "timestamp",
        "loan_start",
        "loan_maturity",
        "loan_end",
    ]
    for field in na_fields:
        df[field] = df[field].apply(lambda x: None if pd.isna(x) else x)

    df["collateral_id"] = df["collateral_id"].astype(str)

    df.reset_index(drop=True, inplace=True)


def run_peer_to_peer_parsers():
    w3 = Web3(Web3.HTTPProvider(settings.alchemy_url))
    latest_block_redshift = read_latest_block_from_redshift()
    latest_block_onchain = w3.eth.blockNumber

    log.info("Running peer to peer parsers")
    log.info(f"Latest block redshift: {latest_block_redshift}")
    log.info(f"Latest block onchain: {latest_block_onchain}")

    parser_list: list[BaseParser] = set_peer_to_peer_parser_list()
    result_list = []

    for parser in parser_list:
        log.info("Parsing loans", parser=parser)
        parser_result: pd.DataFrame = parser.extract(
            from_block=latest_block_redshift,
            to_block=latest_block_onchain,
        )
        result_list.append(parser_result)

    df = pd.concat(result_list)
    _transform(df)
    log.info("Upserting loans", loans_length=len(df))
    load(df=df)
    log.info("Upserted loans", loans_length=len(df))
    log.info("Finished running peer to peer parsers")
