# CSV2JSON MCP 服务器

一个基于 FastMCP 的 CSV 到 JSON 转换 MCP (Model Context Protocol) 服务器，提供高效的 CSV 数据转换服务。

## 功能特性

- ✅ **CSV 文件转 JSON 文件** - 将 CSV 文件转换为 JSON 文件格式
- ✅ **CSV 字符串转 JSON** - 将 CSV 格式的字符串转换为 JSON 数据
- 🚀 **高性能转换** - 基于 pandas 的高效数据处理
- 🔧 **灵活配置** - 支持多种分隔符、编码格式和 JSON 输出格式
- 📚 **MCP 协议** - 符合 Model Context Protocol 标准

## 快速开始

### 环境要求

- Python 3.11+


## MCP 服务器配置


### mcp server 配置

```json
 {
  "mcpServers": {
   "csv2json": {
      "command": "uvx",
      "args": ["csv2json-mcp"],
      "type": "stdio"
    } 
  }
}
```





### 可用工具

#### 1. convert_csv_file

将 CSV 文件转换为 JSON 文件。

**参数：**
- `file_path` (str): CSV 文件路径
- `output_file_path` (str, 可选): 输出 JSON 文件路径，默认为 CSV 文件同目录下的 `.json` 文件
- `delimiter` (str, 可选): CSV 分隔符，默认为 `,`
- `orient` (str, 可选): JSON 输出格式，默认为 `"records"`
- `encoding` (str, 可选): 文件编码，默认为 `"utf-8"`

**返回值：**
```json
{
    "success": true,
    "json_file_path": "path/to/output.json",
    "message": "转换成功"
}
```

#### 2. convert_csv_string

将 CSV 格式的字符串转换为 JSON 数据。

**参数：**
- `csv_content` (str): CSV 格式的字符串内容
- `delimiter` (str, 可选): CSV 分隔符，默认为 `,`
- `skip_rows` (int, 可选): 跳过的行数，默认为 0
- `header` (bool, 可选): 是否包含表头，默认为 true
- `orient` (str, 可选): JSON 输出格式，默认为 `"records"`
- `indent` (int, 可选): JSON 缩进，默认为 None

**返回值：**
```json
{
    "success": true,
    "json": [/* JSON 数据 */],
    "message": "CSV 字符串转换成功"
}
```

### JSON 输出格式

支持以下 JSON 输出格式：

- `"records"`: 每行作为一个字典对象的列表（默认）
- `"values"`: 仅包含值的二维数组
- `"index"`: 包含索引的字典
- `"table"`: 包含 schema 和数据的完整表格格式
- `"split"`: 分开存储列名和数据的格式


## 项目结构

```
csv2json-mcp/
├── csv2json_mcp/          # 核心包
│   ├── __init__.py        # 包初始化
│   ├── converter.py       # 转换器实现
│   └── server.py          # MCP 服务器
├── example/               # 示例文件
│   ├── example.csv        # 示例 CSV 文件
│   ├── example_client.py  # 客户端示例
│   └── example_output.json # 输出示例
├── pyproject.toml         # 项目配置
└── README.md             # 项目文档
```



## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进项目。

## 联系方式

如有问题，请通过以下方式联系：
- 项目仓库：https://github.com/es3154/csv2json-mcp
- 邮箱：893928676@qq.com