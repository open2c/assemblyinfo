import pandas as pd
import re
from typing import Any, Dict, List, Optional, NoReturn

__all__ = [
    "info",
    "get_db",
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
    """
    Returns the GenomeInfo database.

    This method returns the database stored in the class attribute `_data`.

    Parameters
    ----------
    cls : type
        The class object containing the GenomeInfo data.

    Returns
    -------
    pd.DataFrame
        The database stored in the class attribute `_data`.

    Examples
    --------
    >>> GenomeInfo.get_db()
    """

    return cls._data


def info(cls) -> None:
    """
    Display information about available entries in GenomeInfo.

    This method prints a formatted message showing the unique values for
    species, UCSC assemblies, and NCBI assemblies available in the
    GenomeInfo data.

    Parameters
    ----------
    cls : type
        The class object containing the GenomeInfo data.

    Returns
    -------
    None
        This method doesn't return any value, it only prints information.

    Notes
    -----
    The data is accessed through the `_data` attribute of the class, which
    is expected to be a pandas DataFrame with columns 'species',
    'assembly_ucsc', and 'assembly'.

    Examples
    --------
    >>> GenomeInfo.info()
    GenomeInfo available entries:
        Species:
            human, mouse, rat
        
        Assemblies (UCSC):
            hg38, mm10, rn6
        
        Assemblies (NCBI):
            GRCh38, GRCm38, Rnor_6.0

    Please pick an entry and retrieve your desired data!
    """
    data = cls._data
    species_list = data["species"].unique().tolist()
    species_names = data["common_name"].unique().tolist()
    assemblies_ucsc = data["assembly_ucsc"].dropna().unique().tolist()
    assemblies_ncbi = data["assembly"].unique().tolist()

    msg = (
        "Genome Information:\n"
        "===================\n"
        f"Species:\n  - {', '.join(species_list)}\n\n"
        f"Common Names:\n  - {', '.join(species_names)}\n\n"
        f"Assemblies (UCSC):\n  - {', '.join(assemblies_ucsc)}\n\n"
        f"Assemblies (NCBI):\n  - {', '.join(assemblies_ncbi)}\n\n"
        "Please pick an entry and retrieve your desired data!"
    )
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

    Examples
    --------
    >>> GenomeInfo.get_info("species", "homo_sapiens")
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


def get_species_info(cls, species: Optional[str] = None) -> NoReturn:
    """
    Prints the genome information for the specified species.

    Parameters
    ----------
    species : Optional[str]
        The species name to filter by.

    Returns
    ----------
    NoReturn

    Examples
    --------
    >>> GenomeInfo.get_species_info("species", "homo_sapiens")

        Genome Information for homo_sapiens:
        ===================
        Common Names:
          - human

        Assemblies (UCSC):
          - hg19, hg38, hg17, hg18, hs1

        Assemblies (NCBI):
          - GRCh37, GRCh38, NCBI35, NCBI36, T2T-CHM13
    """
    local_db = cls.get_info("species", species)
    species_names = local_db["common_name"].unique().tolist()
    assemblies_ucsc = local_db["assembly_ucsc"].dropna().unique().tolist()
    assemblies_ncbi = local_db["assembly"].unique().tolist()

    msg = (
        f"Genome Information for {species}:\n"
        "===================\n"
        f"Common Names:\n  - {', '.join(species_names)}\n\n"
        f"Assemblies (UCSC):\n  - {', '.join(assemblies_ucsc)}\n\n"
        f"Assemblies (NCBI):\n  - {', '.join(assemblies_ncbi)}\n\n"
    )
    print(msg)

def get_organism_info(cls, organism: Optional[str] = None) -> NoReturn:
    """
    Prints the genome information for the specified organism common name.

    Parameters
    ----------
    organism : Optional[str]
        The common name of the organism to filter by.

    Returns
    ----------
    NoReturn

    Examples
    --------
    >>> GenomeInfo.get_species_info("species", "homo_sapiens")

        Genome Information for human:
        ===================
        Species:
          - homo_sapiens

        Assemblies (UCSC):
          - hg19, hg38, hg17, hg18, hs1

        Assemblies (NCBI):
          - GRCh37, GRCh38, NCBI35, NCBI36, T2T-CHM13

    """
    local_db = cls.get_info("common_name", organism)
    organism_names = local_db["species"].unique().tolist()
    assemblies_ucsc = local_db["assembly_ucsc"].dropna().unique().tolist()
    assemblies_ncbi = local_db["assembly"].unique().tolist()

    msg = (
        f"Genome Information for {organism}:\n"
        "===================\n"
        f"Species:\n  - {', '.join(organism_names)}\n\n"
        f"Assemblies (UCSC):\n  - {', '.join(assemblies_ucsc)}\n\n"
        f"Assemblies (NCBI):\n  - {', '.join(assemblies_ncbi)}\n\n"
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

    Examples
    --------
    >>> GenomeInfo.get_assembly_info("hg38")
        
        {
            'assembly_level': 'Chromosome',
            'assembly_method': None,
            'assembly_name': 'GRCh38',
            'assembly_type': 'haploid-with-alt-loci',
            'bioproject': 'PRJNA168',
        }
    """
    if assembly is None:
        error_msg = (
            f"ERROR: You did not provide any assembly! Pick an assembly using the NCBI nomenclature from:\n\n",
            f"{cls._data['assembly'].unique().tolist()}\n\nor the UCSC nomenclature from:\n\n",
            f"{cls._data['assembly_ucsc'].dropna().unique().tolist()}"
        )
        raise ValueError(
            error_msg
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
        error_msg = (
            f"ERROR: {assembly} not in database! Pick an assembly using the NCBI nomenclature from:\n\n",
            f"{cls._data['assembly'].unique().tolist()}\n\nor the UCSC nomenclature from:\n\n",
            f"{cls._data['assembly_ucsc'].dropna().unique().tolist()}",
        )
        raise ValueError(
            error_msg
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

    Returns 
    -------
    Dict[str, Any]
        A dictionary containing detailed information about the assembly.

    Examples
    --------
    >>> GenomeInfo.build_assembly_info(local_db, "hg38")
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

    Raises
    ------
    ValueError
        If the provider is not 'ucsc' or 'ncbi'.

    Examples
    --------
    >>> GenomeInfo.available_assemblies()

        ['WS144',
         'WBcel215',
         'WBcel235',
         'WS190',
         'WS195',
         ...
         ]
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

    Examples
    --------
    >>> GenomeInfo.available_patches('GRCh38')
        
        ['GRCh38',
         'GRCh38.p1',
         'GRCh38.p2',
         'GRCh38.p3',
         'GRCh38.p4',
         'GRCh38.p5',
         'GRCh38.p6',
         'GRCh38.p7',
         'GRCh38.p8',
         'GRCh38.p9',
         'GRCh38.p10',
         'GRCh38.p11',
         'GRCh38.p12',
         'GRCh38.p13',
         'GRCh38.p14']
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

    Examples
    --------
    >>> GenomeInfo.available_species()
        
        ['homo_sapiens', 'mus_musculus']
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

    Examples:
    ---------
    >>> GenomeInfo.available_accessions('hg38')

        ['GCA_000001405.15',
         'GCA_000001405.16',
         'GCA_000001405.17',
         'GCA_000001405.18',
         'GCA_000001405.19',
         ...]
    """
    if not assembly:
        raise ValueError("ERROR: you must provide an assembly!")

    if assembly in cls._data["assembly"].tolist():
        db = cls._data.query(f"assembly=='{assembly}'")
        return db["genbank_accession"].tolist() + db["refseq_accession"].tolist()
    else:
        db = cls._data.query(f"assembly_ucsc=='{assembly}'")
        return db["genbank_accession"].tolist() + db["refseq_accession"].tolist()
