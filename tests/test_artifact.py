import os
import tempfile

from ivcap_client import artifact


def test_safepath_smoke():
    safepath = artifact.SafePath()
    assert safepath is not None


def test_safepath_unlink_does_not_delete_file():
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "x")
        with open(p, "w") as f:
            f.write("hello")

        sp = artifact.SafePath(p)
        sp.unlink()

        # should still exist because SafePath.unlink is a no-op
        assert os.path.exists(p)


def test_CMPath_():
    with tempfile.TemporaryDirectory() as td:
        with artifact.CMPath(os.path.join(td, "x")) as x_file:
            with open(x_file, "w") as f:
                f.write("hello")
        # now outside of the context manager, the CMPath should be cleaned up
        assert "x" not in os.listdir(td)
