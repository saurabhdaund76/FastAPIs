
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import Annotated 

app = FastAPI()




@app.post("/upload-bytes/")
async def upload_bytes(file: Annotated[bytes, File()]):
    return {"size": len(file)}




@app.post("/upload-file/")
async def upload_file(file: UploadFile):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}


@app.post("/upload-multiple/")
async def upload_files(files: list[UploadFile]):
    return {"filenames": [f.filename for f in files]}



from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": len(contents)
    }



##########file uploadfile and form in the same endoint ####################



from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],              # Raw bytes file
    fileb: Annotated[UploadFile, File()],        # UploadFile for large file
    token: Annotated[str, Form()]                # Additional form field
):
    return {
        "file_size": len(file),                  # Size of the 'file' in memory
        "token": token,                          # The form field
        "fileb_content_type": fileb.content_type # Metadata from UploadFile
    }
