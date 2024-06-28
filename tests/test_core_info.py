import unittest
from unittest.mock import patch
from io import StringIO
from genomeinfo.interface import GenomeInfo


def test_method_attachment():
    db = GenomeInfo.connect()
    assert hasattr(db, "info"), "Method info is not attached"


def test_method_execution():
    genome_info = GenomeInfo.connect()

    try:
        genome_info.info()
    except Exception as e:
        assert False, f"Method execution failed: {str(e)}"


def test_get_species_info():
    genome_info = GenomeInfo.connect()

    assert hasattr(
        genome_info, "get_species_info"
    ), "Method get_species_info is not attached"

    try:
        genome_info.get_species_info("homo_sapiens")
    except Exception as e:
        assert False, f"Method execution failed: {str(e)}"


def test_get_assembly_info_ncbi():
    genome_info = GenomeInfo.connect()

    assert hasattr(
        genome_info, "get_assembly_info"
    ), "Method get_assembly_info is not attached"

    try:
        genome_info.get_assembly_info("GRCh38")
    except Exception as e:
        assert False, f"Method execution failed: {str(e)}"


def test_get_assembly_info_ucsc():
    genome_info = GenomeInfo.connect()

    try:
        rs = genome_info.get_assembly_info("hg38")
    except Exception as e:
        assert False, f"Method execution failed: {str(e)}"

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result if empty"


def test_get_assembly_info_t2t():
    genome_info = GenomeInfo.connect()

    try:
        rs = genome_info.get_assembly_info("T2T-CHM13")
    except Exception as e:
        assert False, f"Method execution failed: {str(e)}"

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result if empty"


def test_available_assemblies():
    genome_info = GenomeInfo.connect()

    try:
        rs = genome_info.available_assemblies()
    except Exception as e:
        assert False, f"Method execution failed: {str(e)}"

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result is empty"


def test_get_organism_info():
    genome_info = GenomeInfo.connect()

    with patch("sys.stdout", new=StringIO()) as fake_out:
        try:
            genome_info.get_organism_info("human")
        except Exception as e:
            assert False, f"Method execution failed: {str(e)}"

        output = fake_out.getvalue()

    assert output.strip() != "", "Nothing was printed"


def test_available_patches():
    genome_info = GenomeInfo.connect()

    try:
        rs = genome_info.available_patches()
    except Exception as e:
        assert False, f"Method execution failed: {str(e)}"

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result is empty"


def test_available_accessions():
    genome_info = GenomeInfo.connect()

    try:
        rs = genome_info.available_accessions("GRCh38")
    except Exception as e:
        assert False, f"Method execution failed: {str(e)}"

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result is empty"

    try:
        rs = genome_info.available_accessions("hg38")
    except Exception as e:
        assert False, f"Method execution failed: {str(e)}"

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result is empty"
