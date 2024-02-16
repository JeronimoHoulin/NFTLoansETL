import os
from dotenv import load_dotenv
from run_peer_to_peer import run_peer_to_peer_parsers
from run_peer_to_pool import run_peer_to_pool_parsers
import pandas as pd


load_dotenv()

root_dir = os.getenv("root_dir")
if root_dir == "" or root_dir == None:
    root_dir = os.getcwd()

os.chdir(f"{root_dir}/outputs")  # WD where output CSV file is


if __name__ == "__main__":
    run_peer_to_peer_parsers()
    run_peer_to_pool_parsers()
