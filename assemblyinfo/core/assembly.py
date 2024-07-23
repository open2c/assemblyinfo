from dataclasses import dataclass
from typing import Dict, List, Optional

import pandas as pd

from .chrom import filter_chromosome_data
from .info import get_assembly_metadata

__all__ = ["Assembly", "assembly_info"]


@dataclass
class Assembly:
    """
    A dataclass to store assembly information.
    """

    assembly: str
    species: str
    common_name: str
    seqinfo: pd.DataFrame
    metadata: Dict[str, str]
    aliases: Dict[str, Dict[str, str]]

    @property
    def chromnames(self) -> List[str]:
        return self.seqinfo.index.tolist()

    @property
    def chromsizes(self) -> pd.Series:
        return self.seqinfo["length"]

    @property
    def chromeq(self) -> Dict[str, Dict[str, str]]:
        return pd.DataFrame(self.aliases).T

    def __repr__(self):
        return (f"Assembly(assembly={self.assembly}",
                f"species={self.species}",
                f"common_name={self.common_name})")


def assembly_info(
    cls,
    assembly: str,
    provider: Optional[str] = None,
    roles: Optional[List[str]] = None,
    units: Optional[List[str]] = None,
    length: Optional[str] = None,
) -> Assembly:
    """
    Get assembly information for a given assembly.
    Parameters
    ----------
    assembly : str
        Assembly name.
    provider : str, Optional
        Data provider.
    roles : List[str], Optional
        Chromosome roles.
    units : List[str], Optional
        Chromosome units.
    length : str, Optional
        Chromosome length.
    Returns
    -------
    Assembly
        Assembly information.
    Examples
    --------
    >>> assembly_info("hg38")
    >>> assembly_info("hg38", provider="ucsc")
    >>> assembly_info("hg38", roles=["assembled"])
    >>> assembly_info("hg38", units=["primary"])
    >>> assembly_info("hg38", length=">1000")
    """
    if provider == "ucsc" or provider is None:
        provider = "name"

    if provider not in ["name", "ncbi", "genbank", "refseq"]:
        raise ValueError("Invalid provider.")

    seqinfo = filter_chromosome_data(
        cls, assembly=assembly, roles=roles, units=units, length=length
    )

    aliases = (
        seqinfo[["name", "ncbi", "genbank", "refseq"]]
        .set_index(provider)
        .to_dict(orient="index")
    )

    metadata = get_assembly_metadata(cls, assembly=assembly)

    return Assembly(
        assembly=assembly,
        species=metadata["species"],
        common_name=metadata["common_name"],
        seqinfo=seqinfo.set_index(provider),
        metadata=metadata,
        aliases=aliases,
    )
