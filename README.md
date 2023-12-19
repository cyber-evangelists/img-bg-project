# FastAPI for Background Removal

This repository offers a powerful, Python-based FastAPI backend for:

## Background Removal:

 Isolate the main subject of an image by effortlessly removing its background.
Background Replacement: Breathe new life into your images by replacing the removed background with a fresh choice.

## Watermark Removal: 
Eliminate unwanted watermarks, restoring the original cleanness of your images.

### Features 
- Simple and intuitive API: Get started quickly with well-documented endpoints.
- Versatile image format support: Handles popular formats like JPEG and PNG.
- Adapts to background complexity: Removes backgrounds from both simple and challenging scenes.
- Flexible background replacement: Choose from various options to customize your image edits.
- Powerful watermark removal: Detects and removes watermarks with a range of methods.
- Built with FastAPI for performance: Enjoy robust scalability and high throughput.

### Installation Requirements:

- Python 3.7+
- pipenv (recommended)
- OpenCV
- NumPy
- FastAPI

Additional dependencies listed in requirements.txt
`pip install -r requirements.txt`

### Setup:

- Clone the repository: ` git clone https://github.com/your_username/img-bg-project.git `

#### Install dependencies:
- With pipenv: `pipenv install`
- With pip: ` pip install -r requirements.txt`


### Running the API:

Start the FastAPI server:
- With pipenv: pipenv run `uvicorn main:app --reload --port 8000 --host 0.0.0.0`
- With pip: `uvicorn main:app --reload --port 8000 --host 0.0.0.0`


### API Usage:

[Demonstration Video](https://www.loom.com/share/e07e480548f44a999491d31e10b6e9c4)
