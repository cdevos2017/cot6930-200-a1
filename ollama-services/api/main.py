from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
from typing import Optional

app = FastAPI()

class ConversionRequest(BaseModel):
    model_path: str
    output_name: Optional[str] = None

@app.post("/convert")
async def convert_model(request: ConversionRequest):
    try:
        model_path = request.model_path
        model_name = request.output_name or os.path.basename(model_path).replace('/', '-')
        
        cmd = [
            "python3",
            "/llama.cpp/convert.py",
            "--outfile", f"/models/output/{model_name}.gguf",
            "--outtype", "q4_k_m",
            "--model", f"/models/input/{model_path}"
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Conversion failed: {stderr.decode()}"
            )
            
        return {
            "status": "success",
            "input_path": model_path,
            "output_file": f"{model_name}.gguf",
            "message": stdout.decode()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/status")
async def get_status():
    return {"status": "running"}