# Text Summarization Service

This project is a simple FastAPI application that uses a Hugging Face transformer model to summarize text. It provides a clean and minimal web interface and a well-structured project layout with static files and HTML templates. The application is container-friendly, works well in GitHub Codespaces, and includes a Makefile for common development tasks.

---

## Features

- Summarizes text using a pretrained Hugging Face model.
- FastAPI backend with clean routing.
- Simple, structured HTML frontend using Jinja2 templates.
- Static files served from a dedicated `static/` directory.
- Error handling for short or invalid inputs.
- Makefile for installation, running, testing, linting, and formatting.

---

## Project Structure

```

.
├── app/
│   ├── app.py
│   ├── static/
│   │   ├── style.css
│   │   └── script.js (optional)
│   └── templates/
│       └── index.html
├── Makefile
└── requirements.txt

```

---

## Installation

Create and activate a virtual environment:

```

python -m venv .venv
source .venv/bin/activate

```

Install dependencies:

```

make install

```

If you prefer manual installation:

```

pip install --upgrade pip
pip install -r requirements.txt

```

---

## Running the Application

Start the FastAPI server:

```

make run

```

Or manually:

```

uvicorn app.app:app --reload --host 0.0.0.0 --port 8000

```

Once running, open:

```

[http://127.0.0.1:8000](http://127.0.0.1:8000)

```

---

## Usage

1. Enter any block of text into the provided textarea.
2. Click the "Summarize" button.
3. The server will return a condensed summary using a Hugging Face transformer model.
4. Errors, such as insufficient text, are displayed in the interface.

---

## Development

### Formatting

Format the codebase with Black:

```

make format

```

### Linting

Run pylint checks:

```

make lint

```

### Testing

Run tests (if added):

```

make test

```

---

## Requirements

The project uses the following Python dependencies:

- fastapi
- uvicorn
- transformers
- torch
- jinja2

These are listed in `requirements.txt`.

---

## Notes

- The summarization model used is `sshleifer/distilbart-cnn-12-6`.
- The model is lightweight compared to larger BART variants but still produces effective summaries.
- If running in a constrained environment, consider enabling CPU-only mode or swapping to a smaller model.

---

## License

This project is provided under the MIT License.
```
