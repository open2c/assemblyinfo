import pandas as pd
from typing import List, Optional

__all__ = [
    "filter_chromosome_data",
    "get_chromnames",
    "get_chromsizes",
    "get_chrom_eq",
    "get_seqinfo",
]


def filter_chromosome_data(
    cls,
    assembly: str,
    roles: Optional[List[str]] = None,
    units: Optional[List[str]] = None,
    length: Optional[str] = None,
) -> pd.DataFrame:
    """
    Filters the chromosome data based on the provided parameters.

    Parameters
    ----------
    assembly : str
        The assembly name to filter by.
    roles : Optional[List[str]]
        The roles to filter by.
    units : Optional[List[str]]
        The units to filter by.
    length : Optional[str]
        The length condition to filter by (e.g., '> 1000').

    Returns
    -------
    pd.DataFrame
        The filtered chromosome data.

    Raises
    ------
    ValueError
        If the assembly is not found in the database.

    Examples
    --------
    >>> GenomeInfo.filter_chromosome_data("hg38", roles=["assembled"])
    """
    if assembly in cls._data["assembly"].tolist():
        group = "assembly"
    elif assembly in cls._data["assembly_ucsc"].dropna().tolist():
        group = "assembly_ucsc"
    else:
        raise ValueError(f"{assembly} not in database!")

    q1 = f'{group} == "{assembly}" and version == "latest"'
    q2 = ""

    if length:
        q2 += f"length {length}"

    if roles:
        if len(q2) > 0:
            q2 += f" and role.isin({roles})"
        else:
            q2 += f"role.isin({roles})"

    if units:
        if len(q2) > 0:
            q2 += f"  and unit.isin({units})"
        else:
            q2 += f"unit.isin({units})"

    if len(q2) > 0:
        mask = (
            pd.DataFrame.from_records(cls._data.query(q1).seqinfo.iloc[0])
            .query(q2)
            .convert_dtypes()
        )
    else:
        mask = pd.DataFrame.from_records(
            cls._data.query(q1).seqinfo.iloc[0]
        ).convert_dtypes()

    return mask


def get_chromnames(
    cls,
    assembly: str,
    provider: Optional[str] = None,
    roles: Optional[List[str]] = None,
    units: Optional[List[str]] = None,
    length: Optional[str] = None,
) -> List[str]:
    """
    Returns the chromosome names for the specified assembly.

    Parameters
    ----------
    assembly : str
        The assembly name to filter by.
    provider : Optional[str]
        The provider to filter by ('ucsc', 'genbank', 'refseq', 'ncbi').
    roles : Optional[List[str]]
        The roles to filter by.
    units : Optional[List[str]]
        The units to filter by.
    length : Optional[str]
        The length condition to filter by (e.g., '> 1000').

    Returns
    -------
    List[str]
        A list of chromosome names.

    Raises
    ------
    ValueError
        If the provider is not valid.

    Examples
    --------
    >>> GenomeInfo.get_chromnames("hg38", provider="ucsc")
    """
    if not provider or provider == "ucsc":
        colname = "name"
    elif provider in ["genbank", "refseq", "ncbi"]:
        colname = provider
    else:
        error_msg = (
            f"{provider} is not a valid provider!\n",
            "Valid providers are 'ucsc', 'genbank', 'refseq', 'ncbi'",
        )
        raise ValueError(error_msg)

    return cls.filter_chromosome_data(assembly, roles, units, length)[colname].tolist()


