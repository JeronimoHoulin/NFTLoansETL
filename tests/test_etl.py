import pandas as pd
from parsers.NFTFi_V1 import NFTFiParser
from parsers.NFTFi_V2 import NFTFiV2Parser
from parsers.NFTFi_V2_Old import NFTFiV2OldParser
from parsers.NFTFi_V2_New import NFTFiV2NewParser
from parsers.X2Y2_V1 import X2Y2V1Parser
from parsers.X2Y2_V2 import X2Y2V2Parser
from peer_to_pool_parsers.BendDao import BendDaoParser
from parsers.Blend import BlendParser
import os
from .conftest import data_directory

valid_schema = {

}

def get_parsers(data_directory):
    return [
        NFTFiParser(abi_file=os.path.join(data_directory, "nftfi_v1.json")),
        NFTFiV2Parser(abi_file=os.path.join(data_directory, "nftfi_v2.json")),
        NFTFiV2OldParser(abi_file=os.path.join(data_directory, "nftfi_v2_old.json")),
        NFTFiV2NewParser(abi_file=os.path.join(data_directory, "nftfi_v2_new.json")),
        X2Y2V1Parser(abi_file=os.path.join(data_directory, "x2y2_v1.json")),
        X2Y2V2Parser(abi_file=os.path.join(data_directory, "x2y2_v2.json")),
        BendDaoParser(abi_file=os.path.join(data_directory, "benddao.json")),
        BlendParser(abi_file=os.path.join(data_directory, "blend.json")),
    ]


def test_no_transfer_block(data_directory):
    for parser in get_parsers(data_directory):
        transfers_df = parser.extract(15555964, 15555964)
        assert transfers_df.empty


def test_block(data_directory):
    blend = get_parsers(data_directory=data_directory)[-1]
    benddao = get_parsers(data_directory=data_directory)[-2]
    benddao_df = benddao.extract(16637525, 16637525)
    transfers_df = blend.extract(17167713, 17167900)
    assert len(benddao_df) > 0
    assert type(benddao_df) == pd.DataFrame
    assert len(transfers_df) > 0
    assert type(transfers_df) == pd.DataFrame




# check one exact record
