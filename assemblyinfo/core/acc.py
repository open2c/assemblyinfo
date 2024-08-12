from typing import List

__all__ = [
    "get_patch_from_accession",
    "get_assembly_from_accession",
]


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
    >>> AssemblyInfo.get_patch_from_accession("GCA_000001405.29")
    """
    if not accession:
        raise ValueError("ERROR: you must provide an accession!")
    elif (
        accession not in cls._data.genbank.dropna().tolist()
        and accession not in cls._data.refseq.dropna().tolist()
    ):
        raise ValueError("ERROR: accession not in database!")

    if accession in cls._data.genbank.dropna().tolist():
        return cls._data.query(f"genbank=='{accession}'").patch.tolist()
    elif accession in cls._data.refseq.dropna().tolist():
        return cls._data.query(f"refseq=='{accession}'").patch.tolist()
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
    >>> AssemblyInfo.get_assembly_from_accession("GCA_000001405.29")
    """
    if not accession:
        raise ValueError("ERROR: you must provide an accession!")
    elif (
        accession not in cls._data.genbank.dropna().tolist()
        and accession not in cls._data.refseq.dropna().tolist()
    ):
        raise ValueError("ERROR: accession not in database!")

    if accession in cls._data.genbank.dropna().tolist():
        return (
            cls._data.query(f"genbank=='{accession}'")
            .reset_index()
            .loc[0, ["assembly", "ucsc_name"]]
            .tolist()
        )
    elif accession in cls._data.refseq.dropna().tolist():
        return (
            cls._data.query(f"refseq=='{accession}'")
            .reset_index()
            .loc[0, ["assembly", "ucsc_name"]]
            .tolist()
        )
    else:
        raise ValueError("ERROR: accession not in database!")
