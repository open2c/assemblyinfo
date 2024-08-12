import pandas as pd
import pytest

from assemblyinfo.interface import AssemblyInfo


def test_filter_chromosome_data():
    db = AssemblyInfo.connect()

    result = db.filter_chromosome_data("GRCh38", roles=["assembled"])
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 25
    assert set(result["role"]) == {"assembled"}

    result = db.filter_chromosome_data(
        "hg38", roles=["assembled"], units=["non-nuclear"]
    )
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert set(result["role"]) == {"assembled"}
    assert set(result["unit"]) == {"non-nuclear"}

    result = db.filter_chromosome_data(
        "GRCh38", roles=["assembled"], length=">133137821"
    )
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 13
    assert set(result["role"]) == {"assembled"}

    with pytest.raises(ValueError):
        db.filter_chromosome_data("NonExistentAssembly")

    result = db.filter_chromosome_data("GRCh38", roles=["non_existent_role"])
    assert len(result) == 0


def test_get_chromnames():
    db = AssemblyInfo.connect()

    result = db.get_chromnames("GRCh38", roles=["assembled"])
    assert isinstance(result, list)
    assert len(result) == 25

    result = db.get_chromnames("hg38", roles=["assembled"], units=["non-nuclear"])
    assert isinstance(result, list)
    assert len(result) == 1

    with pytest.raises(ValueError):
        db.get_chromnames("NonExistentAssembly")


def test_get_chromsizes():
    db = AssemblyInfo.connect()

    result = db.get_chromsizes("GRCh38", roles=["assembled"])
    assert isinstance(result, pd.Series)
    assert len(result) == 25

    result = db.get_chromsizes("hg38", roles=["assembled"], units=["non-nuclear"])
    assert isinstance(result, pd.Series)
    assert len(result) == 1

    with pytest.raises(ValueError):
        db.get_chromsizes("NonExistentAssembly")


def test_assembly_info():
    db = AssemblyInfo.connect()

    result = db.assembly_info("GRCh38")
    assert isinstance(result.seqinfo, pd.DataFrame)

    result = db.assembly_info("T2T-CHM13")
    assert isinstance(result.seqinfo, pd.DataFrame)

    result = db.assembly_info("canFam6")
    assert isinstance(result.seqinfo, pd.DataFrame)

    result = db.assembly_info("GRCm38")
    assert isinstance(result.seqinfo, pd.DataFrame)

    with pytest.raises(ValueError):
        db.assembly_info("NonExistentAssembly")
