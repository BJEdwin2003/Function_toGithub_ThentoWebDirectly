
from fastapi import FastAPI, UploadFile, File, Body
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import base64
import tempfile
import pandas as pd
from MixedModelDOE_Function_OutputToWeb_20250807 import run_mixed_model_doe_with_output

app = FastAPI(
    title="Mixed Model DOE Analysis API",
    description="API for performing Design of Experiments (DOE) analysis using Mixed Models. Analyzes L*a*b color space data with statistical modeling.",
    version="1.1.0"
)

# 添加 CORS 中间件解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名，生产环境建议指定具体域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)

@app.post("/runDOE")
async def run_doe(file: UploadFile = File(None)):
    # 处理未上传文件或空文件名的情况，返回标准 JSON 错误
    if file is None or not hasattr(file, "filename") or not file.filename:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "No file uploaded"}
        )

    # 使用 os.path.basename 清理上传文件名，防止路径穿越攻击
    safe_filename = os.path.basename(file.filename)

    # 设置输入和输出目录（适用于 Windows）
    input_dir = "./input"
    output_dir = "./outputDOE"
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # 构建安全的输入文件路径
    input_path = os.path.join(input_dir, safe_filename)

    # 保存上传的文件
    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"File save failed: {str(e)}"}
        )

    # 调用 DOE 函数
    try:
        console_output = run_mixed_model_doe_with_output(file_path=input_path, output_dir=output_dir)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"DOE analysis failed: {str(e)}"}
        )

    # 返回结果
    return {
        "status": "success",
        "input_file": input_path,
        "output_dir": output_dir,
        "files": os.listdir(output_dir),
        "console_output": console_output  # 🆕 添加控制台输出
    }

@app.get("/runDOE")
async def run_doe_get():
    return {"status": "ready"}


# 🆕 新增：下载生成的文件
@app.get("/download/{filename}")
async def download_file(filename: str):
    """
    下载分析生成的文件
    例如：/download/simplified_logworth.csv
    """
    output_dir = "./outputDOE"
    file_path = os.path.join(output_dir, filename)
    
    if not os.path.exists(file_path):
        return JSONResponse(
            status_code=404,
            content={"status": "error", "message": f"File {filename} not found"}
        )
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

# 🆕 新增：列出所有可下载的文件
@app.get("/files")
async def list_files():
    """
    列出所有可下载的分析结果文件
    """
    output_dir = "./outputDOE"
    if not os.path.exists(output_dir):
        return {"files": [], "message": "No analysis results available. Run DOE analysis first."}
    
    files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
    return {
        "files": files,
        "download_urls": [f"/download/{f}" for f in files],
        "total_files": len(files)
    }


# 新增：支持 JSON body 传 base64 编码的 CSV 内容
from pydantic import BaseModel
from typing import Optional, List

class DOEJsonRequest(BaseModel):
    filename: str
    file_b64: str  # base64 encoded CSV content

# 新增：AI Foundry 兼容的 DOE 分析请求格式
class DoeAnalysisRequest(BaseModel):
    data: str  # base64 encoded CSV data or URL or raw CSV
    response_column: str  # comma-separated string like "Lvalue,Avalue,Bvalue"
    predictors: Optional[str] = None  # comma-separated string, optional
    threshold: Optional[float] = 1.5
    force_full_dataset: Optional[bool] = True

@app.post("/runDOEjson")
async def run_doe_json(request: DOEJsonRequest):
    try:
        # 解码 base64 内容并保存为临时 CSV 文件
        csv_bytes = base64.b64decode(request.file_b64)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            tmp.write(csv_bytes)
            tmp_path = tmp.name
        # 设置输出目录
        output_dir = "./outputDOE"
        os.makedirs(output_dir, exist_ok=True)
        # 调用 DOE 分析
        console_output = run_mixed_model_doe_with_output(file_path=tmp_path, output_dir=output_dir)
        # 返回结果
        return {
            "status": "success",
            "input_file": tmp_path,
            "output_dir": output_dir,
            "files": os.listdir(output_dir),
            "console_output": console_output  # 🆕 添加控制台输出
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"DOE analysis failed: {str(e)}"}
        )


# 新增：AI Foundry 兼容的 DOE 分析接口
@app.post("/api/DoeAnalysis")
async def doe_analysis(request: DoeAnalysisRequest):
    """
    AI Foundry compatible DOE Analysis endpoint.
    Supports flexible data input and configurable response variables.
    """
    try:
        # 处理数据输入 - 支持 base64, URL 或原始 CSV
        if request.data.startswith("http"):
            # URL 输入 - 暂时不支持，返回错误
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "URL data input not supported yet. Please use base64 encoded data."}
            )
        elif "," in request.data and "\n" in request.data:
            # 原始 CSV 数据
            csv_content = request.data.encode('utf-8')
        else:
            # base64 编码数据
            try:
                csv_content = base64.b64decode(request.data)
            except Exception:
                return JSONResponse(
                    status_code=400,
                    content={"status": "error", "message": "Invalid base64 data format"}
                )
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='wb') as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name
        
        # 设置输出目录
        output_dir = "./outputDOE"
        os.makedirs(output_dir, exist_ok=True)
        
        # 调用 DOE 分析
        console_output = run_mixed_model_doe_with_output(file_path=tmp_path, output_dir=output_dir)
        
        # 构建响应格式，兼容 AI Foundry
        response = {
            "status": "success",
            "summary": {
                "response_variables": request.response_column.split(","),
                "threshold": request.threshold,
                "force_full_dataset": request.force_full_dataset,
                "analysis_completed": True
            },
            "input_file": tmp_path,
            "output_dir": output_dir,
            "files": os.listdir(output_dir),
            "console_output": console_output  # 🆕 添加控制台输出
        }
        
        # 清理临时文件
        try:
            os.unlink(tmp_path)
        except:
            pass
            
        return response
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"DOE analysis failed: {str(e)}"}
        )
