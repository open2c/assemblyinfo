import pandas as pd
import re
from typing import Any, Dict, List, Optional

__all__ = [
    "info",
    "get_info",
    "get_species_info",
    "get_organism_info",
    "build_assembly_info",
    "get_version",
    "get_assembly_info",
    "available_assemblies",
    "available_patches",
    "available_species",
    "available_accessions",
]


def get_db(cls) -> pd.DataFrame:
    """Returns the entire database as a pandas DataFrame."""
    return cls._data


def info(cls) -> None:
    data = cls._data
    msg = f"""
    GenomeInfo available entries:
        species: {data["species"].unique()}
        assemblies (UCSC): {data["assembly_ucsc"].unique()}
        assemblies (NCBI): {data["assembly"].unique()}
        Please pick an entry and retrieve your desired data!
    """
    print(msg)


def get_info(cls, key: str, value: Optional[str]) -> pd.DataFrame:
    """
    Retrieves information from the database based on the specified key and value.

    Parameters
    ----------
    key : str
        The key to filter by (e.g., 'species', 'common_name').
    value : Optional[str]
        The value to filter for the given key.

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame based on the key and value.

    Raises
    ------
    ValueError
        If the value is None or the key is not found in the database.
    """
    if value is None:
        raise ValueError(f"ERROR! Pick a {key}: {cls._data[key].unique()}")

    local_db = cls._data.set_index(key).loc[value, :]
    return local_db


def get_version(s: List[str]):
    """
    Extracts the version number from each string in a list.

    Parameters
    ----------
    s : List[str]
        A list of strings containing version numbers.

    Returns
    -------
    Tuple[int]
        A tuple containing the version number.
    """
    match = re.search(r"(\d+)(?:\.\d+)*$", s)
    if match:
        return tuple(map(int, match.group().split(".")))
    return (0,)


def get_species_info(cls, species: Optional[str] = None) -> None:
    """
    Prints the genome information for the specified species.

    Parameters
    ----------
    species : Optional[str]
        The species name to filter by.
    """
    local_db = cls.get_info("species", species)
    print(
        f'GenomeInfo data for {species}:\n\nname: {local_db["common_name"].unique()}\nassemblies (UCSC): {local_db["assembly_ucsc"].unique()}\nassemblies (NCBI): {local_db["assembly"].unique()}'
    )


def get_organism_info(cls, organism: Optional[str] = None) -> None:
    """
    Prints the genome information for the specified organism common name.

    Parameters
    ----------
    organism : Optional[str]
        The common name of the organism to filter by.
    """
    local_db = cls.get_info("common_name", organism)
    print(
        f'GenomeInfo data for {organism}:\n\nspecies: {local_db["species"].unique()}\nassemblies (UCSC): {local_db["assembly_ucsc"].unique()}\nassemblies (NCBI): {local_db["assembly"].unique()}'
    )


