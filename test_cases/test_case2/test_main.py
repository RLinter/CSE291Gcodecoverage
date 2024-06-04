import pytest
import requests_mock
from main import fetch_page_title

@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m

def test_fetch_page_title_with_valid_content(mock_requests):
    # Setup the mock to return a specific content for a URL
    mock_requests.get('http://example.com', text='<html><head><title>Example Domain</title></head><body></body></html>')

    # Call the crawler function
    title = fetch_page_title('http://example.com')

    # Assert that the title is correctly fetched
    assert title == 'Example Domain', "The crawler did not fetch the correct title"

def test_fetch_page_title_with_no_title_tag(mock_requests):
    # Setup the mock to return content without a title tag
    mock_requests.get('http://example.com', text='<html><head></head><body>No title here</body></html>')

    # Call the crawler function
    title = fetch_page_title('http://example.com')

    # Assert that the title is correctly identified as missing
    assert title == 'No title found', "The crawler did not handle the absence of a title tag correctly"

def test_fetch_page_title_with_http_error(mock_requests):
    # Setup the mock to simulate a 404 error
    mock_requests.get('http://example.com', status_code=404)

    # Call the crawler function
    title = fetch_page_title('http://example.com')

    # Check how the crawler handles HTTP errors
    assert 'Error' in title, "The crawler did not handle the HTTP error correctly"
