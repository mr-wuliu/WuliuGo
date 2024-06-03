from goserve.core import GoGame
from typing import List, Dict, Any
import json
from goserve.config import (
    KATAGO_PATH, AYS_CONFIG_PATH,
    MODEL_PATH_DEFAULT, MODEL_PATH_2
)

'''
支持多对局管理
'''

class BaseConfig:
    def __init__(self) -> None:
        self.core_methods = [
            'analysis'
        ]
        self.node_methods = [
            'player_move',
            'move_next',
            'reback',
            'del_current',
            'current_layer_num',
            'swap_node',
        ]
    
class GogameManagement(BaseConfig):
    def __init__(self) -> None:
        super().__init__()
        self.games : Dict[str, GoGame] = {}

    def init_app(self, app):
        """注册服务
        :param Flask app: Flask App对象
        """
        app.gogame_management = self

    def createGame(self, token: str | None=None,
                   katago_path=KATAGO_PATH,
                   ays_config_path=AYS_CONFIG_PATH,
                   model_path_default=MODEL_PATH_DEFAULT,
                   komi:float=6.5,
                   rule = 'chinese') -> str:
        sgf_file = None
        if token is None:
            # TODO: 调用文件服务创建一个sgf文件
            token = 'this_is_token'
            pass
        else :
            #TODO : 调用文件服务加载一个sgf文件
            pass
        # TODO: 初始化一个GoGame对象
        self.games[token] = GoGame()

        return token
    
    def action(self, token:str, opt : dict ) -> Any:
        """动态映射, 将操作转化为对应的game操作

        :param str token: 标识符
        :param dict opt: 包含函数名和参数的字典
        :return Any: 函数执行结果
        """
        if token not in self.games:
            raise ValueError("Game not found")
        game = self.games[token]
        func_name = opt.get("func")
        params = opt.get("params", [])
        if func_name is None or params is None:
            raise ValueError("func_name or params is None")
        if func_name in self.core_methods:
            func = getattr(game, func_name)
        elif func_name in self.node_methods:
            func = getattr(game.game, func_name)
        else:
            raise ArithmeticError(f"{type(game).__name__} object has no attribute '{func_name}'")
        return func(*params)
    