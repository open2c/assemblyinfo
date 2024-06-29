import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import functools
from typing import List
import pyarrow as pa
import pyarrow.parquet as pq
from schema import *
import os
from typing import Dict, List, Tuple, NoReturn

try:
    from importlib.resources import files as resource_path
except ImportError:
    from importlib_resources import files as resource_path


def get_directories(url: str) -> List[str]:
    """
    Retrieves a list of directories from the given URL.

    Parameters
    ----------
    url : str
        The URL to fetch the directories from.

    Returns
    -------
    List[str]
        A list of directories found in the URL.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        directories = [
            a.get_text() for a in soup.find_all("a") if a.get_text().endswith("/")
        ]
    except Exception as e:
        print(f"Error fetching directories for {url}: {str(e)}")

    if len(directories) == 0:
        print(f"error with {url}, 0 dirs")
    return directories


def get_formatted_paths(paths: List[str]) -> List[Tuple]:
    """
    Helper function to format the paths and extract relevant information.

    Parameters
    ----------
    paths : List[str]
        A list of paths to format.

    Returns
    -------
    List[Tuple]
        A list of tuples containing the formatted path information.
    """
    return [
        (
            "_".join(x.split("_", 2)[:2]),  # Accession
            x.split("_", 2)[-1][:-1],  # assembly complete
            x.split("_", 2)[-1][
                :-1
            ],  # common assembly name (without patch v.) | NOW IS JUST ASSEMBLY COMPLETE -> WILL TAKE OF THIS LATER
            f"{NCBI}/{x.split('.', 1)[0].split('_')[0]}/{x.split('.', 1)[0].split('_')[1][0:3]}/{x.split('.', 1)[0].split('_')[1][3:6]}/{x.split('.', 1)[0].split('_')[1][6:9]}/{x}",
        )
        for x in paths
    ]


def create_dataframe(paths: List[str], columns: List[str]) -> pd.DataFrame:
    """
    Helper function to create a DataFrame from formatted data.

    Parameters
    ----------
    paths : List[str]
        A list of paths to format.
    columns : List[str]
        A list of column names for the DataFrame.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the formatted path information.
    """
    formatted_data = get_formatted_paths(paths)
    return pd.DataFrame(formatted_data, columns=columns)


def build_db(raw_db: pd.DataFrame) -> pd.DataFrame:
    """
    Builds a DataFrame from the raw database.

    Parameters
    ----------
    raw_db : pd.DataFrame
        The raw database to build the DataFrame from.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the formatted path information.
    """
    dfs = []

    for assembly, species in zip(raw_db["assembly_name"], raw_db["species"]):
        genbank_path = raw_db.set_index("assembly_name").loc[assembly, "genbank_path"]
        refseq_path = raw_db.set_index("assembly_name").loc[assembly, "refseq_path"]

        gb = get_directories(genbank_path)
        rf = get_directories(refseq_path)

        df1_gb = create_dataframe(
            gb, ["genbank_accession", "assembly_patch", "assembly", "genbank_path"]
        )
        df1_rf = create_dataframe(
            rf, ["refseq_accession", "assembly_patch", "assembly", "refseq_path"]
        )

        df = pd.merge(df1_gb, df1_rf, on="assembly_patch", how="outer")
        df["species"] = species
        df["common_name"] = MAP_SPECIES_NAME[species]
        dfs.append(df)

    main_df = pd.concat(dfs).reset_index(drop=True)
    main_df["assembly_x"].fillna(main_df["assembly_y"].to_dict(), inplace=True)
    main_df.drop(columns=["assembly_y"], inplace=True)

    main_df = main_df[
        [
            "assembly_x",
            "assembly_patch",
            "genbank_accession",
            "refseq_accession",
            "genbank_path",
            "refseq_path",
            "species",
        ]
    ]

    main_df = main_df[~main_df["assembly_patch"].isin(ASSEMBLY_BLACKLIST)].rename(
        columns={"assembly_x": "assembly", "assembly_patch": "patch"}
    )

    main_df["assembly"] = main_df["assembly"].apply(lambda x: (
        x.split("v")[0] if x.startswith("T2T") else
        x.split(".")[0] if x.startswith(("GRCh38.", "GRCh37.", "GRCm38.")) else
        x
    ))

    main_df["assembly_ucsc"] = [ASSEMBLY_MAP[a] for a in main_df["assembly"]]

    main_df = main_df[
        ~main_df["refseq_accession"].isin(REFSEQ_BLACKLIST)
    ].convert_dtypes()

    return main_df


def retrieve_file_from_url(url: str, pattern: str) -> List[str]:
    """
    Retrieves a list of files from the given URL.

    Parameters
    ----------
    url : str
        The URL to fetch the files from.

    Returns
    -------
    List[str]
        A list of files found in the URL.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        files = [
            a.get_text() for a in soup.find_all("a") if a.get_text().endswith(pattern)
        ]
    except Exception as e:
        print(f"Error fetching directories for {url}: {str(e)}")

    if len(files) == 0:
        print(f"error with {url}, 0 dirs")
    else:
        paths = []
        for f in files:
            path = f"{url}/{f}"
            paths.append(path)
    return paths


