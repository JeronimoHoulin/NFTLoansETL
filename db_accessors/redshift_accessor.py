import awswrangler as wr
import pandas as pd
from decimal import Decimal
from datetime import datetime, timezone


def read_latest_block_from_redshift() -> int:
    table = "nft_loans"
    con = wr.redshift.connect("Redshift-Cluster-1-Prod")
    cursor = con.cursor()
    result = cursor.execute(f"SELECT MAX(block_number) FROM onchain.{table}").fetchone()
    con.close()
    return result[0]


def load(df: pd.DataFrame = None, peer_to_pool: bool = False) -> None:
    if len(df) == 0:
        return
    table = "nft_loans"
    primary_keys = ["venue", "contract_version", "loan_id"]
    if peer_to_pool:
        primary_keys.append("loan_hash")
    wr.redshift.to_sql(
        df=df,
        con=wr.redshift.connect("Redshift-Cluster-1-Prod"),
        schema="onchain",
        table=table,
        mode="upsert",
        primary_keys=primary_keys,
        index=False,
        use_column_names=True,
        chunksize=1000,
    )

def get_active_loans_by_venue_and_version(venue: str, version: str):
    table = "nft_loans"
    con = wr.redshift.connect("Redshift-Cluster-1-Prod")
    cursor = con.cursor()
    cursor.execute(
        f"SELECT * FROM onchain.{table} WHERE status = 'active' AND venue = '{venue}' AND contract_version = '{version}'"
    )
    # Fetch column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]
    # Fetch all rows
    rows = cursor.fetchall()
    con.close()

    # Convert rows to list of dictionaries with Decimal values as floats and naive datetimes as timezone-aware datetimes
    result = [
        {
            key: float(value)
            if isinstance(value, Decimal)
            else value.replace(tzinfo=timezone.utc)
            if isinstance(value, datetime)
            else value
            for key, value in zip(column_names, row)
        }
        for row in rows
    ]
    return result

def get_active_loans_by_venue(venue: str):
    table = "nft_loans"
    con = wr.redshift.connect("Redshift-Cluster-1-Prod")
    cursor = con.cursor()
    cursor.execute(
        f"SELECT * FROM onchain.{table} WHERE status = 'active' AND venue = '{venue}'"
    )
    # Fetch column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]
    # Fetch all rows
    rows = cursor.fetchall()
    con.close()

    # Convert rows to list of dictionaries with Decimal values as floats and naive datetimes as timezone-aware datetimes
    result = [
        {
            key: float(value)
            if isinstance(value, Decimal)
            else value.replace(tzinfo=timezone.utc)
            if isinstance(value, datetime)
            else value
            for key, value in zip(column_names, row)
        }
        for row in rows
    ]
    return result
