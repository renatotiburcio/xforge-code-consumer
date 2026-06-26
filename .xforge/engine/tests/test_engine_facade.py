# Tests for engine facade (v3.11.5 per DR-0099)

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def test_facade_imports():
    import xforge_engine
    assert hasattr(xforge_engine, "TOOLS")

def test_tools_dict_has_19_entries():
    import xforge_engine
    tools = xforge_engine.TOOLS
    assert len(tools) >= 19, "expected 19+ tools, got " + str(len(tools))

def test_tools_have_callable():
    import xforge_engine
    for name, fn in xforge_engine.TOOLS.items():
        assert callable(fn), name + " should be callable"

def test_engine_file_size():
    import xforge_engine
    import os
    size = os.path.getsize(xforge_engine.__file__)
    assert size < 15000, "engine is " + str(size) + " bytes (>15KB means not modularized)"

def test_critical_tools_in_facade():
    import xforge_engine
    expected = ["xforge_doctor", "xforge_pack_list", "xforge_knowledge_search", "xforge_rbac_check", "xforge_graph_query"]
    for t in expected:
        assert t in xforge_engine.TOOLS, "missing: " + t
