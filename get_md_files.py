import os
import pathlib
import yaml

def get_md_files(directory):
    """
    获取指定目录下所有.md文件的路径
    
    Args:
        directory (str): 要搜索的目录路径
    
    Returns:
        list: 包含所有.md文件路径的列表
    """
    md_files = []
    
    # 遍历目录及其子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                # 构建完整路径并添加到列表中
                full_path = os.path.join(root, file)
                md_files.append(full_path)
    
    return md_files

def build_nav_structure(md_files):
    """
    根据文件路径构建导航结构，按照目录命名分类
    
    Args:
        md_files (list): Markdown文件路径列表
    
    Returns:
        list: 符合mkdocs nav格式的结构
    """
    # 构建嵌套字典结构
    nav_tree = {}
    
    for md_file in md_files:
        # 移除路径前缀 'docs/'
        relative_path = md_file.replace('\\', '/').replace('docs/', '', 1)
        path_parts = relative_path.split('/')
        
        # 获取文件名（不带扩展名）作为标题
        filename = path_parts[-1].replace('.md', '')
        
        # 构建嵌套结构
        current_level = nav_tree
        for i, part in enumerate(path_parts):
            if i == len(path_parts) - 1:  # 最后一项是文件
                current_level[filename] = relative_path
            else:  # 目录层级
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
    
    # 转换为mkdocs nav格式
    return convert_to_nav_format(nav_tree)

def convert_to_nav_format(nav_tree):
    """
    将嵌套字典转换为mkdocs nav格式
    
    Args:
        nav_tree (dict): 嵌套字典结构
    
    Returns:
        list: mkdocs nav格式列表
    """
    nav_list = []
    
    for key, value in nav_tree.items():
        if isinstance(value, dict):
            # 递归处理子级
            nav_list.append({key: convert_to_nav_format(value)})
        else:
            # 叶子节点（文件）
            nav_list.append({key: value})
    
    return nav_list

def print_nav_structure(nav_list, indent=0):
    """
    格式化打印导航结构
    
    Args:
        nav_list (list): nav结构列表
        indent (int): 缩进级别
    """
    prefix = "  " * indent
    
    for item in nav_list:
        if isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, list):
                    print(f"{prefix}- {key}:")
                    print_nav_structure(value, indent + 1)
                else:
                    print(f"{prefix}- {key}: {value}")

def main():
    # 获取docs目录下的所有md文件
    docs_dir = 'docs'
    if os.path.exists(docs_dir):
        md_files = get_md_files(docs_dir)
        
        print(f"在 {docs_dir} 目录下找到 {len(md_files)} 个 Markdown 文件:")
        print("-" * 50)
        
        # 构建导航结构
        nav_structure = build_nav_structure(md_files)
        
        # 打印导航结构
        print("生成的导航结构:")
        print_nav_structure(nav_structure)
        
    else:
        print(f"目录 {docs_dir} 不存在")

if __name__ == "__main__":
    main()