def get_chromsizes(
    cls,
    assembly: str,
    provider: Optional[str] = None,
    roles: Optional[List[str]] = None,
    units: Optional[List[str]] = None,
    length: Optional[str] = None,
) -> pd.Series:
    """
    Returns the chromosome sizes for the specified assembly.

    Parameters
    ----------
    assembly : str
        The assembly name to filter by.
    provider : Optional[str]
        The provider to filter by ('ucsc', 'genbank', 'refseq', 'ncbi').
    roles : Optional[List[str]]
        The roles to filter by.
    units : Optional[List[str]]
        The units to filter by.
    length : Optional[str]
        The length condition to filter by (e.g., '> 1000').

    Returns
    -------
    pd.Series
        A series with chromosome sizes.

    Raises
    ------
    ValueError
        If the provider is not valid.

    Examples
    --------
    >>> GenomeInfo.get_chromsizes("hg38", provider="ucsc")
    """
    if not provider or provider == "ucsc":
        colname = "name"
    elif provider in ["genbank", "refseq", "ncbi"]:
        colname = provider
    else:
        error_msg = (
            f"{provider} is not a valid provider!\n",
            "Valid providers are 'ucsc', 'genbank', 'refseq', 'ncbi'",
        )
        raise ValueError(error_msg)

    df = cls.filter_chromosome_data(assembly, roles, units, length)
    return df.set_index(colname)["length"]


def get_chrom_eq(
    cls,
    assembly: str,
    providers: Optional[List[str]] = None,
    roles: Optional[List[str]] = None,
    units: Optional[List[str]] = None,
    length: Optional[str] = None,
) -> pd.DataFrame:
    """
    Returns the chromosome equivalence for the specified assembly.

    Parameters
    ----------
    assembly : str
        The assembly name to filter by.
    providers : Optional[List[str]]
        The providers to filter by (e.g., 'ucsc', 'genbank', 'refseq', 'ncbi').
    roles : Optional[List[str]]
        The roles to filter by.
    units : Optional[List[str]]
        The units to filter by.
    length : Optional[str]
        The length condition to filter by (e.g., '> 1000').

    Returns
    -------
    pd.DataFrame
        A DataFrame with chromosome equivalence across different providers.

    Raises
    ------
    ValueError
        If the provider is not valid.

    Examples
    --------
    >>> GenomeInfo.get_chrom_eq("hg38", providers=["ucsc", "genbank"])
    """
    if not providers:
        providers = ["name", "ncbi", "genbank", "refseq"]
    else:
        if "ucsc" in providers:
            providers = [p if p != "ucsc" else "name" for p in providers]

    return cls.filter_chromosome_data(assembly, roles, units, length)[providers]


def get_seqinfo(cls, assembly: str) -> pd.DataFrame:
    """
    Returns the sequence information for the specified assembly.

    Parameters
    ----------
    assembly : str
        The assembly name to filter by.

    Returns
    -------
    pd.DataFrame
        A DataFrame with sequence information.

    Raises
    ------
    ValueError
        If the assembly is not found in the database.

    Examples
    --------
    >>> GenomeInfo.get_seqinfo("hg38")
    """
    if assembly in cls._data["assembly"].tolist():
        group = "assembly"
    elif assembly in cls._data["assembly_ucsc"].dropna().tolist():
        group = "assembly_ucsc"
    elif assembly in cls._data["patch"].dropna().tolist():
        group = "patch"
    else:
        error_msg = (
            f"{assembly} not in database!\n",
            "Valid assemblies are:\n\n",
            f"NCBI:\n{cls._data.assembly.unique().tolist()}\n\n",
            f"UCSC:\n{cls._data.assembly_ucsc.dropna().unique().tolist()}\n\n",
            f"Patch:\n{cls._data.patch.dropna().unique().tolist()}",
        )
        raise ValueError(f"{assembly} not in database!")

    q1 = f'{group} == "{assembly}"'
    q2 = 'version == "latest"'

    local_db = cls._data.query(q1)
    if len(local_db) > 1:
        return (
            pd.DataFrame.from_records(local_db.query(q2).seqinfo.iloc[0])
            .convert_dtypes()
            .set_index("name")
        )
    else:
        return (
            pd.DataFrame.from_records(local_db.seqinfo.iloc[0])
            .convert_dtypes()
            .set_index("name")
        )
