# Copilot Agent 设置指南 - DOE 分析集成

## 🎯 概述

本指南将帮助您创建一个专门的 Copilot Agent 来分析 DOE 结果，实现**方案 3.2：带参数跳转到 Copilot Agent**。

## 📋 Step 1: 创建 Copilot Agent

### 1.1 访问 Copilot Studio
1. 打开浏览器，访问：https://copilotstudio.microsoft.com
2. 使用您的 Microsoft 365 账户登录
3. 选择合适的环境（如果有多个）

### 1.2 创建新的 Copilot
1. 点击 **"Create"** → **"New copilot"**
2. 选择 **"From blank"**
3. 填写基本信息：
   - **Name**: `DOE Analysis Expert`
   - **Description**: `专门分析 Design of Experiments 统计结果的 AI 助手`
   - **Language**: 选择中文或英文
   - **Solution**: 选择默认解决方案

## 🔧 Step 2: 配置 Agent 知识和能力

### 2.1 设置 Agent 指令
在 **"Instructions"** 部分添加：

```
你是一个专业的 DOE (Design of Experiments) 分析专家，具有以下专业知识：
- 混合模型 (Mixed Models) 统计分析
- LogWorth 值解读和显著性检验
- L*a*b 色彩空间分析
- JMP 风格的统计报告解读
- 工艺优化建议

当用户提供 DOE 分析结果时，请按以下格式提供分析：
📊 模型效应显著性总结
📐 模型拟合统计 
🧠 关键洞察
💡 工艺优化建议
```

### 2.2 添加知识源（可选）
- 上传相关的 DOE 分析文档
- 添加统计学参考资料
- 包含工艺优化最佳实践

## 🔌 Step 3: 配置 Action（关键步骤）

### 3.1 创建 Action
1. 在 Copilot 编辑器中，点击 **"Actions"** → **"Add an action"**
2. 选择 **"From OpenAPI spec"**

### 3.2 添加 OpenAPI 规范
复制以下 OpenAPI 规范：

```yaml
openapi: 3.0.0
info:
  title: DOE Analysis API
  description: API for retrieving DOE analysis results
  version: 1.0.0
servers:
  - url: https://function-togithub-thentowebdirectly.onrender.com
    description: DOE Analysis Server
paths:
  /get_analysis_for_copilot:
    get:
      summary: Get DOE analysis results for Copilot
      description: Retrieves stored DOE analysis results by analysis ID
      operationId: getDOEAnalysis
      parameters:
        - name: analysis_id
          in: query
          required: true
          schema:
            type: string
          description: The unique identifier for the analysis
      responses:
        '200':
          description: Analysis results retrieved successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "success"
                  analysis_id:
                    type: string
                  analysis_text:
                    type: string
                    description: Full console output of the DOE analysis
                  summary:
                    type: object
                    properties:
                      model_found:
                        type: boolean
                      logworth_analysis:
                        type: boolean
                      r_squared:
                        type: number
                      significant_effects:
                        type: array
                        items:
                          type: string
                  timestamp:
                    type: string
                  files_available:
                    type: array
                    items:
                      type: string
                  download_base_url:
                    type: string
                  ai_prompt_suggestion:
                    type: string
        '404':
          description: Analysis not found
        '400':
          description: Bad request
```

### 3.3 保存并测试 Action
1. 点击 **"Save"** 保存 Action
2. 测试 Action 是否正常工作

## 🌐 Step 4: 获取 Agent URL

### 4.1 获取 Agent 链接
创建完成后，您可以通过以下方式获取 Agent URL：

1. **Canvas URL（推荐）**：
   - 在 Copilot Studio 中，复制浏览器地址栏的 URL
   - 格式类似：`https://copilotstudio.microsoft.com/environments/[env-id]/bots/[bot-id]/canvas`

2. **Web Chat URL**：
   - 点击 **"Publish"** → **"Demo website"**
   - 获取嵌入代码中的 URL

### 4.2 配置 DOE Interface
将获取的 URL 添加到 `doe_analysis_test_interface.html` 中：

```javascript
const COPILOT_AGENT_CONFIG = {
    // 替换为您实际的 Copilot Agent URL
    agentUrl: 'https://copilotstudio.microsoft.com/environments/YOUR-ENV-ID/bots/YOUR-BOT-ID/canvas'
};
```

## 🧪 Step 5: 测试集成

### 5.1 完整测试流程
1. 在 DOE Interface 中上传 CSV 文件并运行分析
2. 点击 **"🤖 Ask My Copilot Agent"** 按钮
3. 确认跳转到 Copilot Agent
4. 在 Agent 中说：**"请分析我的 DOE 结果，分析 ID 是 [显示的ID]"**
5. 验证 Agent 是否成功调用 API 并返回分析结果

### 5.2 故障排除
- **Agent 无法调用 API**：检查 Action 配置和 OpenAPI 规范
- **URL 无法访问**：确认 Copilot Agent 已发布且有访问权限
- **分析 ID 无效**：检查分析是否成功存储到后端

## 📝 Step 6: 自定义和优化

### 6.1 自定义 Agent 响应
可以进一步训练 Agent：
- 添加更多 DOE 相关的示例对话
- 优化分析格式和建议模板
- 集成更多统计学知识

### 6.2 安全考虑
- 确保 API 访问权限合适
- 考虑添加用户身份验证
- 定期清理存储的分析数据

## 🎉 完成！

现在您的 DOE 分析系统已经成功集成了 Copilot Agent，用户可以：

1. ✅ 在 DOE Interface 中完成统计分析
2. ✅ 一键跳转到专门的 Copilot Agent
3. ✅ 自动传递分析结果进行智能解读
4. ✅ 获得专业的工艺优化建议

这实现了**零开发者费用**的 AI 集成方案，充分利用了用户现有的 Microsoft 365 订阅！
