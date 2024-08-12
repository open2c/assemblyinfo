import pytest

from assemblyinfo.interface import AssemblyInfo


def test_get_patch_from_accession():
    db = AssemblyInfo.connect()

    result = db.get_patch_from_accession("GCF_000001405.40")
    assert result == ["p14"]

    result = db.get_patch_from_accession("GCA_000001635.7")
    assert result == ["p5"]

    with pytest.raises(ValueError):
        db.get_patch_from_accession("NonExistentAssembly")


def test_get_assembly_from_accession():
    db = AssemblyInfo.connect()

    result = db.get_assembly_from_accession("GCA_000001405.29")
    assert result == ["GRCh38", "hg38"]

    result = db.get_assembly_from_accession("GCF_000001635.25")
    assert result == ["GRCm38", "mm10"]

    with pytest.raises(ValueError):
        db.get_assembly_from_accession("NonExistentAssembly")
