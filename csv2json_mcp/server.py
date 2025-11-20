"""CSV 到 JSON MCP 服务器."""

import asyncio
from pathlib import Path
from typing import Optional, Dict, Any
import tempfile
import os

from fastmcp import FastMCP

from .converter import CSVConverter, CSVConversionOptions


class CSV2JSONServer:
    """CSV 到 JSON 转换 MCP 服务器."""
    
    def __init__(self, name: str = "CSV2JSON-MCP"):
        self.mcp = FastMCP(name=name)
        self.converter = CSVConverter()
        self._setup_tools()
    
    def _setup_tools(self):
        """设置 MCP 工具."""
        
        @self.mcp.tool
        async def convert_csv_file(
            file_path: str,
            output_file_path: Optional[str] = None,
            delimiter: str = ",",
            encoding: str = "utf-8",
            skip_rows: int = 0,
            header: bool = True,
            orient: str = "records",
            indent: Optional[int] = None
        ) -> Dict[str, Any]:
            """
            将 CSV 文件转换为 JSON 文件。
            
            Args:
                file_path: CSV 文件路径，必须是有效的文件路径
                output_file_path: 输出 JSON 文件路径（可选，默认为 CSV 文件同目录下同名 .json 文件）
                delimiter: CSV 分隔符，默认为逗号(,)，可以是制表符(\t)、分号(;)等
                encoding: 文件编码，默认为 utf-8，支持 gbk、gb2312 等常见编码
                skip_rows: 跳过的行数，默认为 0，用于跳过文件开头的注释或空行
                header: 是否包含表头，默认为 True，如果为 False 则使用列索引作为键名
                orient: JSON 输出格式，默认为 "records"，可选值：
                    - "records": 每行作为一个字典对象的列表
                    - "values": 仅包含值的二维数组
                    - "split": 分开存储列名和数据的格式
                indent: JSON 缩进，默认为 None（紧凑格式），可设置为 2 或 4 等值
                
            Returns:
                包含转换结果的字典，结构为：
                {
                    "success": bool,      # 转换是否成功
                    "json_file_path": str, # 生成的 JSON 文件路径
                    "message": str       # 操作结果消息
                }
                
            Raises:
                FileNotFoundError: 当文件路径不存在时
                ValueError: 当文件格式错误或转换失败时
                Exception: 其他未知错误
            """
            try:
                # 创建转换选项
                options = CSVConversionOptions(
                    delimiter=delimiter,
                    encoding=encoding,
                    skip_rows=skip_rows,
                    header=header,
                    orient=orient,
                    indent=indent
                )
                
                # 执行转换并生成 JSON 文件
                json_file_path = self.converter.convert_csv_to_json_file(
                    file_path, output_file_path, options
                )
                
                return {
                    "success": True,
                    "json_file_path": json_file_path,
                    "message": "CSV 文件转换成功，JSON 文件已生成"
                }
                
            except FileNotFoundError as e:
                return {
                    "success": False,
                    "error": str(e),
                    "message": "文件不存在"
                }
            except ValueError as e:
                return {
                    "success": False,
                    "error": str(e),
                    "message": "转换失败"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "message": "未知错误"
                }
        
        @self.mcp.tool
        async def convert_csv_string(
            csv_content: str,
            delimiter: str = ",",
            skip_rows: int = 0,
            header: bool = True,
            orient: str = "records",
            indent: Optional[int] = None
        ) -> Dict[str, Any]:
            """
            将 CSV 格式的字符串转换为 JSON 格式。
            
            Args:
                csv_content: CSV 格式的字符串内容，必须包含有效的 CSV 数据
                delimiter: CSV 分隔符，默认为逗号(,)，可以是制表符(\t)、分号(;)等
                skip_rows: 跳过的行数，默认为 0，用于跳过字符串开头的注释或空行
                header: 是否包含表头，默认为 True，如果为 False 则使用列索引作为键名
                orient: JSON 输出格式，默认为 "records"，可选值：
                    - "records": 每行作为一个字典对象的列表
                    - "values": 仅包含值的二维数组
                    - "index": 包含索引的字典
                    - "table": 包含 schema 和数据的完整表格格式
                    - "split": 分开存储列名和数据的格式
                indent: JSON 缩进，默认为 None（紧凑格式），可设置为 2 或 4 等值
                
            Returns:
                包含转换结果的字典，结构为：
                {
                    "success": bool,  # 转换是否成功
                    "json": Any,      # 转换后的 JSON 数据
                    "message": str    # 操作结果消息
                }
                
            Raises:
                ValueError: 当字符串格式错误或转换失败时
                Exception: 其他未知错误
            """
            try:
                # 创建转换选项
                options = CSVConversionOptions(
                    delimiter=delimiter,
                    skip_rows=skip_rows,
                    header=header,
                    orient=orient,
                    indent=indent
                )
                
                # 执行转换
                json_result = self.converter.convert_csv_string_to_json(csv_content, options)
                
                return {
                    "success": True,
                    "json": json_result,
                    "message": "CSV 字符串转换成功"
                }
                
            except ValueError as e:
                return {
                    "success": False,
                    "error": str(e),
                    "message": "转换失败"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "message": "未知错误"
                }
        

        

    
    def run(self, transport: str = "stdio", host: str = "localhost", port: int = 8000):
        """
        运行 MCP 服务器。
        
        Args:
            transport: 传输协议 ('stdio' 或 'http')
            host: HTTP 服务器主机名
            port: HTTP 服务器端口
        """
        if transport == "http":
            self.mcp.run(transport="http", host=host, port=port)
        else:
            self.mcp.run()


def main():
    """主函数入口."""
    server = CSV2JSONServer()
    
    # 检查命令行参数
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        print("启动 HTTP 模式的 CSV2JSON MCP 服务器...")
        server.run(transport="http", host="localhost", port=8000)
    else:
        print("启动 stdio 模式的 CSV2JSON MCP 服务器...")
        server.run(transport="stdio")


if __name__ == "__main__":
    main()