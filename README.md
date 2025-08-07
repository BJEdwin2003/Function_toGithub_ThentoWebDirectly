# Mixed Model DOE Analysis - Multi-Platform Deployment

A comprehensive FastAPI-based web service for performing Design of Experiments (DOE) analysis using Mixed Models, optimized for L*a*b color space data analysis.

## 🎯 部署方式概览 (Deployment Options)

本仓库支持多种部署和使用方式：

### 1️⃣ Web Direct Access (当前主要版本)
**直接网页访问，文件上传/下载**
- **Live API**: https://function-togithub-thentowebdirectly.onrender.com
- **测试界面**: [doe_analysis_test_interface.html](./doe_analysis_test_interface.html)
- **特点**: 
  - 直接文件上传
  - 完整控制台输出显示 
  - 文件下载功能
  - 用户友好的网页界面

### 2️⃣ AI Agent Integration (兼容版本)
**AI Foundry/Copilot Studio 集成**
- **Previous API**: https://mixedmodeldoe-v1.onrender.com
- **用途**: AI Agent 调用
- **特点**: 
  - Base64 编码数据传输
  - 标准化 AI Agent 响应格式
  - OpenAPI 规范兼容

### 3️⃣ Local Development 
**本地开发和测试**
```bash
# 安装依赖
pip install -r requirements.txt

# 本地运行
uvicorn app:app --reload

# 访问 API 文档
http://localhost:8000/docs
```

## 🚀 Quick Start (Web Direct)


### 最简单使用方式：
1. 打开测试界面：[doe_analysis_test_interface.html](./doe_analysis_test_interface.html)
2. 上传 CSV 文件
3. 点击"� 运行 DOE 分析"
4. 查看完整分析结果和下载文件

### 或直接 API 调用：
```bash
curl -X POST -F "file=@your_data.csv" \
  https://function-togithub-thentowebdirectly.onrender.com/runDOE
```

## �📡 API Endpoints (所有版本)

### 1️⃣ Web Direct 专用接口

#### `/runDOE` (POST) - 文件上传分析
直接上传 CSV 文件进行分析，返回完整控制台输出。

```bash
curl -X POST -F "file=@data.csv" \
  https://function-togithub-thentowebdirectly.onrender.com/runDOE
```

**响应示例**:
```json
{
  "status": "success",
  "input_file": "./input/data.csv",
  "output_dir": "./outputDOE", 
  "files": ["simplified_logworth.csv", "diagnostics_summary.csv", ...],
  "console_output": "🚀 开始DOE混合模型分析...\n📊 数据文件: ./input/data.csv\n..."
}
```

#### `/files` (GET) - 文件列表
获取所有可下载的分析结果文件。

```bash
curl https://function-togithub-thentowebdirectly.onrender.com/files
```

#### `/download/{filename}` (GET) - 文件下载  
下载指定的分析结果文件。

```bash
curl -O https://function-togithub-thentowebdirectly.onrender.com/download/simplified_logworth.csv
```

### 2️⃣ AI Agent 兼容接口

#### `/runDOEjson` (POST) - JSON + Base64
AI Agent 使用的 Base64 编码数据传输。

```json
{
  "filename": "data.csv",
  "file_b64": "ZHllMSxkeWUyLFRpbWUsVGVtcCxMdmFsdWU..."
}
```

#### `/api/DoeAnalysis` (POST) - AI Foundry 专用 ⭐
AI Foundry/Copilot Studio 集成的标准化接口。

```json
{
  "data": "base64_encoded_csv_data",
  "response_column": "Lvalue,Avalue,Bvalue",
  "threshold": 1.5,
  "force_full_dataset": true
}
```

## 🔧 数据格式要求

您的 CSV 文件应包含以下列：
- `dye1`, `dye2` - 染料浓度
- `Time`, `Temp` - 工艺参数  
- `Lvalue`, `Avalue`, `Bvalue` - 颜色测量值 (响应变量)

示例数据：
```csv
dye1,dye2,Time,Temp,Lvalue,Avalue,Bvalue
1.0,2.0,30,150,45.2,12.3,8.7
1.5,2.5,35,160,47.1,13.1,9.2
2.0,3.0,40,170,49.0,14.2,10.1
```

## 📊 输出文件说明

分析完成后会生成以下文件（可通过 `/download/{filename}` 下载）：

