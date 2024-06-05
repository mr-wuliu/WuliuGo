from __future__ import annotations
from typing import List,  Any
from contextlib import contextmanager
import unittest
import copy
from goserve.config import (
    MAX_DLINKLIST_NODE_NUM, MAX_BOARD_SIZE
)
import numpy as np
from goserve.typesys import (
    Color, Move, Operate, Capturing, Board, Action, Tuple
)

class GoStatus:
    def __init__(self, color=None, move=None, board=None, captured=0) -> None:
        self.color : Color  =  'none' if not color else color
        self.move : Move = 'none' if not move else move
        self.board : np.ndarray = np.zeros([19, 19], dtype=int) if board is None else board # 空棋盘
        self.captured : int = 0
class GoNode:
    def __init__(self, value: GoStatus) -> None:
        self.previouse : GoNode | None = None
        self.child : List[GoNode] = []
        self.status = value
        
class GoTree:
    def __init__(self, sgf : Any=None) -> None:
        self.chess : GoNode = GoNode(GoStatus())
        self.current = self.chess
        if sgf is not None:
            self.parse_sgf_dict(sgf=sgf)
            #TODO : 将传来的sgf字典变成GoNode                        

        self.main_prop = {}
    @contextmanager
    def __manage_state(self):
        original_chess = copy.deepcopy(self.chess)
        original_current = copy.deepcopy(self.current)
        try:
            yield
        except Exception as e:
            self.chess = original_chess
            self.current = original_current
            raise e
        
    def player_move(self, opt : Operate | List[Operate]) -> bool :
        try :
            with self.__manage_state():
                if isinstance(opt, list):
                    for action in opt:
                        self.__play_signle_move(action)
                else:
                    self.__play_signle_move(opt)
        except RuntimeError as e:
            print(f"Runtime error: {e}")
            return False
        except ValueError as e:
            print(f"Value error: {e}")
            return False
        except AssertionError:
            print("Assertion error: Invalid move type or pass move not hanled.")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
        return True
    
    def move_next(self, index:int) -> bool:
        """下一步

        :param int index: 选择分支
        :return bool
        """
        if not 0 <= index < len(self.current.child):
            return False
        self.current = self.current.child[index]
        return True

    def reback(self, index : int = 1) -> bool:
        """返回n步"""
        current = copy.deepcopy(self.current)
        for i in range(index):
            if self.current.previouse is not None:
                self.current = self.current.previouse
            else:
                self.current = current
                return False
        return True
    def del_current(self):
        if self.current.status.color == 'none':
            # 空棋盘, 不能再删啦
            return False
        assert self.current.previouse is not None
        parent = self.current.previouse
        del self.current
        self.current = parent
    def current_layer_num(self) -> int :
        if self.current.status.color == 'none':
            return 1
        assert self.current.previouse is not None
        return len(self.current.previouse.child)

    def swap_node(self, itme_i: int, item_j: int) -> bool:
        """交换两个节点的顺序

        :param int itme_i: i
        :param int item_j: j  
        """
        if itme_i == item_j : return True
        pre = self.current.previouse
        if not pre:
            return False
        if not (0 <= itme_i < len(pre.child)  and 0 <= item_j < len(pre.child) ):
            return False    
        pre.child[itme_i], pre.child[item_j] = pre.child[item_j] , pre.child[itme_i]
        return True

    def print_board(self):
        column_labels = "ABCDEFGHJKLMNOPQRST"[:19]  # 跳过"I"
        board_size = 19
        print()
        for y in range(board_size, 0, -1):
            row = f"{y:2d} "  # 保持行号对齐
            for x in range(board_size):
                stone = self.current.status.board[y-1][x]
                match stone:
                    case 0: row += ". "
                    case 1: row += "# "
                    case 2: row += "o "
            print(row)
        # 打印列标签
        print("   " + " ".join(column_labels))
    
    def parse_sgf_dict(self, sgf:dict)->None:
        first :bool = False
        for item in sgf:
            properties = item['properties']
            moves = item['moves']
            for move in moves:
                opt: Operate = ( move["color"] ,( move['position'][0], move['position'][1] ) )
                self.player_move(opt)
            

    def __play_signle_move(self, opt : Operate) -> None:
        if len(self.current.child) > MAX_DLINKLIST_NODE_NUM:
            raise RuntimeError("Reached the max number of items")
        if opt is None: raise ValueError("None input")
        assert opt[0] != "none" and opt[1] != "pass" and opt[1] != 'none'
        # TODO: pass 的情况
        x, y = opt[1]
        if not ( 0 <= x < MAX_BOARD_SIZE and 0 <= y < MAX_BOARD_SIZE):
            raise ValueError("Invalied Move value.")
        # 检查当前局面该处是否落子
        if self.current.status.board[x][y] != 0:
            raise RuntimeError("Have already stone here.")
        # 提子和打劫
        temp_board : Board = np.copy(self.current.status.board)
        temp_board[x][y] = 1 if opt[0] == 'b' else 2
        temp_board ,cap_num = self.__capture_stones(x, y, board=temp_board)
        if temp_board[x][y] == 0:
            # 禁着点
            raise RuntimeError("Forbidden points")
        pre = self.current.previouse
        if pre is not None and pre.status.move == opt and pre.status.captured == 1:
            # 劫争
            raise RuntimeError("Robbery")
        # 合法节点
        new_node = GoNode(GoStatus(opt[0], opt[1],temp_board, cap_num))
        new_node.previouse = self.current
        index = len(self.current.child)
        self.current.child.append(new_node)
        self.current = self.current.child[index]

    def __capture_stones(self, x :int , y :int, board : Board)-> Tuple[Board, Capturing]:
        """提子

        :param int x: x
        :param int y: y
        :param Board board: 未提子的棋盘
        :return Tuple[Board, Capturing]: 返回棋盘和提子数
        """
        opponent = 3 - board[x][y]
        cap_num = 0
        for nx, ny in self.__get_neighbors(x,y):
            if board[nx, ny] == opponent and not self.__has_liberty(nx, ny, board):
                board, capturing = self.__remove_group(nx, ny, board)
                cap_num += capturing
        # 检查自己是否有气
        if not self.__has_liberty(x, y, board):
            board, capturing = self.__remove_group(x, y, board)
        return board,  cap_num

    
    def __get_neighbors(self, x :int, y : int) :
        """获取邻居, 减少计算量"""
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        return [ (x + dx, y+dy) for dx, dy in directions if 0 <= x + dx < MAX_BOARD_SIZE and 0 <= y + dy < MAX_BOARD_SIZE]
    def __has_liberty(self, x:int , y:int, board :Board):
        visited = set()
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add( (cx, cy))
            for nx, ny in self.__get_neighbors(cx, cy):
                if board[nx, ny] == 0:
                    return True
                elif board[nx, ny] == board[cx, cy] :
                    stack.append((nx, ny))
        return False
    
    def __remove_group(self, x: int , y:int, board: Board):
        stack = [(x,y)]
        color = board[x][y]
        captured_stonse = 0
        while stack:
            cx, cy = stack.pop()
            if board[cx][cy] == color:
                board[cx, cy] = 0
                captured_stonse += 1
                for nx, ny in self.__get_neighbors(cx, cy):
                    if board[nx][ny] == color:
                        stack.append((nx, ny))
        return board, captured_stonse


