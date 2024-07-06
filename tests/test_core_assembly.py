import pandas as pd
import pytest

from genomeinfo.interface import GenomeInfo
from genomeinfo.core.assembly import AssemblyInfo


def test_assembly_info_human():
    db = GenomeInfo.connect()

    try:
        assembly = db.assembly_info(assembly="GRCh38")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")

    assert isinstance(assembly, AssemblyInfo)
    assert assembly.assembly == "GRCh38"
    assert assembly.species == "homo_sapiens"
    assert assembly.common_name == "human"

    try:
        assembly = db.assembly_info(assembly="hg38")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")

    assert isinstance(assembly, AssemblyInfo)
    assert assembly.assembly == "hg38"
    assert assembly.species == "homo_sapiens"
    assert assembly.common_name == "human"
