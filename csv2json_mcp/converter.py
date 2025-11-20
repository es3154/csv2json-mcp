"""CSV to JSON 转换器模块（使用标准库实现）."""

import csv
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from io import StringIO
from pydantic import BaseModel, Field


class CSVConversionOptions(BaseModel):
    """CSV 转换选项."""
    
    delimiter: str = Field(default=",", description="CSV 分隔符")
    encoding: str = Field(default="utf-8", description="文件编码")
    skip_rows: int = Field(default=0, description="跳过的行数")
    header: bool = Field(default=True, description="是否包含表头")
    orient: str = Field(default="records", description="JSON 输出格式: 'records', 'values', 'split'")
    indent: Optional[int] = Field(default=None, description="JSON 缩进，None 表示压缩格式")


class CSVConverter:
    """CSV 到 JSON 转换器（使用标准库实现）."""
    
    def __init__(self):
        # 简化支持的格式，移除 pandas 特有的格式
        self.supported_formats = ["records", "values", "split"]
    
    def _read_csv_data(
        self,
        csv_source: Union[str, Path, StringIO],
        options: CSVConversionOptions
    ) -> tuple[List[str], List[List[str]]]:
        """
        读取 CSV 数据并返回列名和数据行。
        
        Args:
            csv_source: CSV 数据源（文件路径或字符串）
            options: 转换选项
            
        Returns:
            (列名列表, 数据行列表)
        """
        # 处理文件路径和字符串输入
        if isinstance(csv_source, (str, Path)):
            with open(csv_source, 'r', encoding=options.encoding) as f:
                reader = csv.reader(f, delimiter=options.delimiter)
                return self._process_csv_reader(reader, options)
        else:
            # 处理字符串输入
            reader = csv.reader(csv_source, delimiter=options.delimiter)
            return self._process_csv_reader(reader, options)
    
    def _process_csv_reader(
        self,
        reader: csv.reader,
        options: CSVConversionOptions
    ) -> tuple[List[str], List[List[str]]]:
        """
        处理 CSV 读取器并返回列名和数据。
        
        Args:
            reader: CSV 读取器
            options: 转换选项
            
        Returns:
            (列名列表, 数据行列表)
        """
        rows = list(reader)
        
        # 跳过指定行数
        if options.skip_rows > 0:
            rows = rows[options.skip_rows:]
        
        if not rows:
            return [], []
        
        # 处理表头
        if options.header:
            headers = rows[0]
            data_rows = rows[1:]
        else:
            # 如果没有表头，生成默认列名
            headers = [f"column_{i}" for i in range(len(rows[0]))]
            data_rows = rows
        
        return headers, data_rows
    
    def _convert_to_json_format(
        self,
        headers: List[str],
        data_rows: List[List[str]],
        options: CSVConversionOptions
    ) -> str:
        """
        将 CSV 数据转换为指定格式的 JSON。
        
        Args:
            headers: 列名列表
            data_rows: 数据行列表
            options: 转换选项
            
        Returns:
            JSON 格式的字符串
        """
        if options.orient == "records":
            # 每行作为一个字典对象
            result = []
            for row in data_rows:
                if len(row) == len(headers):
                    record = {headers[i]: row[i] for i in range(len(headers))}
                    result.append(record)
            
        elif options.orient == "values":
            # 仅包含值的二维数组
            result = data_rows
            
        elif options.orient == "split":
            # 分开存储列名和数据
            result = {
                "columns": headers,
                "data": data_rows
            }
        
        else:
            raise ValueError(f"不支持的 JSON 格式: {options.orient}")
        
        # 转换为 JSON 字符串
        return json.dumps(result, ensure_ascii=False, indent=options.indent)
    
    def convert_csv_to_json(
        self,
        csv_file_path: Union[str, Path],
        options: Optional[CSVConversionOptions] = None
    ) -> str:
        """
        将 CSV 文件转换为 JSON 字符串。
        
        Args:
            csv_file_path: CSV 文件路径
            options: 转换选项
            
        Returns:
            JSON 格式的字符串
            
        Raises:
            FileNotFoundError: 文件不存在
            ValueError: 文件格式错误或选项无效
        """
        if options is None:
            options = CSVConversionOptions()
        
        # 验证文件存在
        csv_path = Path(csv_file_path)
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV 文件不存在: {csv_file_path}")
        
        # 验证 JSON 格式
        if options.orient not in self.supported_formats:
            raise ValueError(f"不支持的 JSON 格式: {options.orient}")
        
        try:
            # 读取 CSV 数据
            headers, data_rows = self._read_csv_data(csv_path, options)
            
            # 转换为 JSON
            return self._convert_to_json_format(headers, data_rows, options)
            
        except csv.Error as e:
            raise ValueError(f"CSV 文件解析错误: {e}")
        except UnicodeDecodeError as e:
            raise ValueError(f"文件编码错误: {e}")
        except Exception as e:
            raise ValueError(f"转换失败: {e}")
    
    def convert_csv_to_json_file(
        self,
        csv_file_path: Union[str, Path],
        output_file_path: Optional[Union[str, Path]] = None,
        options: Optional[CSVConversionOptions] = None
    ) -> str:
        """
        将 CSV 文件转换为 JSON 文件。
        
        Args:
            csv_file_path: CSV 文件路径
            output_file_path: 输出 JSON 文件路径（可选，默认为 CSV 文件同目录下同名 .json 文件）
            options: 转换选项
            
        Returns:
            生成的 JSON 文件路径
            
        Raises:
            FileNotFoundError: 文件不存在
            ValueError: 文件格式错误或选项无效
        """
        if options is None:
            options = CSVConversionOptions()
        
        # 验证文件存在
        csv_path = Path(csv_file_path)
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV 文件不存在: {csv_file_path}")
        
        # 验证 JSON 格式
        if options.orient not in self.supported_formats:
            raise ValueError(f"不支持的 JSON 格式: {options.orient}")
        
        # 生成输出文件路径
        if output_file_path is None:
            # 默认输出路径：同目录下同名 .json 文件
            output_file_path = csv_path.with_suffix('.json')
        else:
            output_file_path = Path(output_file_path)
        
        try:
            # 读取 CSV 数据
            headers, data_rows = self._read_csv_data(csv_path, options)
            
            # 转换为 JSON 对象
            json_data = self._convert_to_json_format(headers, data_rows, options)
            
            # 写入 JSON 文件
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(json_data)
            
            return str(output_file_path)
            
        except csv.Error as e:
            raise ValueError(f"CSV 文件解析错误: {e}")
        except UnicodeDecodeError as e:
            raise ValueError(f"文件编码错误: {e}")
        except Exception as e:
            raise ValueError(f"转换失败: {e}")
    
    def convert_csv_string_to_json(
        self,
        csv_content: str,
        options: Optional[CSVConversionOptions] = None
    ) -> str:
        """
        将 CSV 字符串内容转换为 JSON 字符串。
        
        Args:
            csv_content: CSV 格式的字符串
            options: 转换选项
            
        Returns:
            JSON 格式的字符串
        """
        if options is None:
            options = CSVConversionOptions()
        
        try:
            # 从字符串读取 CSV 数据
            string_io = StringIO(csv_content)
            headers, data_rows = self._read_csv_data(string_io, options)
            
            # 转换为 JSON
            return self._convert_to_json_format(headers, data_rows, options)
            
        except csv.Error as e:
            raise ValueError(f"CSV 内容解析错误: {e}")
        except Exception as e:
            raise ValueError(f"转换失败: {e}")
    
    def get_csv_info(self, csv_file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        获取 CSV 文件的基本信息。
        
        Args:
            csv_file_path: CSV 文件路径
            
        Returns:
            包含文件信息的字典
        """
        csv_path = Path(csv_file_path)
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV 文件不存在: {csv_file_path}")
        
        try:
            # 读取文件基本信息
            file_size = csv_path.stat().st_size
            
            # 读取前几行来检测信息
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                
                # 读取前 10 行进行检测
                rows = []
                for i, row in enumerate(reader):
                    if i >= 10:
                        break
                    rows.append(row)
            
            if not rows:
                return {
                    "file_size": file_size,
                    "row_count": 0,
                    "column_count": 0,
                    "columns": [],
                    "sample_data": [],
                    "file_encoding": "utf-8",
                    "detected_delimiter": ",",
                }
            
            # 检测分隔符（简化版）
            first_line = rows[0] if rows else []
            delimiter = "," if len(first_line) > 1 else ","
            
            # 估算行数（读取文件行数）
            with open(csv_path, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f)
            
            # 生成列名
            if len(rows) > 0:
                headers = rows[0] if len(rows[0]) > 1 else [f"column_{i}" for i in range(len(rows[0]))]
                column_count = len(headers)
                
                # 生成示例数据
                sample_data = []
                for i, row in enumerate(rows[1:4] if len(rows) > 1 else []):
                    if len(row) == len(headers):
                        record = {headers[j]: row[j] for j in range(len(headers))}
                        sample_data.append(record)
            else:
                headers = []
                column_count = 0
                sample_data = []
            
            info = {
                "file_size": file_size,
                "row_count": line_count - 1 if line_count > 1 else line_count,  # 减去表头
                "column_count": column_count,
                "columns": headers,
                "sample_data": sample_data,
                "file_encoding": "utf-8",
                "detected_delimiter": delimiter,
            }
            
            return info
            
        except Exception as e:
            raise ValueError(f"获取 CSV 文件信息失败: {e}")