class TestGoGame(unittest.TestCase):
    def test_player_move(self):
        tree = GoTree()
        self.assertTrue(tree.player_move(('b', (3, 3))))
        self.assertEqual(tree.current.status.board[3, 3], 1)

    def test_invalid_move(self):
        tree = GoTree()
        tree._GoTree__play_signle_move(('b', (3, 3)))
        with self.assertRaises(RuntimeError):
            tree._GoTree__play_signle_move(('b', (3, 3)))  # Same move should raise error

    def test_capture_stones(self):
        tree = GoTree()
        tree.player_move(('b', (3, 3)))
        tree.player_move(('w', (2, 3)))
        tree.player_move(('w', (4, 3)))
        tree.player_move(('w', (3, 2)))
        tree.player_move(('w', (3, 4)))
        self.assertEqual(tree.current.status.board[3, 3], 0)  # The black stone should be captured

    def test_get_neighbors(self):
        tree = GoTree()
        neighbors = tree._GoTree__get_neighbors(3, 3)
        expected_neighbors = [(2, 3), (4, 3), (3, 2), (3, 4)]
        self.assertCountEqual(neighbors, expected_neighbors)

    def test_has_liberty(self):
        tree = GoTree()
        tree.player_move(('b', (3, 3)))
        self.assertTrue(tree._GoTree__has_liberty(3, 3, tree.current.status.board))

    def test_no_liberty(self):
        tree = GoTree()
        tree.player_move(('b', (3, 3)))
        tree.player_move(('w', (2, 3)))
        tree.player_move(('w', (4, 3)))
        tree.player_move(('w', (3, 2)))
        tree.player_move(('w', (3, 4)))
        self.assertFalse(tree._GoTree__has_liberty(3, 3, tree.current.status.board))

    def test_remove_group(self):
        tree = GoTree()
        tree.player_move(('b', (3, 3)))
        tree.player_move(('w', (2, 3)))
        tree.player_move(('w', (4, 3)))
        tree.player_move(('w', (3, 2)))
        tree.player_move(('w', (3, 4)))
        board, captured_stones = tree._GoTree__remove_group(3, 3, tree.current.status.board)
        self.assertEqual(board[3, 3], 0)
        self.assertEqual(captured_stones, 1)

    def test_print_board(self):
        tree = GoTree()
        tree.player_move(('b', (3, 3)))
        tree.print_board()

    def test_parse_sgf_dict(self):
        from goserve.fileserve import FileServe
        import os
        from goserve.config import BASE_DIR
        file_path = os.path.join(BASE_DIR, "ABC.sgf")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No file found for token: ABC")
        with open(file_path, "rb") as f:
            sgf_content = f.read().decode("utf-8")
        file = FileServe()
        out = file.parse_sgf(sgf_content=sgf_content)
        tree = GoTree(out)
        print(tree.print_board())

if __name__ == '__main__':
    unittest.main()
