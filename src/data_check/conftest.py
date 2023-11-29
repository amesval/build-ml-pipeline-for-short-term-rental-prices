import pytest
import pandas as pd
import wandb


def pytest_addoption(parser):
    """
    The function defines the config parameters used by Pytest.
    """
    parser.addoption("--csv", action="store")
    parser.addoption("--ref", action="store")
    parser.addoption("--kl_threshold", action="store")
    parser.addoption("--min_price", action="store")
    parser.addoption("--max_price", action="store")


@pytest.fixture(scope='session')
def data(request):
    """
    Fixture that provides the dataset to be load from a csv file.
    """
    run = wandb.init(job_type="data_tests", resume=True)

    data_path = run.use_artifact(request.config.option.csv).file()

    if data_path is None:
        pytest.fail("You must provide the --csv option on the command line")

    df = pd.read_csv(data_path)

    return df


@pytest.fixture(scope='session')
def ref_data(request):
    """
    Fixture that provides the reference dataset.
    """
    run = wandb.init(job_type="data_tests", resume=True)

    data_path = run.use_artifact(request.config.option.ref).file()

    if data_path is None:
        pytest.fail("You must provide the --ref option on the command line")

    df = pd.read_csv(data_path)

    return df


@pytest.fixture(scope='session')
def kl_threshold(request):
    """
    Returns the threshold to discriminate if two datasets are significantly different.
    """
    kl_threshold = request.config.option.kl_threshold

    if kl_threshold is None:
        pytest.fail("You must provide a threshold for the KL test")

    return float(kl_threshold)

@pytest.fixture(scope='session')
def min_price(request):
    """
    Returns the minimum acceptable price value.
    """
    min_price = request.config.option.min_price

    if min_price is None:
        pytest.fail("You must provide min_price")

    return float(min_price)

@pytest.fixture(scope='session')
def max_price(request):
    """
    Returns the maximum acceptable price value.
    """
    max_price = request.config.option.max_price

    if max_price is None:
        pytest.fail("You must provide max_price")

    return float(max_price)
