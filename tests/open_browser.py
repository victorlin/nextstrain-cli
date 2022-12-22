"""
Test nextstrain.cli.view.open_browser() works under different multiprocessing
start methods.

This file is loaded in the global pytest process, but each test function is
marked to run in its own (forked) subprocess, so we modify relevant global
state in each function.
"""
import multiprocessing
import os
import pytest

if os.name != "posix":
    pytest.skip("@pytest.mark.forked requires a POSIX platform", allow_module_level = True)


@pytest.mark.forked
def pytest_open_browser_fork():
    multiprocessing.set_start_method("fork")
    _open_browser()


@pytest.mark.forked
def pytest_open_browser_spawn():
    multiprocessing.set_start_method("spawn")
    _open_browser()


def _open_browser():
    # Must do this early, before nextstrain.cli.command.view is loaded
    os.environ["BROWSER"] = "echo"

    from nextstrain.cli.command.view import open_browser
    assert open_browser("https://nextstrain.org")
