"""CSV2JSON MCP 客户端示例."""

import asyncio
import json
from fastmcp import Client


async def main():
    """主函数."""
    # 连接到本地 MCP 服务器
    client = Client("http://localhost:8000/mcp")
    
    try:
        async with client:
            # 1. 转换 CSV 文件为 JSON 文件
            print("\n=== 转换 CSV 文件为 JSON 文件 ===")
            convert_result = await client.call_tool("convert_csv_file", {
                "file_path": "example/example.csv",
                "output_file_path": "example/example_output.json",  # 指定输出文件路径
                "delimiter": ",",
                "orient": "records",
                "encoding": "utf-8"
            })
            
            if hasattr(convert_result, 'content') and convert_result.content:
                convert_text = convert_result.content[0].text
                convert_data = json.loads(convert_text)
            else:
                convert_data = convert_result
            
            if convert_data.get("success"):
                print("转换成功:")
                json_file_path = convert_data["json_file_path"]
                print(f"生成的 JSON 文件路径: {json_file_path}")
                
                # 读取并显示生成的 JSON 文件内容
                try:
                    # 处理相对路径：如果路径以 "example/" 开头，则从项目根目录开始
                    import os
                    if json_file_path.startswith("example"):
                        # 从项目根目录开始计算路径
                        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                        absolute_path = os.path.join(project_root, json_file_path)
                    else:
                        absolute_path = os.path.abspath(json_file_path)
                    
                    with open(absolute_path, 'r', encoding='utf-8') as f:
                        json_content = f.read()
                    print("生成的 JSON 文件内容:")
                    print(json_content)
                except Exception as e:
                    print(f"读取 JSON 文件失败: {e}")
            else:
                print(f"转换失败: {convert_data.get('error')}")
            
            # 2. 转换 CSV 字符串为 JSON
            print("\n=== 转换 CSV 字符串为 JSON ===")
            csv_content = """name,age,city,score
Alice,25,Beijing,85.5
Bob,30,Shanghai,92.0
Charlie,28,Guangzhou,78.5"""
            
            string_result = await client.call_tool("convert_csv_string", {
                "csv_content": csv_content,
                "delimiter": ",",
                "orient": "records"
            })
            
            if hasattr(string_result, 'content') and string_result.content:
                string_text = string_result.content[0].text
                string_data = json.loads(string_text)
            else:
                string_data = string_result
            
            if string_data.get("success"):
                print("字符串转换成功:")
                print(string_data["json"])
            else:
                print(f"字符串转换失败: {string_data.get('error')}")
                
    except Exception as e:
        print(f"客户端错误: {e}")


if __name__ == "__main__":
    asyncio.run(main())