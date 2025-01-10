from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from werkzeug.utils import secure_filename
import os
import tempfile
from pathlib import Path
import base64
import re
from dotenv import load_dotenv
from ollama import Client

# Load environment variables
load_dotenv()

# Configurable parameters from .env
PORT = int(os.getenv("API_PORT", 5050))
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llava:34b")
UPLOAD_FOLDER = (
    Path(os.getenv("UPLOAD_DIR", tempfile.gettempdir())) / "latex_generator_uploads"
)
ALLOWED_EXTENSIONS = set(os.getenv("ALLOWED_EXTENSIONS", "png,jpg,jpeg").split(","))

app = Flask(__name__)
app.config["SWAGGER"] = {
    "title": "Image to LaTeX API",
    "uiversion": 3,
    "version": "1.0",
    "description": "API for converting images to LaTeX using Ollama",
}
swagger = Swagger(app)


class OllamaLatexGenerator:
    def __init__(self, model=MODEL_NAME):
        self.model = model
        self.client = Client(
            host=os.getenv("OLLAMA_API_HOST", "http://localhost:11434")
        )

    def encode_image(self, image_path):
        """Encode an image file into a base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def clean_latex(self, latex_code, content_type):
        """
        Clean the LaTeX code by removing unnecessary preambles and explanations
        """
        # Extract content within LaTeX code blocks
        latex_pattern = r"```latex(.*?)```"
        match = re.search(latex_pattern, latex_code, re.DOTALL)
        if match:
            latex_code = match.group(1).strip()
        else:
            # Fallback: Look for environments directly if backticks are missing
            environment_patterns = {
                "table": r"\\begin{table}.*?\\end{table}",
                "equation": r"\\begin{equation}.*?\\end{equation}",
                "text": r".*",
            }
            pattern = environment_patterns.get(content_type, r".*")
            match = re.search(pattern, latex_code, re.DOTALL)
            if match:
                latex_code = match.group(0).strip()
            else:
                return "No valid LaTeX content found."

        # Common cleanup for all content types
        latex_code = re.sub(r"\\documentclass.*?\n", "", latex_code, flags=re.DOTALL)
        latex_code = re.sub(r"\\usepackage.*?\n", "", latex_code, flags=re.DOTALL)
        latex_code = re.sub(r"\\begin{document}", "", latex_code)
        latex_code = re.sub(r"\\end{document}", "", latex_code)

        return latex_code.strip()

    def generate_latex(self, image_path, content_type):
        """Generate LaTeX code from the provided image based on content type."""
        if not Path(image_path).is_file():
            raise FileNotFoundError(f"Image file not found: {image_path}")

        base64_image = self.encode_image(image_path)

        prompt = f"""
        Analyze the content in the provided image and generate LaTeX code for the specified type: {content_type}.
        - Ensure the output is in valid LaTeX syntax.
        - Remove document preambles (e.g., \\documentclass, \\usepackage, \\begin{{document}}, \\end{{document}}).
        - Include only the relevant LaTeX environments (e.g., \\begin{{table}}, \\begin{{equation}}).
        - Do not include explanations or additional text outside the LaTeX code block.
        """

        try:
            response = self.client.generate(
                model=self.model, prompt=prompt, images=[base64_image], stream=False
            )

            # Clean the LaTeX code
            cleaned_latex = self.clean_latex(response.response, content_type)
            return cleaned_latex

        except Exception as e:
            raise Exception(f"Failed to generate LaTeX: {str(e)}")


# Create uploads directory if it doesn't exist
UPLOAD_FOLDER.mkdir(exist_ok=True)


def allowed_file(filename):
    """Check if a file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api/generate", methods=["POST"])
@swag_from(
    {
        "tags": ["LaTeX Generation"],
        "summary": "Generate LaTeX from image",
        "parameters": [
            {
                "name": "file",
                "in": "formData",
                "type": "file",
                "required": True,
                "description": "Image file to convert to LaTeX",
            },
            {
                "name": "type",
                "in": "formData",
                "type": "string",
                "enum": ["table", "equation", "text"],
                "required": True,
                "description": "Type of content in the image (table, equation, or text)",
            },
        ],
        "responses": {
            200: {
                "description": "LaTeX code generated successfully",
                "schema": {
                    "type": "object",
                    "properties": {
                        "latex": {"type": "string"},
                        "type": {"type": "string"},
                    },
                },
            },
            400: {"description": "Invalid request"},
            500: {"description": "Internal server error"},
        },
    }
)
def generate_latex():
    """Generate LaTeX code from an uploaded image."""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    content_type = request.form.get("type", "").lower()

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    if content_type not in {"table", "equation", "text"}:
        return jsonify({"error": "Invalid content type"}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = UPLOAD_FOLDER / filename
        file.save(filepath)

        generator = OllamaLatexGenerator()
        latex_code = generator.generate_latex(str(filepath), content_type)

        os.remove(filepath)

        return jsonify({"latex": latex_code, "type": content_type})

    except FileNotFoundError as e:
        return jsonify({"error": f"File error: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


@app.route("/api/health", methods=["GET"])
@swag_from(
    {
        "tags": ["Health"],
        "summary": "Check API health",
        "responses": {
            200: {
                "description": "API is healthy",
                "schema": {
                    "type": "object",
                    "properties": {"status": {"type": "string"}},
                },
            }
        },
    }
)
def health_check():
    """Check the health of the API."""
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)
