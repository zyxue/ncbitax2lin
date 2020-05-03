import gzip
import io

import pandas as pd

from ncbitax2lin import utils


def strip(str_: str) -> str:
    """
    :param str_: a string
    """
    return str_.strip()


@utils.timeit
def load_nodes(nodes_file: str) -> pd.DataFrame:
    """
    load nodes.dmp and convert it into a pandas.DataFrame
    """
    df = pd.read_csv(
        nodes_file,
        sep="|",
        header=None,
        index_col=False,
        names=[
            "tax_id",
            "parent_tax_id",
            "rank",
            "embl_code",
            "division_id",
            "inherited_div_flag",
            "genetic_code_id",
            "inherited_GC__flag",
            "mitochondrial_genetic_code_id",
            "inherited_MGC_flag",
            "GenBank_hidden_flag",
            "hidden_subtree_root_flag",
            "comments",
        ],
    )

    # To get rid of flanking tab characters
    df["rank"] = df["rank"].apply(strip)
    df["embl_code"] = df["embl_code"].apply(strip)
    df["comments"] = df["comments"].apply(strip)
    return df


@utils.timeit
def load_names(names_file: str) -> pd.DataFrame:
    """
    load names.dmp and convert it into a pandas.DataFrame
    """
    df = pd.read_csv(
        names_file,
        sep="|",
        header=None,
        index_col=False,
        names=["tax_id", "name_txt", "unique_name", "name_class"],
    )
    df["name_txt"] = df["name_txt"].apply(strip)
    df["unique_name"] = df["unique_name"].apply(strip)
    df["name_class"] = df["name_class"].apply(strip)

    sci_df = df[df["name_class"] == "scientific name"]
    sci_df.reset_index(drop=True, inplace=True)
    return sci_df


def read_names_and_nodes(names_file: str, nodes_file: str) -> pd.DataFrame:
    # data downloaded from ftp://ftp.ncbi.nih.gov/pub/taxonomy/
    # args = parse_args()
    nodes_df = load_nodes(nodes_file)
    names_df = load_names(names_file)

    return (
        nodes_df.merge(names_df, on="tax_id")[
            ["tax_id", "parent_tax_id", "rank", "name_txt"]
        ]
        .rename(columns={"name_txt": "rank_name"})
        .reset_index(drop=True)
    )


def write_lineages_to_disk(df_lineages: pd.DataFrame, output_path: str) -> None:
    """Gzip lineages and write them to disk"""
    cols = [
        "tax_id",
        "superkingdom",
        "phylum",
        "class",
        "order",
        "family",
        "genus",
        "species",
    ]
    other_cols = sorted([col for col in df_lineages.columns if col not in cols])
    output_cols = cols + other_cols

    df_lineages.to_csv(
        output_path, index=False, compression="gzip", columns=output_cols
    )
