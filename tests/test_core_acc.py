import pytest

from genomeinfo.interface import GenomeInfo


def test_get_genbank_accession():
    db = GenomeInfo.connect()

    result = db.get_genbank_accession("GRCh38.p14")
    assert result == ["GCA_000001405.29"]

    result = db.get_genbank_accession("GRCm38.p5")
    assert result == ["GCA_000001635.7"]

    with pytest.raises(ValueError):
        db.get_genbank_accession("NonExistentAssembly")


def test_get_refseq_accession():
    db = GenomeInfo.connect()

    result = db.get_refseq_accession("GRCh38.p14")
    assert result == ["GCF_000001405.40"]

    result = db.get_refseq_accession("GRCm38.p5")
    assert result == ["GCF_000001635.25"]

    with pytest.raises(ValueError):
        db.get_refseq_accession("NonExistentAssembly")


def test_get_patch_from_accession():
    db = GenomeInfo.connect()

    result = db.get_patch_from_accession("GCF_000001405.40")
    assert result == ["GRCh38.p14"]

    result = db.get_patch_from_accession("GCA_000001635.7")
    assert result == ["GRCm38.p5"]

    with pytest.raises(ValueError):
        db.get_patch_from_accession("NonExistentAssembly")


def test_get_assembly_from_accession():
    db = GenomeInfo.connect()

    result = db.get_assembly_from_accession("GCA_000001405.29")
    assert result == ["GRCh38", "hg38"]

    result = db.get_assembly_from_accession("GCF_000001635.25")
    assert result == ["GRCm38", "mm10"]

    with pytest.raises(ValueError):
        db.get_assembly_from_accession("NonExistentAssembly")
