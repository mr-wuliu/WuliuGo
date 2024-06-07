from goserve.core import GoGame
from typing import List, Dict, Any
import json
from goserve.config import (
    KATAGO_PATH, AYS_CONFIG_PATH,
    MODEL_PATH_DEFAULT, MODEL_PATH_2
)
from goserve.typesys import Operate
from goserve.util import GoTree
from flask import session

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
        # self.games : Dict[str, GoGame] = {}
        self.current_game : GoGame | None = None

    def init_app(self, app):
        """注册服务
        :param Flask app: Flask App对象
        """
        app.gogame_management = self

    def create_game(self, token: str | None=None,
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
        session['game_token'] = token

        # TODO: 初始化一个GoGame对象
        self.current_game = GoGame(sgf=sgf_file)
        return token
    
    def get_current_game(self) -> GoGame:
        """获取当前的用户信息

        :return GoGame: 返回用户棋局
        """
        if not self.current_game:
            raise ValueError("No game found for current session")
        return self.current_game

    def action(self, token:str, opt : dict ) -> Any:
        """动态映射, 将操作转化为对应的game操作

        :param str token: 标识符
        :param dict opt: 包含函数名和参数的字典
        :return Any: 函数执行结果
        """
        game = self.get_current_game()
        func = opt.get("func")
        params = opt.get("params", [])
        if func is None or params is None:
            raise ValueError("func or Params is None")
        
        if isinstance(func, str):
            if hasattr(game, func):
                func = getattr(game, func)
            elif hasattr(game.game, func):
                func = getattr(game.game, func)
            else:
                raise AttributeError(f"{type(game).__name__} object has no attribute '{func}'")
        elif callable(func):
            if hasattr(game, func.__name__):
                func = getattr(game, func.__name)
            elif hasattr(game.game, func.__name__):
                func =getattr(game.game, func)
            else:
                raise AttributeError(f"{type(game).__name__} object has no attribute '{func}'")
        else :
            raise TypeError("func mast be callable object")
        
        return func(*params)
