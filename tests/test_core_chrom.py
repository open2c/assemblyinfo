import pandas as pd
import numpy as np
import pytest
from genomeinfo.interface import GenomeInfo


def test_filter_chromosome_data():
    db = GenomeInfo.connect()

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
    db = GenomeInfo.connect()

    result = db.get_chromnames("GRCh38", roles=["assembled"])
    assert isinstance(result, list)
    assert len(result) == 25

    result = db.get_chromnames("hg38", roles=["assembled"], units=["non-nuclear"])
    assert isinstance(result, list)
    assert len(result) == 1

    with pytest.raises(ValueError):
        db.get_chromnames("NonExistentAssembly")


def test_get_chromsizes():
    db = GenomeInfo.connect()

    result = db.get_chromsizes("GRCh38", roles=["assembled"])
    assert isinstance(result, pd.Series)
    assert len(result) == 25

    result = db.get_chromsizes("hg38", roles=["assembled"], units=["non-nuclear"])
    assert isinstance(result, pd.Series)
    assert len(result) == 1

    with pytest.raises(ValueError):
        db.get_chromsizes("NonExistentAssembly")


def test_get_seqinfo():
    db = GenomeInfo.connect()

    result = db.get_seqinfo("GRCh38")
    assert isinstance(result, pd.DataFrame)

    result = db.get_seqinfo("T2T-CHM13")
    assert isinstance(result, pd.DataFrame)

    result = db.get_seqinfo("canFam6")
    assert isinstance(result, pd.DataFrame)

    result = db.get_seqinfo("GRCm38")
    assert isinstance(result, pd.DataFrame)

    with pytest.raises(ValueError):
        db.get_seqinfo("NonExistentAssembly")
