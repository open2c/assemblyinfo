from assemblyinfo.core.assembly import Assembly
from assemblyinfo.interface import AssemblyInfo


def test_assembly_info_human():
    db = AssemblyInfo.connect()

    assembly = db.assembly_info(assembly="GRCh38")

    assert isinstance(assembly, Assembly)
    assert assembly.name == "GRCh38"
    assert assembly.species == "homo_sapiens"
    assert assembly.common_name == "human"

    assembly = db.assembly_info(assembly="hg38")

    assert isinstance(assembly, Assembly)
    assert assembly.name == "hg38"
    assert assembly.species == "homo_sapiens"
    assert assembly.common_name == "human"
