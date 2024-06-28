import pandas as pd
from typing import List

__all__ = [
    "get_genbank_accession",
    "get_refseq_accession",
    "get_patch_from_accession",
    "get_assembly_from_accession",
]


def get_genbank_accession(cls, patch: str) -> str:
    """
    Returns the GenBank accession for the specified patch.

    Parameters
    ----------
    patch : str
        The patch name to filter by.

    Returns
    -------
    str
        The GenBank accession.['GRCh38.p14']

    Raises
    ------
    ValueError
        If the patch is not provided.

    Examples
    --------
    >>> GenomeInfo.get_genbank_accession("GRCh38.p14")
    """
    if not patch:
        raise ValueError("ERROR: you must provide a patch!")
    elif patch not in cls._data.patch.tolist():
        raise ValueError("ERROR: patch not in database!")

    return cls._data.query(f"patch=='{patch}'").genbank_accession.tolist()


def get_refseq_accession(cls, patch: str) -> str:
    """
    Returns the RefSeq accession for the specified patch.

    Parameters
    ----------
    patch : str
        The patch name to filter by.

    Returns
    -------
    str
        The RefSeq accession.

    Raises
    ------
    ValueError
        If the patch is not provided.

    Examples
    --------
    >>> GenomeInfo.get_refseq_accession("GRCh38.p14")
    """
    if not patch:
        raise ValueError("ERROR: you must provide a patch!")
    elif patch not in cls._data.patch.tolist():
        raise ValueError("ERROR: patch not in database!")

    return cls._data.query(f"patch=='{patch}'").refseq_accession.tolist()


def get_patch_from_accession(cls, accession: str) -> List[str]:
    """
    Returns the patches for the specified accession.

    Parameters
    ----------
    accession : str
        The accession to filter by.

    Returns
    -------
    List[str]
        A list of patches.

    Raises
    ------
    ValueError
        If the accession is not provided or not found in the database.

    Examples
    --------
    >>> GenomeInfo.get_patch_from_accession("GCA_000001405.29")
    """
    if not accession:
        raise ValueError("ERROR: you must provide an accession!")
    elif (
        accession not in cls._data.genbank_accession.dropna().tolist()
        and accession not in cls._data.refseq_accession.dropna().tolist()
    ):
        raise ValueError("ERROR: accession not in database!")

    if accession in cls._data.genbank_accession.dropna().tolist():
        return cls._data.query(f"genbank_accession=='{accession}'").patch.tolist()
    elif accession in cls._data.refseq_accession.dropna().tolist():
        return cls._data.query(f"refseq_accession=='{accession}'").patch.tolist()
    else:
        raise ValueError("ERROR: accession not in database!")


def get_assembly_from_accession(cls, accession: str) -> List[str]:
    """
    Returns the assembly names for the specified accession.

    Parameters
    ----------
    accession : str
        The accession to filter by.

    Returns
    -------
    List[str]
        A list of assembly names.

    Raises
    ------
    ValueError
        If the accession is not provided or not found in the database.

    Examples
    --------
    >>> GenomeInfo.get_assembly_from_accession("GCA_000001405.29")
    """
    if not accession:
        raise ValueError("ERROR: you must provide an accession!")
    elif (
        accession not in cls._data.genbank_accession.dropna().tolist()
        and accession not in cls._data.refseq_accession.dropna().tolist()
    ):
        raise ValueError("ERROR: accession not in database!")

    if accession in cls._data.genbank_accession.dropna().tolist():
        return (
            cls._data.query(f"genbank_accession=='{accession}'")
            .reset_index()
            .loc[0, ["assembly", "assembly_ucsc"]]
            .tolist()
        )
    elif accession in cls._data.refseq_accession.dropna().tolist():
        return (
            cls._data.query(f"refseq_accession=='{accession}'")
            .reset_index()
            .loc[0, ["assembly", "assembly_ucsc"]]
            .tolist()
        )
    else:
        raise ValueError("ERROR: accession not in database!")
