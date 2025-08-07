import pytest
from django.conf import settings


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Enable database access for all tests.
    This fixture is automatically used for all tests.
    """
    pass


@pytest.fixture
def mock_rtmp_settings():
    """Mock RTMP server settings for testing"""
    with patch.dict('django.conf.settings.__dict__', {
        'RTMP_SERVER_HOST': 'localhost',
        'RTMP_SERVER_API_PORT': 8080,
        'RTMP_HLS_BASE_URL': 'http://localhost:8080/hls/',
        'RTMP_POLLING_INTERVAL': 1
    }):
        yield