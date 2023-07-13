from ivcap_client import __version__

def test_config():
    """Test reading Config."""
    # cfg = Config([])
    # assert type(cfg.IO_ADAPTER) == LocalIOAdapter
    assert type(__version__) == str