def get_assembly_info(cls, assembly: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieves the detailed information for the specified assembly.

    Parameters
    ----------
    assembly : Optional[str]
        The assembly name to filter by, using either NCBI or UCSC nomenclature.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing detailed information about the assembly.

    Raises
    ------
    ValueError
        If the assembly is not provided or not found in the database.
    """
    if assembly is None:
        raise ValueError(
            f'ERROR: You did not provide any assembly! Pick an assembly using the NCBI nomenclature from: {cls._data["assembly"].unique()} or the UCSC nomenclature from: {cls._data["assembly_ucsc"].unique()}'
        )

    if assembly in cls._data["assembly"].tolist():
        local_db = cls._data.set_index("assembly").loc[assembly, :]
        if isinstance(local_db, pd.Series):
            local_db = local_db.to_frame().T.reset_index(names="assembly")
        else:
            local_db = local_db.reset_index(names="assembly")
        out = cls.build_assembly_info(local_db, assembly)

        return out

    elif assembly in cls._data["assembly_ucsc"].dropna().tolist():
        local_db = cls._data.set_index("assembly_ucsc").loc[assembly, :]
        if isinstance(local_db, pd.Series):
            local_db = local_db.to_frame().T.reset_index(names="assembly_ucsc")
        else:
            local_db = local_db.reset_index(names="assembly_ucsc")
        out = cls.build_assembly_info(local_db, assembly)

        return out
    else:
        raise ValueError(
            f'ERROR: {assembly} not in database! Pick an assembly using the NCBI nomenclature from: {cls._data["assembly"].unique()} or the UCSC nomenclature from: {cls._data["assembly_ucsc"].unique()}'
        )


def build_assembly_info(cls, local_db: pd.DataFrame, assembly: str) -> Dict[str, Any]:
    """
    Builds a dictionary with detailed information for the specified assembly.

    Parameters
    ----------
    local_db : pd.DataFrame
        The filtered DataFrame containing information about the assembly.
    assembly : str
        The name of the assembly.

    Returnsenbank_accession	refseq_accession	genbank_path	refseq_path	species	assembly_ucsc	seqinfo
    -------
    Dict[str, Any]
        A dictionary containing detailed information about the assembly.
    """
    if len(local_db.patch) > 1:
        latest = sorted(local_db.patch.tolist(), key=get_version, reverse=True)[0]
        core = local_db.query(f"patch=='{latest}'").metadata.tolist()[0]
    else:
        core = local_db.query(
            f"patch=='{local_db.assembly.unique()[0]}'"
        ).metadata.tolist()[0]

    return core | {
        "species": local_db.species.unique()[0],
        "name": local_db.common_name.unique()[0],
        "synonyms": [local_db.assembly.unique()[0], local_db.assembly_ucsc.unique()[0]],
        "patches": local_db.patch.tolist(),
        "genbank": local_db.genbank_accession.tolist(),
        "refseq": local_db.refseq_accession.tolist(),
    }


def available_assemblies(cls, provider: Optional[str] = None) -> List[str]:
    """
    Returns the list of available assemblies.

    Parameters
    ----------
    provider : Optional[str]
        The provider to filter by ('ucsc' or 'ncbi').

    Returns
    -------
    List[str]
        A list of available assemblies.
    """
    if not provider:
        return (
            cls._data.assembly.unique().tolist()
            + cls._data.assembly_ucsc.unique().tolist()
        )
    else:
        if provider == "ucsc":
            return cls._data.assembly_ucsc.unique().tolist()
        elif provider == "ncbi":
            return cls._data.assembly.unique().tolist()
        else:
            raise ValueError("ERROR: provider must be either 'ucsc' or 'ncbi'!")


def available_patches(cls, assembly: Optional[str] = None) -> List[str]:
    """
    Returns the list of available patches.

    Parameters
    ----------
    assembly : Optional[str]
        The assembly name to filter by.

    Returns
    -------
    List[str]
        A list of available patches.
    """
    if not assembly:
        return cls._data.patch.unique().tolist()
    else:
        return cls._data.query(f"assembly=='{assembly}'").patch.unique().tolist()


def available_species(cls) -> List[str]:
    """
    Returns the list of available species.

    Returns
    -------
    List[str]
        A list of available species.
    """
    return cls._data.species.unique().tolist()


def available_accessions(cls, assembly: str) -> List[str]:
    """
    Returns the list of available accessions for the specified assembly.

    Parameters
    ----------
    assembly : str
        The assembly name to filter by.

    Returns
    -------
    List[str]
        A list of available accessions.

    Raises
    ------
    ValueError
        If the assembly is not provided.
    """
    if not assembly:
        raise ValueError("ERROR: you must provide an assembly!")

    if assembly in cls._data["assembly"].tolist():
        db = cls._data.query(f"assembly=='{assembly}'")
        return db["genbank_accession"].tolist() + db["refseq_accession"].tolist()
    else:
        db = cls._data.query(f"assembly_ucsc=='{assembly}'")
        return db["genbank_accession"].tolist() + db["refseq_accession"].tolist()