### 主要结果文件：
- `simplified_logworth.csv` - 简化模型的显著因子
- `fullmodel_logworth.csv` - 完整模型结果  
- `uncoded_parameters.csv` - 未编码参数估计
- `diagnostics_summary.csv` - 模型诊断信息

### 诊断文件：
- `mixed_model_variance_summary.csv` - 方差组分分析
- `JMP_style_lof.csv` - 拟合缺失检验
- `residual_data_*.csv` - 各响应变量的残差数据

### 数据文件：
- `design_data.csv` - 设计数据
- `scaler.csv` - 标准化参数
- `console_output.txt` - 完整控制台输出

## 🎨 Web 界面特色功能

### 完整控制台输出显示
网页界面显示与 VS Code 终端完全相同的分析过程：
- 🚀 分析进度提示
- 📊 数据维度和统计信息
- 📋 JMP风格诊断汇总  
- ✅ 文件保存确认

### 文件管理功能
- 📂 浏览生成的文件
- ⬇️ 一键下载分析结果
- 📄 文件预览和说明

## 🤖 AI Agent Integration (Legacy)

### AI Foundry/Copilot Studio 集成说明：
1. 使用 OpenAPI 规范：`openapi_doe_analysis_ai_foundry.json`
2. 端点：`/api/DoeAnalysis`  
3. **重要**：`response_column` 必须是逗号分隔的字符串，不是数组

### AI Foundry 调用示例：
```json
{
  "data": "base64_csv_here", 
  "response_column": "Lvalue,Avalue,Bvalue",
  "threshold": 1.5
}
```

##  开发和部署

### 项目结构
```
├── app.py                                    # 主 API 服务器 (Web Direct)
├── doe_analysis_test_interface.html          # Web 测试界面
├── MixedModelDOE_Function_OutputToWeb_*.py   # 核心分析逻辑
├── requirements.txt                          # 依赖包
├── openapi*.json                            # API 规范 (AI Agent)
└── README.md                                # 本文档
```

### 核心依赖：
- `fastapi` - Web 框架
- `uvicorn` - ASGI 服务器
- `pandas`, `numpy` - 数据处理
- `statsmodels` - 统计建模
- `scikit-learn` - 机器学习工具

### 部署到 Render.com：
1. Fork 本仓库
2. 在 Render.com 创建 Web Service
3. 连接 GitHub 仓库
4. 构建命令：`pip install -r requirements.txt`
5. 启动命令：`uvicorn app:app --host 0.0.0.0 --port $PORT`

## 📈 性能指标

- **分析时间**: 典型数据集 < 60 秒
- **内存使用**: 大部分分析 < 1MB
- **支持数据量**: 最多 10,000 行
- **文件上传限制**: 50MB

## 🔄 版本历史

### v1.1.0 (当前版本) - Web Direct
- ✅ 完整控制台输出捕获和显示
- ✅ 文件下载 API (`/files`, `/download/{filename}`)
- ✅ 用户友好的 Web 测试界面
- ✅ 保持 AI Agent 兼容性

### v1.0.0 - AI Agent 专用
- ✅ AI Foundry/Copilot Studio 集成
- ✅ Base64 数据传输
- ✅ OpenAPI 规范支持

## 🔗 相关资源

- [可行性报告](MixedModelDOE_AI_Agent_Feasibility_Report.md) (AI Agent 版本)
- [English Version](MixedModelDOE_AI_Agent_Feasibility_Report_EN.md)
- [测试界面](./doe_analysis_test_interface.html) (Web Direct 版本)

## 📞 技术支持

如有问题或建议：
1. Web Direct 版本：访问 API 文档 https://function-togithub-thentowebdirectly.onrender.com/docs
2. AI Agent 版本：参考 OpenAPI 规范文件
3. 本地开发：查看 `/docs` 端点

## 💡 使用建议

### 推荐使用场景：

1️⃣ **普通用户** → Web Direct (当前版本)
- 简单文件上传
- 完整结果查看
- 方便文件下载

2️⃣ **AI Agent 开发者** → AI Foundry 接口
- 程序化调用
- 标准化响应
- 自动化集成

3️⃣ **开发者** → Local Development
- 代码调试
- 功能扩展
- 性能优化

---

**当前版本**: v1.1.0 (Web Direct)  
**最后更新**: 2025年8月  
**维护状态**: 🟢 活跃开发中
