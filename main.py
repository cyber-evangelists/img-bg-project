import tempfile
from removebg import replace_background
from fastapi import FastAPI, UploadFile, Body, Depends,HTTPException
from pathlib import Path
from fastapi.responses import FileResponse
from io import BytesIO
import shutil
import logging
from fastapi.responses import JSONResponse
from removebg import remove_bg
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from objRemove import ObjectRemove
from models.deepFill import Generator
from torchvision.models.detection import maskrcnn_resnet50_fpn, MaskRCNN_ResNet50_FPN_Weights
import os
import cv2
import logging 
import shutil
import tempfile
from pathlib import Path
from fastapi import Query
from PIL import Image
from io import BytesIO
from auth.model import  ApiKeySchema
from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer
from decouple import config


API_KEY=config("apiKey")


# Configure the logger
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s [%(levelname)s] - %(message)s")

# Create a FastAPI application
app = FastAPI(debug=True, title='Image Editing', summary='This API Provides Access to all Endpoints of Image Editing API')

# add middlewares to all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/auth",tags=["user"])
async def user_login(userkey: ApiKeySchema = Body(...)):
    cleaned_apikey = userkey.apikey.strip()
    if cleaned_apikey == API_KEY:
         return signJWT(API_KEY)
    else:
         raise HTTPException(status_code=403, detail="Invalid API Key.")




# Define an endpoint to receive and save the image
@app.post("/remove_background/",dependencies=[Depends(JWTBearer())],tags=['Remove Background'])
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
@app.post("/replace_background/",dependencies=[Depends(JWTBearer())],tags=['Replace Background'])
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


# Load Mask-RCNN model
for f in os.listdir('models'):
    if f.endswith('.pth'):
        deepfill_weights_path = os.path.join('models', f)

weights = MaskRCNN_ResNet50_FPN_Weights.DEFAULT
transforms = weights.transforms()
rcnn = maskrcnn_resnet50_fpn(weights=weights, progress=False)
rcnn = rcnn.eval()
# Load deepfill model
deepfill = Generator(checkpoint=deepfill_weights_path, return_flow=True)
model = ObjectRemove(segmentModel=rcnn,
                rcnn_transforms=transforms,
                inpaintModel=deepfill)


# Load Mask-RCNN model
for f in os.listdir('models'):
    if f.endswith('.pth'):
        deepfill_weights_path = os.path.join('models', f)

weights = MaskRCNN_ResNet50_FPN_Weights.DEFAULT
transforms = weights.transforms()
rcnn = maskrcnn_resnet50_fpn(weights=weights, progress=False)
rcnn = rcnn.eval()
# Load deepfill model
deepfill = Generator(checkpoint=deepfill_weights_path, return_flow=True)
model = ObjectRemove(segmentModel=rcnn,
                rcnn_transforms=transforms,
                inpaintModel=deepfill)

@app.post("/remove_object/",dependencies=[Depends(JWTBearer())],tags=['Remove Object'])
async def rep_background(file: UploadFile,
                        x1: float = Query(..., description="X1-coordinate"),
                        y1: float = Query(..., description="Y1-coordinate"),
                        x2: float = Query(..., description="X2-coordinate"),
                        y2: float = Query(..., description="Y2-coordinate"),
                        width: float = Query(..., description="Width"),
                        height: float = Query(..., description="Height")):
    try:
        # Create a directory to save the uploaded files if it doesn't exist
        upload_dir = Path("temp")
        upload_dir.mkdir(parents=True, exist_ok=True)
        coordinates =[x1,y1,x2,y2,(width,height)]
        # Save the uploaded file with the correct name in the local directory
        image_path = upload_dir / file.filename
        with open(image_path, "wb") as image_file:
            shutil.copyfileobj(file.file, image_file)

        # Run object removal using the absolute path (converted to string)
        output_image = model.run(image_path=str(image_path), coordinates=coordinates)
        # img = cv2.cvtColor(model.image_orig[0].permute(1,2,0).numpy(),cv2.COLOR_RGB2BGR)
# Save the NumPy array as an image using OpenCV
        temp_file_path = str(upload_dir / "removed_background.png")
        cv2.imwrite(temp_file_path, cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR))
        # Assuming 'img' is your NumPy array
        pil_image = Image.fromarray(output_image)

        # Remove the 'temp' directory
        shutil.rmtree(upload_dir, ignore_errors=True)

        # Save the PIL Image as PNG in a temporary file
        with BytesIO() as temp_buffer:
            pil_image.save(temp_buffer, format="PNG")
            temp_buffer.seek(0)

            # Create a temporary file and write the image data to it
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                temp_file.write(temp_buffer.read())
                temp_file_path = temp_file.name

        print('returning')
        return FileResponse(temp_file_path, media_type="image/jpeg", headers={"Content-Disposition": "attachment; filename=removed_object.png"})

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)