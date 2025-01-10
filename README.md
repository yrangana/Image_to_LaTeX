[![Test_API](https://github.com/yrangana/Image_to_LaTeX/actions/workflows/Test_API.yml/badge.svg)](https://github.com/yrangana/Image_to_LaTeX/actions/workflows/Test_API.yml)  [![Docker CI](https://github.com/yrangana/Image_to_LaTeX/actions/workflows/docker-image.yml/badge.svg)](https://github.com/yrangana/Image_to_LaTeX/actions/workflows/docker-image.yml)

# Image_to_LaTeX

A Flask API powered by a locally hosted multimodal LLM (via Ollama) to generate LaTeX code from images of equations, tables, and figures. Supports conference styles like IEEE, ensuring data privacy and flexibility. Ideal for researchers and academics.

## Features

- Multi-Content Support: Extracts LaTeX for equations, tables, and formatted text.
- Preferred Model: Optimized for the multimodal LLM `llava:34b`.
- Fuzzy Matching: Handles variations in LaTeX syntax for robust extraction.
- Conference Styles: Outputs tailored for formats like IEEE.
- Privacy First: No external API calls; processes are hosted locally.
- Extensible: Built on Flask with well-structured, modular code.

## Prerequisites

To use this API, you must either have Ollama installed locally or have access to a running Ollama API host with multimodal LLM support (e.g., `llava:34b`).

1. **Ollama Installed Locally**:
   - Download and install Ollama by following the instructions at https://ollama.com/.
   - Ensure the Ollama service is running and accessible on `http://localhost:11434` (default).

2. **Accessible Ollama API Host**:
   - If you are not running Ollama locally, set the `OLLAMA_API_HOST` environment variable to the accessible API host URL of a running Ollama instance.

   Example:
   ```bash
   OLLAMA_API_HOST=http://<remote-host>:<port>
   ```

## Requirements

Install the dependencies listed in `requirements.txt`:

```bash
python-dotenv==1.0.1  
pylint==3.3.3  
pytest==8.3.4  
black==24.10.0  
Flask==3.1.0  
requests==2.32.3  
pillow==11.1.0  
pytesseract==0.3.13
ollama==0.4.5  
flasgger==0.9.7.1
```

## Installation

1. Clone the repository:  
    ```bash
   git clone https://github.com/yrangana/Image_to_LaTeX.git  
   cd Image_to_LaTeX  
   ```

2. Create and activate a virtual environment:  
    ```bash
   python -m venv venv  
   source venv/bin/activate  (Windows: venv\Scripts\activate)  
    ```

3. Install dependencies:
    ```bash
   pip install -r requirements.txt
   or
   make install
   ``` 

4. Configure environment variables in a `.env` file:  
   ```bash
   API_PORT=5050  
   OLLAMA_API_HOST=http://localhost:11434  
   OLLAMA_MODEL=llava:34b  
   UPLOAD_DIR=/tmp  
   ALLOWED_EXTENSIONS=png,jpg,jpeg 
   ```

## Usage

### Starting the Server

Run the Flask API:
```bash
python app.py
or
make run
```  

### Running Tests

Use the Makefile to run linters and tests:  
```bash
make lint  (Lint the codebase with pylint)  
make test  (Run tests with pytest)  
make clean (Clean up temporary files)  
```

### API Endpoints

1. `/api/generate`:  
   - Method: POST  
   - Description: Generates LaTeX code from an uploaded image.  
   - Parameters:  
     - file: The image file (required).  
     - type: The content type (table, equation, text).  

2. `/api/health`:  
   - Method: GET  
   - Description: Checks the API health status.  

## Makefile Targets

- run: Starts the Flask server.  
- lint: Runs pylint to check code quality.  
- test: Runs tests using pytest.  
- clean: Cleans up temporary files like `.pytest_cache`.  

## Example API Request

```bash
curl -X POST "http://127.0.0.1:5050/api/generate" \  
-H "Content-Type: multipart/form-data" \  
-F "file=@example.png" \  
-F "type=table"
```

## Contributing

1. Fork the repository.  
2. Create a new branch for your feature or bugfix:  
   git checkout -b feature/my-feature  
3. Commit your changes:  
   git commit -m "Add my new feature"  
4. Push the branch:  
   git push origin feature/my-feature  
5. Open a pull request.  

## Acknowledgments

- Framework: Built with Flask and flasgger for API documentation.
- LLM Support: Powered by Ollama for multimodal LaTeX generation.