def get_metadata_info(url: str) -> Dict[str, str]:
    """
    Reads the report file line by line until a '##' is encountered,
    then splits the read lines and builds a dictionary from them.

    Parameters
    ----------
    url : str
        The URL to fetch the metadata from.

    Returns
    -------
    Dict[str, str]
        A dictionary containing the metadata information.
    """
    file = retrieve_file_from_url(url, "report.txt")
    report_dict = {}
    try:
        response = requests.get(file[0])
        response.raise_for_status()  # Ensure the request was successful
        lines = response.text.split("\n")
        collected_lines = []

        for line in lines:
            if line.strip() == "##" or len(line[1:].strip()) == 0:
                break
            collected_lines.append(line)

        for item in collected_lines:
            item = item[1:]
            key, value = item.split(":", 1)  # Split only on the first colon
            report_dict[key.strip().lower().replace(" ", "_")] = value.strip()

    except Exception as e:
        print(f"Error reading report file from {url}: {str(e)}")

    return report_dict


def get_stats_info(url: str) -> pd.DataFrame:
    """
    Reads the stats file line by line, then splits the read
    lines and builds a dictionary from them.

    Parameters
    ----------
    url : str
        The URL to fetch the stats from.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the stats information.
    """
    file = retrieve_file_from_url(url, "stats.txt")
    dfs = []
    try:
        response = requests.get(file[0])
        response.raise_for_status()  # Ensure the request was successful
        lines = response.text.split("\n")
        collected_lines = []

        for line in lines:
            if line.startswith("#"):
                continue
            collected_lines.append(line)

        for item in collected_lines:
            if item.strip():
                inner_df = pd.DataFrame(item.strip().split("\t")).T.replace(
                    "na", np.NaN
                )
                inner_df.columns = [
                    "unit-name",
                    "molecule-name",
                    "molecule-type",
                    "sequence-type",
                    "statistic",
                    "value",
                ]
                dfs.append(inner_df)

    except Exception as e:
        print(f"Error reading stats file from {url}: {str(e)}")

    return pd.concat(dfs)


def get_chromosome_info(url: str) -> pd.DataFrame:
    """
    Reads the report file line by line until a '##' is encountered,
    then splits the read lines and builds a dictionary from them.

    Parameters
    ----------
    url : str
        The URL to fetch the chromosome information from.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the chromosome information.
    """
    file = retrieve_file_from_url(url, "report.txt")
    dfs = []
    try:
        response = requests.get(file[0])
        response.raise_for_status()  # Ensure the request was successful
        lines = response.text.split("\n")
        collected_lines = []

        for line in lines:
            if line.startswith("#"):
                continue
            collected_lines.append(line)

        for item in collected_lines:
            if item.strip():
                inner_df = pd.DataFrame(item.strip().split("\t")).T.replace(
                    "na", np.NaN
                )
                inner_df.columns = [
                    "ncbi",
                    "role",
                    "molecule",
                    "drop",
                    "genbank",
                    "drop1",
                    "refseq",
                    "unit",
                    "length",
                    "name",
                ]
                dfs.append(inner_df)

    except Exception as e:
        print(f"Error reading report file from {url}: {str(e)}")

    return pd.concat(dfs)


