from __future__ import annotations
from typing import Any, Union, Literal, Tuple, List, Dict, Optional

from goserve.config import (
    KATAGO_PATH, AYS_CONFIG_PATH,
    MODEL_PATH_DEFAULT, MODEL_PATH_2
)
from goserve.util import GoTree, GoStatus, GoNode
import numpy as np
from goserve.typesys import (
    Color, Move, Operate, Capturing, Board, Action
)
'''
The module serves a single game session, providing functionalities such as text-to-game and
game-to-text conversion.
'''


class GoGame:
    def __init__(self,
                 katago_path=KATAGO_PATH,
                 ays_config_path=AYS_CONFIG_PATH,
                 model_path_default=MODEL_PATH_DEFAULT,
                 komi:float=6.5,
                 rule:str = 'chinese',
                 sgf:Any=None) -> None:

        self.KATAGO_PATH = katago_path,
        self.AYS_CONFIG_PATH = ays_config_path,
        self.MODEL_PATH = model_path_default
        self.komi : float = komi
        self.rule : str = rule

        if isinstance(sgf, dict):
            self.game = GoTree(sgf)
        self.game = GoTree()

        #TODO: 解析sgf
        if (sgf is not None):
            pass
        

    def move(self):
        pass
    def delete(self):
        pass
    def previous(self):
        pass
    def next(self):
        pass
    def toSGF(self):
        pass
    def toJSON(self):
        pass