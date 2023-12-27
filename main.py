import tempfile
from removebg import replace_background
from fastapi import FastAPI, UploadFile
from pathlib import Path
from fastapi.responses import FileResponse
from io import BytesIO
import shutil
import logging
from fastapi.responses import JSONResponse
from removebg import remove_bg
from PIL import Image
# Configure the logger
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s [%(levelname)s] - %(message)s")

# Create a FastAPI application
app = FastAPI(debug=True, title='Image Editing', summary='This API Provides Access to all Endpoints of Image Editing API')

# Define an endpoint to receive and save the image
@app.post("/remove_background/")
async def remove_background(file: UploadFile):
    try:
        # Create a directory to save the uploaded files if it doesn't exist
        upload_dir = Path("temp")
        upload_dir.mkdir(parents=True, exist_ok=True)
        # Save the uploaded file to the local directory
        with open(upload_dir / file.filename, "wb") as image_file:
            shutil.copyfileobj(file.file, image_file)        
        image=remove_bg(Image.open(upload_dir / file.filename))
        print('bg removed')
        shutil.rmtree('temp',ignore_errors=True)
          # Save the PIL Image as JPEG in a temporary file
        with BytesIO() as temp_buffer:
            image.save(temp_buffer, format="PNG")
            temp_buffer.seek(0)
            
            # Create a temporary file and write the image data to it
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                temp_file.write(temp_buffer.read())
                temp_file_path = temp_file.name
        print('returning')
        return FileResponse(temp_file_path, media_type="image/jpeg", headers={"Content-Disposition": "attachment; filename=removed.png"})

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
    
# Define an endpoint to replace the background
@app.post("/replace_background/")
async def rep_background(file: UploadFile, background: UploadFile):
    try:
        # Create a directory to save the uploaded files if it doesn't exist
        upload_dir = Path("temp")
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Save the uploaded file with the correct name in the local directory
        with open(upload_dir / file.filename, "wb") as image_file:
            shutil.copyfileobj(file.file, image_file)

        # Save the uploaded background file with the correct name in the local directory
        with open(upload_dir / background.filename, "wb") as background_file:
            shutil.copyfileobj(background.file, background_file)

        image = replace_background(upload_dir / file.filename, upload_dir / background.filename)
        print('background replaced')

        # Remove the 'temp' directory
        shutil.rmtree(upload_dir, ignore_errors=True)

        # Save the PIL Image as PNG in a temporary file
        with BytesIO() as temp_buffer:
            image.save(temp_buffer, format="PNG")
            temp_buffer.seek(0)

            # Create a temporary file and write the image data to it
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                temp_file.write(temp_buffer.read())
                temp_file_path = temp_file.name
        print('returning')
        return FileResponse(temp_file_path, media_type="image/jpeg", headers={"Content-Disposition": "attachment; filename=removed_background.png"})

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)
