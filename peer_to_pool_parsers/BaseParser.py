from web3 import Web3
from abc import ABC, abstractmethod
from config import settings
import os
import json

from db_accessors.redshift_accessor import get_active_loans_by_venue

class BaseParser:
    def __init__(self):
        w3 = Web3(Web3.HTTPProvider(settings.alchemy_url))
        self.w3 = w3
        with open(self.abi_file) as f:
            info_json = json.load(f)

        abi = info_json
        self.contract = w3.eth.contract(address=self.address, abi=abi)


    def get_payment_token_info(self, payment_token):
        tokens = {
            "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2": ("WETH", 1e18),
            "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0": ("wstETH", 1e18),
            "0xBe9895146f7AF43049ca1c1AE358B0541Ea49704": ("cbETH", 1e18),
            "0xae78736cd615f374d3085123a210448e74fc6393": ("rETH", 1e18),
            "0x030ba81f1c18d280636f32af80b9aad02cf0854e": ("aETH", 1e18),
            "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84": ("stETH", 1e18),
            "0x4d224452801ACEd8B2F0aebE155379bb5D594381": ("APE", 1e18),
            "0xC5c9fB6223A989208Df27dCEE33fC59ff5c26fFF": ("cAPE", 1e18),
            "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599": ("WBTC", 1e8),
            "0x6B175474E89094C44Da98b954EedeAC495271d0F": ("DAI", 1e18),
            "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48": ("USDC", 1e6),
            "0xdAC17F958D2ee523a2206206994597C13D831ec7": ("USDT", 1e6),
            "0x853d955aCEf822Db058eb8505911ED77F175b99e": ("FRAX", 1e18),
            "0x5283D291DBCF85356A21bA090E6db59121208b44": ("BLUR", 1e18),
            "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D": ("BAYC", None),
            "0x60E4d786628Fea6478F785A6d7e704777c86a7c6": ("MAYC", None),
            "0xba30E5F9Bb24caa003E9f2f0497Ad287FDF95623": ("BAKC", None),
            "0x764AeebcF425d56800eF2c84F2578689415a2DAa": ("SewerPass", None),
            "0xBd3531dA5CF5857e7CfAA92426877b022e612cf8": ("PudgyPenguins", None),
            "0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e": ("Doodles", None),
            "0xb7F7F6C52F2e2fdb1963Eab30438024864c313F6": ("WPUNKS", None),
            "0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB": ("CryptoPunks", None),
            "0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B": ("CloneX", None),
            "0x34d85c9CDeB23FA97cb08333b511ac86E1C4E258": ("Otherdeed", None),
            "0xED5AF388653567Af2F388E6224dC7C4b3241C544": ("Azuki", None),
            "0x7Bd29408f11D2bFC23c34f18275bBf23bB716Bc7": ("Meebits", None),
            "0x23581767a106ae21c074b2276D25e5C3e136a68b": ("Moonbirds", None),
            "0xC36442b4a4522E871399CD717aBDD847Ab11FE88": ("UniswapV3", None),
            "0xE012Baf811CF9c05c408e879C399960D1f305903": ("Otherside Koda", None),
            "0x5b1085136a811e55b2Bb2CA1eA456bA82126A376": ("Otherside Vessle", None),
            "0x790B2cF29Ed4F310bf7641f013C65D4560d28371": ("Otherdeed Expanded", None),
            "0x306b1ea3ecdf94aB739F1910bbda052Ed4A9f949": ("Beanz", None),
            "0x8821BeE2ba0dF28761AffF119D66390D594CD280": ("DeGods", None),
        }
        tokens = {k.lower(): v for k, v in tokens.items()}
        return tokens.get(payment_token, (None, None))

    @abstractmethod
    def get_logs(self, from_block, to_block):
        pass

    @abstractmethod
    def extract(self, from_block, to_block):
        pass
