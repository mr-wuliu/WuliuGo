from typing import List, Dict, Union ,Optional, Any, Literal, Tuple
import numpy as np

# 定义操作
Color = Union[Literal["b"], Literal["w"], Literal["none"]]
Move = Union[Literal["none"], Literal["pass"], Tuple[int,int]]
Capturing = int
Board = np.ndarray
Operate=Tuple[Color, Move]  
Action=Tuple[Operate,Board, Capturing]
