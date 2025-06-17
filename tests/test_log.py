import io
import logging
import logging.config

import pytest

from django.conf import settings


@pytest.fixture
def setup_logger():
    test_logger = logging.getLogger("django")
    log_output = io.StringIO()
    stream_handler = logging.StreamHandler(log_output)
    stream_handler.setLevel(logging.DEBUG)
    test_logger.addHandler(stream_handler)
    yield test_logger, log_output
    test_logger.handlers = []


@pytest.fixture
def temp_log_dir(tmp_path):
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    return log_dir


def test_logging_configuration_present():
    assert hasattr(settings, "LOGGING"), "Configuração de logging deve estar presente em settings"
    assert "handlers" in settings.LOGGING, "Configuração de logging deve incluir handlers"
    assert "console" in settings.LOGGING["handlers"], "Deve haver um handler 'console' definido"


def test_debug_logging(setup_logger):
    logger, log_output = setup_logger

    original_level = logger.level
    logger.debug("Debug message should not appear")
    assert "Debug message should not appear" not in log_output.getvalue()

    logger.setLevel(logging.DEBUG)
    logger.debug("Debug message should appear")
    assert "Debug message should appear" in log_output.getvalue()


def test_info_logging(setup_logger):
    logger, log_output = setup_logger
    logger.info("Info log test message")
    assert "Info log test message" in log_output.getvalue()


def test_warning_logging(setup_logger):
    logger, log_output = setup_logger
    logger.warning("Warning log test message")
    assert "Warning log test message" in log_output.getvalue()


def test_error_logging(setup_logger):
    logger, log_output = setup_logger
    logger.error("Error log test message")
    assert "Error log test message" in log_output.getvalue()


def test_critical_logging(setup_logger):
    logger, log_output = setup_logger
    logger.critical("Critical log test message")
    assert "Critical log test message" in log_output.getvalue()


def test_exception_logging(setup_logger):
    logger, log_output = setup_logger
    try:
        raise ValueError("Test exception")
    except ValueError:
        logger.exception("Exception log test message")
    assert "Exception log test message" in log_output.getvalue()
    assert "ValueError: Test exception" in log_output.getvalue()