def process_chromosome_info(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processes the chromosome information DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the chromosome information.

    Returns
    -------
    pd.DataFrame
        A processed DataFrame containing the chromosome information.
    """
    df = df.drop(columns=["drop", "drop1"]).reset_index(drop=True)
    df["role"] = [role.split("-")[0] for role in df["role"]]
    df = df[~df["role"].isin(["pseudo"])]

    df["unit"] = [
        unit.split()[0].lower().strip() if unit.startswith("P") else unit
        for unit in df["unit"]
    ]

    df["name"].fillna(
        {idx: f"chr{x}" for idx, x in enumerate(df["ncbi"])}, inplace=True
    )

    df = df.dropna(how="all", axis=1)

    alias = {
        molecule: name
        for name, molecule in list(
            zip(
                df[df["role"] == "assembled"]["name"],
                df[df["role"] == "assembled"]["molecule"],
            )
        )
    }

    df["molecule"] = [
        alias[mol] if not mol is np.NaN and mol in alias.keys() else mol
        for mol in df["molecule"]
    ]

    df = df.convert_dtypes()
    df["length"] = df["length"].astype(pd.Int64Dtype())

    return df


def insert_stat_info(df: pd.DataFrame, idx: int, path: str):
    """
    Inserts the stats information into the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to insert the stats information into.

    idx : int
        The index of the DataFrame to insert the stats information into.

    path : str
        The path to the stats information.
    """
    stats = get_stats_info(path)
    stats = stats[stats["unit-name"].isin(["all", "Primary Assembly", "non_nuclear"])]
    stats["molecule-type"].fillna("all", inplace=True)
    stats["sequence-type"] = [s.split("-")[0] for s in stats["sequence-type"]]

    # assembly
    stats_all = stats[stats["molecule-type"] == "all"].reset_index(drop=True)

    for i in stats_all.index:
        if (
            stats_all.loc[i, "unit-name"] == "Primary Assembly"
            and stats_all.loc[i, "sequence-type"] == "all"
        ):
            stats_all.loc[i, "sequence-type"] = "primary"
            stats_all.loc[i, "statistic"] = "-".join(
                [stats_all.loc[i, "sequence-type"], stats_all.loc[i, "statistic"]]
            )
        elif stats_all.loc[i, "unit-name"] != "all":
            tmp_name = stats_all.loc[i, "unit-name"].lower().replace(" ", "_")
            stats_all.loc[i, "statistic"] = f"{tmp_name}-" + "-".join(
                [stats_all.loc[i, "sequence-type"], stats_all.loc[i, "statistic"]]
            )

    df.at[idx, "metadata"] = df.loc[idx, "metadata"] | stats_all[
        ["statistic", "value"]
    ].set_index("statistic").astype(pd.Float64Dtype()).to_dict().get("value")

    # chr
    stats_chr = stats[stats["molecule-type"] != "all"].reset_index(drop=True)
    stats_chr["statistic"] = [
        "-".join([stats_chr.loc[idx, "sequence-type"], stats_chr.loc[idx, "statistic"]])
        for idx in stats_chr.index
    ]

    for i in stats_chr.index:
        if stats_chr.loc[i, "unit-name"] != "Primary Assembly":
            name = stats_chr.loc[i, "unit-name"].lower().replace(" ", "_")
            stats_chr.loc[i, "statistic"] = f"{name}-" + stats_chr.loc[i, "statistic"]

    stats_chr = stats_chr[["molecule-name", "statistic", "value"]]
    stats_chr = stats_chr.pivot(
        index="molecule-name", columns="statistic", values="value"
    ).astype(pd.Float64Dtype())
    # drop all columns filled with None

    tmp_df = pd.DataFrame.from_records(df.loc[idx, "seqinfo"]).set_index("ncbi")
    df.at[idx, "seqinfo"] = (
        pd.merge(tmp_df, stats_chr, left_index=True, right_index=True, how="left")
        .reset_index()
        .to_dict(orient="records")
    )

def builder(init_db: pd.DataFrame) -> pd.DataFrame:
    """
    Builds the database from the initial DataFrame.

    Parameters
    ----------
    init_db : pd.DataFrame
        The initial DataFrame to build the database from.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the formatted path information.
    """
    db = build_db(init_db).reset_index(drop=True)

    db["seqinfo"] = [dict]*len(db)
    db["metadata"] = [dict]*len(db)
    
    for idx in db.index:
        path1 = db.loc[idx, "genbank_path"]
        path2 = db.loc[idx, "refseq_path"]
    
        if pd.notna(path1):
            report_metadata = get_metadata_info(path1)
            chrom_df = get_chromosome_info(path1)
            chrom_df = process_chromosome_info(chrom_df)
            
            db.at[idx,"seqinfo"] = chrom_df.to_dict(orient='records')
            db.at[idx,"metadata"] = report_metadata
            insert_stat_info(db, idx, path1)
        else:
            report_metadata = get_metadata_info(path2)
            chrom_df = get_chromosome_info(path2)
            chrom_df = process_chromosome_info(chrom_df)
            
            db.at[idx,"seqinfo"] = chrom_df.to_dict(orient='records')
            db.at[idx,"metadata"] = report_metadata
            insert_stat_info(db, idx, path2)
            
    for p in db.groupby("assembly").patch:
        sorted_patches = sorted(p[-1].tolist(), key=get_version, reverse=True)
        if len(sorted_patches) > 1:
            patch = sorted_patches[1]
        else:
            patch = sorted_patches[0]
        
        db.loc[db.query(f"patch=='{patch}'").index, "version"] = "latest"

    return db
