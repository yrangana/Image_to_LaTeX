import pytest
from app import app  # Import the Flask app
from io import BytesIO

@pytest.fixture
def client():
    """Set up the Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json == {'status': 'healthy'}

def test_generate_latex_no_file(client):
    """Test the /api/generate endpoint with no file provided."""
    response = client.post('/api/generate', data={'type': 'table'})
    assert response.status_code == 400
    assert response.json['error'] == 'No file provided'

def test_generate_latex_invalid_file_type(client):
    """Test the /api/generate endpoint with an invalid file type."""
    data = {
        'file': (BytesIO(b'fake data'), 'example.txt'),
        'type': 'table'
    }
    response = client.post('/api/generate', content_type='multipart/form-data', data=data)
    assert response.status_code == 400
    assert response.json['error'] == 'Invalid file type'

def test_generate_latex_missing_type(client):
    """Test the /api/generate endpoint with no type provided."""
    data = {
        'file': (BytesIO(b'fake image data'), 'example.png')
    }
    response = client.post('/api/generate', content_type='multipart/form-data', data=data)
    assert response.status_code == 400
    assert response.json['error'] == 'Invalid content type'

def test_generate_latex_success(client, mocker):
    """Test the /api/generate endpoint with valid inputs."""
    mocker.patch(
        'app.OllamaLatexGenerator.generate_latex',
        return_value='\\begin{table}...\n\\end{table}'
    )

    data = {
        'file': (BytesIO(b'fake image data'), 'example.png'),
        'type': 'table'
    }
    response = client.post('/api/generate', content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    assert response.json['latex'] == '\\begin{table}...\n\\end{table}'
    assert response.json['type'] == 'table'
