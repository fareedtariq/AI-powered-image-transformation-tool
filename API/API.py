# from io import BytesIO
# import torch
# import uvicorn
# from torchvision import transforms
# from inference.Inferencer import Inferencer
# from models.PasticheModel import PasticheModel
# from PIL import Image
# from typing import Optional
# import io
# from fastapi import FastAPI, UploadFile, HTTPException, Form, File
# from fastapi.responses import StreamingResponse
# from fastapi.middleware.cors import CORSMiddleware  

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],  
# )

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# num_styles = 16
# image_size = 512
# model_save_dir = "style16/pastichemodel-FINAL.pth"

# pastiche_model = PasticheModel(num_styles)
# inference = Inferencer(pastiche_model, device, image_size)
# inference.load_model_weights(model_save_dir, device)

# @app.post('/apply-style/')
# async def apply_style(
#     image: UploadFile = File(...),
#     style_1: int = Form(...),
#     style_2: Optional[int] = Form(None),
#     alpha: Optional[float] = Form(None),
# ):
#     try:
#         if alpha is not None and (alpha < 0 or alpha > 1):
#             raise HTTPException(status_code=400, detail="Alpha must be between 0 and 1")

#         img_data = await image.read()
#         img = Image.open(io.BytesIO(img_data)).convert('RGB')

#         output = inference.eval_image(img, style_1, style_2, alpha)

#         output_buffer = BytesIO()
#         output.save(output_buffer, format="PNG")
#         output_buffer.seek(0)

#         return StreamingResponse(output_buffer, media_type="image/png")

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=8001)



from io import BytesIO
import torch
import uvicorn
from torchvision import transforms
from inference.Inferencer import Inferencer
from models.PasticheModel import PasticheModel
from PIL import Image
from typing import Optional
import io
from fastapi import FastAPI, UploadFile, HTTPException, Form, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware  


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

num_styles = 16
image_size = 512
model_save_dir = "style16/pastichemodel-FINAL.pth"

pastiche_model = PasticheModel(num_styles)
inference = Inferencer(pastiche_model, device, image_size)
inference.load_model_weights(model_save_dir, device)


@app.post('/apply-style/')
async def apply_style(
    image: UploadFile = File(...),
    style_1: int = Form(...),
    style_2: Optional[int] = Form(None),
    alpha: Optional[float] = Form(None),
):
    try:
        if alpha is not None and (alpha < 0 or alpha > 1):
            raise HTTPException(status_code=400, detail="Alpha must be between 0 and 1")

        img_data = await image.read()
        img = Image.open(io.BytesIO(img_data)).convert('RGB')

        output = inference.eval_image(img, style_1, style_2, alpha)

        # Convert image to bytes
        output_buffer = BytesIO()
        output.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return StreamingResponse(output_buffer, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)