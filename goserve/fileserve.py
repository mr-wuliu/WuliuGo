import os
import re
import json
from goserve.config import BASE_DIR

class FileServe:
    def __init__(self):
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)

    def save_record(self, file, token: str):
        """
        将文件根据token存储到BASE_DIR中
        :param file: 要存储的文件内容
        :param str token: 文件的标识符
        """
        file_path = os.path.join(BASE_DIR, f"{token}.sgf")
        with open(file_path, 'wb') as f:
            f.write(file.read())

    def load_file(self, token: str):
        """
        根据token从BASE_DIR中加载文件
        :param str token: 文件的标识符
        :return: 文件内容
        """
        file_path = os.path.join(BASE_DIR, f"{token}.sgf")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No file found for token: {token}")
        
        with open(file_path, 'rb') as f:
            sgf_content = f.read().decode('utf-8')
        return self.parse_sgf(sgf_content)


    def parse_sgf(self, sgf_content: str):
        """
        解析 SGF 内容为字典格式，处理分支结构
        :param str sgf_content: SGF 文件内容
        :return: 解析后的文件内容字典
        """
        def parses_node(node : str):
            # 使用正则提取属性
            propreties = {}
            moves = []
            node = node.strip()
            tokens = re.findall(r'([A-Z]+)\[([^\]]*)\]', node)
            for key , value in tokens:
                if key in ['B','W']:
                    moves.append({'move': key, 'position':value})
                else :
                    propreties[key] = value
            return propreties, moves
        def parse_branch(content : str):
            branch = []
            while content:
                if content[0] == ';':
                    enx_idx = min([content.find(c, 1) for c in ';()'] + [len(content)])
                    node, content = content[1 : enx_idx], content[enx_idx]
                    props, moves = parses_node(node)
                elif content[0] == '(':
                    sub_branch, content = parse_branch(content[1:])
                    branch.append({'variation': sub_branch})
                elif content[0] == '(':
                    sub_branch, content = parse_branch(content[1:])
                    branch.append({'variation': sub_branch})
                else:
                    # 未知字符，跳过
                    content = content[1:]
            return branch, content
        # 解析整个SGF文件
        if sgf_content.startswith('('):
            result, _ = parse_branch(sgf_content[1:])
        else:
            result, _ = parse_branch(sgf_content)
        return result
if __name__ == '__main__':
    pass
    # file_path = os.path.join(BASE_DIR, "ABC.sgf")
    # if not os.path.exists(file_path):
    #     raise FileNotFoundError(f"No file found for token: ABC")
    
    # with open(file_path, 'rb') as f:
    #     sgf_content = f.read().decode('utf-8')
    # sgf_content = "(;GM[1](;B[dd];W[qq])(;B[pd];W[dp](;B[qp];W[dq])(;B[dq];W[qp])))"

    # game_data = parse_sgf(sgf_content)
    # json_output = export_to_json(game_data)

    # print(json_output)