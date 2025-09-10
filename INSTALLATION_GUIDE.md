# Cursor 安装指南

## 📥 第一步：下载 Cursor

### **官方下载**
1. 访问：https://cursor.sh/
2. 点击 "Download for Windows"
3. 下载 `.exe` 安装文件

### **备用下载（如果官方站点较慢）**
- **GitHub 发布页面**：https://github.com/getcursor/cursor/releases
- 下载最新的 Windows `.exe` 文件

## 🔧 第二步：安装

### **基本安装**
1. **以管理员身份运行安装程序**
2. **接受许可协议**
3. **选择安装位置**（推荐：`C:\Users\[您的用户名]\AppData\Local\Programs\Cursor`）
4. **选择组件**：
   - ✅ Cursor 编辑器
   - ✅ 桌面快捷方式
   - ✅ 添加到 PATH
5. **点击安装**

### **安装后**
1. **重启计算机**（推荐）
2. **从开始菜单或桌面启动 Cursor**

## ⚙️ 第三步：基本设置（可选）

### **语言设置（可选）**
如果您喜欢中文界面：
1. 打开 Cursor
2. 按 `Ctrl + Shift + P`
3. 输入 "Configure Display Language"
4. 选择 "Chinese (Simplified)"
5. 重启 Cursor

**注意**：此步骤完全可选。如果您愿意，可以继续使用英文界面。

## 🤖 第四步：AI 助手设置

### **首次设置**
1. **登录 Cursor**：
   - **选项 1**：在 AI 聊天界面点击 "Log in" 按钮
   - **选项 2**：转到设置（齿轮图标）→ 登录
   - **选项 3**：在左下角寻找 "Sign In" 按钮
   - 使用您的 GitHub 账户（推荐）
   - 或创建新账户

2. **验证登录成功**：
   - **"Agents" 按钮**应该可用
   - **AI 聊天**应该可以正常工作，不再要求您登录

3. **AI 模型选择**：
   - Cursor 自动使用最佳可用模型
   - 无需额外配置

## 🐍 第五步：Python 环境设置

### **安装 Python**
1. 从 https://www.python.org/downloads/ 下载 Python 3.9+
2. **重要**：安装时勾选 "Add Python to PATH"
3. 验证安装：打开命令提示符，输入 `python --version`

### **安装必需的包**

#### **选项 1：设置清华镜像为默认（推荐）**
**这使清华镜像永久生效 - 您无需再次输入：**

```bash
# 为 pip 设置清华镜像为默认
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/

# 现在您可以正常安装包（在中国更快）
pip install pandas numpy matplotlib plotly streamlit jupyter
```

#### **选项 2：一次性使用（不推荐）**
```bash
# 仅在此次安装中使用清华镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pandas numpy matplotlib plotly streamlit jupyter
```

#### **选项 3：标准安装（在中国最慢）**
```bash
pip install pandas numpy matplotlib plotly streamlit jupyter
```

**为什么选项 1 最好：**
- **设置一次，永久使用** - 无需记住镜像 URL
- **所有未来的 pip 安装**将自动使用清华镜像
- **所有 Python 包的下载速度更快**
- **如需要可轻松改回**：`pip config unset global.index-url`

### **验证安装**
```bash
# 检查包是否正确安装
python -c "import pandas; print('Pandas 版本:', pandas.__version__)"

# 验证您的镜像设置（如果您使用了选项 1）
pip config list
```

### **管理您的镜像设置**
```bash
# 检查当前镜像设置
pip config list

# 改回官方 PyPI（如需要）
pip config unset global.index-url

# 设置不同的镜像（例如，阿里云）
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
```

## 📚 第六步：课程项目设置

### **创建项目文件夹**
1. 创建新文件夹：`C:\Users\[您的用户名]\Desktop\Demo1`
2. 将要分析的文件（例如 'Student Handbook_2025-26 Cohort.pdf'）放入此文件夹
3. 在 Cursor 中打开文件夹：`文件 → 打开文件夹`
4. 尝试："创建一个网页应用来美观地展示 'Student Handbook_2025-26 Cohort' 文档的内容。使用导航、章节和专业样式使其美观。"

### **创建项目文件夹**
1. 创建新文件夹：`C:\Users\[您的用户名]\Desktop\Demo2`
2. 将 `UM_C19_2021.csv` 复制到此文件夹
3. 在 Cursor 中打开文件夹：`文件 → 打开文件夹`

## 🔍 第七步：故障排除

### **中国的常见问题**

#### **下载/安装缓慢**
- 如果可用，使用 VPN
- 尝试在非高峰时段下载
- 使用备用下载源

#### **AI 助手不工作**
- 检查网络连接
- 尝试刷新页面
- 重启 Cursor
- 检查是否已登录

#### **找不到 Python**
- 确保 Python 已添加到 PATH
- 安装后重启命令提示符
- 使用完整路径：`C:\Python39\python.exe`

#### **包安装错误**
- **使用清华镜像进行更快安装：**
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pandas numpy matplotlib plotly streamlit jupyter
```
- **如果 pip 失败，尝试 conda：**
```bash
conda install pandas numpy matplotlib plotly streamlit jupyter
```
- **如果清华镜像较慢，使用备用镜像：**
```bash
# 阿里云镜像
pip install -i https://mirrors.aliyun.com/pypi/simple/ pandas

# 豆瓣镜像  
pip install -i https://pypi.douban.com/simple/ pandas
```

### **性能问题**
- 关闭不必要的浏览器标签页
- 暂时禁用杀毒软件实时扫描
- 如果可用，使用 SSD
- 增加虚拟内存

## ✅ 验证清单

- [ ] Cursor 安装并成功启动
- [ ] 可以登录 Cursor 账户
- [ ] AI 助手响应 `Ctrl + K`
- [ ] Python 已安装并可从命令行访问
- [ ] 必需的包安装成功
- [ ] 可以打开课程项目文件夹
- [ ] AI 生成 CSV 读取代码

## 🆘 获取帮助

### **官方资源**
- **Cursor 文档**：https://cursor.sh/docs
- **Discord 社区**：https://discord.gg/cursor
- **GitHub 问题**：https://github.com/getcursor/cursor/issues

### **课程支持**
- 在课程期间提问
- 使用上面的故障排除部分
- 查看课程材料中的解决方案

## 🎯 下一步

安装完成后：
1. **练习使用 AI 助手**进行简单提示
2. **熟悉 Cursor 界面**
3. **为课程的第二小时做准备**
4. **准备好您的 CSV 文件**进行分析

---

**恭喜！** 您现在已准备好使用 Cursor 学习 AI 驱动的数据分析！🎉

