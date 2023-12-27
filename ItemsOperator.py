from typing import Optional, Literal, Dict, Any
from SupportBases import Location, Toward, GameStateConsts, ClockBase, Digit, Map, MoveInfo


class Item:
    def __init__(self) -> None:
        """相关属性"""
        self.visible: bool = True  # 可视的
        self.passable: bool = False  # 可穿过的
        self.movable: bool = False  # 可移动的
        self.pushable: bool = False  # 可推动的
        self.interactive: bool = False  # 可操作的
        self.assailable: bool = False  # 可攻击的
        self.vulnerable: bool = False  # 可伤害的(代表有血条)

        self.blood: Digit= None  # 血条
        self.speed: Digit = None  # 移动速度

        """."""
        self.identifying: Optional[str] = None  # 显示标识

    def __repr__(self) -> str:
        return self.identifying if self.identifying is not None else 'N'


class Person(Item):
    def __init__(self, 
                 game_map: Map, 
                 spawn: Location, 
                 blood: Digit, 
                 speed: Digit, 
                 clock: ClockBase) -> None:
        # 实例定义
        super().__init__()
        self.game_map: Map = game_map
        self.clock: ClockBase = clock
        # 对象属性设置
        self.visible = self.movable = self.assailable = self.vulnerable = True
        self.blood: Digit = blood
        self.speed: Digit = speed  # FIXME: speed不应该是等待时间的逻辑
        # 定义初始化
        self.location: Location = spawn
        self.last_pos_info: MoveInfo = {
            'Location': self.location,
            'Item': self.game_map[self.location]
        }
        self.last_move_time: float = clock.now

    def move(self, toward: Toward) -> None:
        raise NotImplementedError(
            'The method should be override instead of using it.')

    def _real_move(self, new_pos: Location) -> bool:
        cached_last_info: MoveInfo = self.last_pos_info
        self.last_pos_info: MoveInfo = {
            'Location': new_pos,
            'Item': self.game_map[new_pos]
        }

        self.location: Location = new_pos
        return self.game_map.update({
            cached_last_info['Location']: cached_last_info['Item'],
            new_pos: self
        })


class Player(Person):
    def __init__(self, 
                 game_map: Map, 
                 spawn: Location, 
                 blood: Digit, 
                 speed: Digit, 
                 clock: ClockBase) -> None:
        super().__init__(game_map, spawn, blood, speed, clock)
        self.identifying = 'P'

        """断言层"""
        assert isinstance(self.game_map[spawn], Floor), 'spawn point should be Floor'

        """初始生成"""
        self.game_map.update({
            spawn: self
        })

    def move(self, toward: Toward) -> (bool, GameStateConsts):
        now: float = self.clock.now
        # 移动速度判断
        if now - self.last_move_time < self.speed:  # FIXME: 与上面的speed fixme相同问题, 应该一起被修
            return True, GameStateConsts.timeNotReach
        # 基础量
        x, y = self.location
        dx, dy = toward
        except_location: Location = (x + dx, y + dy)
        # 是否在地图内
        if except_location not in self.game_map:
            return True, GameStateConsts.towardError
        new_pos_content: Any = self.game_map[except_location]
        # 游戏内容判断
        # 碰鬼（结束）
        if isinstance(new_pos_content, Ghost):
            return False, GameStateConsts.MeetGhost
        # 出口（胜利）
        elif isinstance(new_pos_content, ExitPoint):
            return False, GameStateConsts.ReachExit
        # 地板（正常移动）
        elif isinstance(new_pos_content, Floor):
            self._real_move(except_location)
            self.last_move_time = now
            return True, GameStateConsts.GameRunning
        # 碰墙（不移动）
        elif isinstance(new_pos_content, Wall):
            return True, GameStateConsts.crashWall


class Ghost(Person):
    def __init__(self, 
                 game_map: Map, 
                 spawn: Location, 
                 blood: Digit, 
                 speed: Digit, 
                 clock: ClockBase) -> None:
        super().__init__(game_map, spawn, blood, speed, clock)
        self.identifying = 'G'

        """断言层"""
        assert isinstance(self.game_map[spawn], Floor), 'spawn point should be Floor'

        """初始生成"""
        self.game_map.update({
            spawn: self
        })

    def move(self, toward: Toward) -> (bool, GameStateConsts):
        now: float = self.clock.now
        # 移动速度判断
        if now - self.last_move_time < self.speed:
            return True, GameStateConsts.timeNotReach
        # 基础量
        x, y = self.location
        dx, dy = toward
        except_location: Location = (x + dx, y + dy)
        # 是否在地图内
        if except_location not in self.game_map:
            return True, GameStateConsts.towardError
        new_pos_content: Any = self.game_map[except_location]
        # 游戏内容判断
        # 碰玩家（结束）
        if isinstance(new_pos_content, Player):
            return False, GameStateConsts.MeetGhost
        # 地板（正常移动）
        elif isinstance(new_pos_content, Floor):
            self._real_move(except_location)
            self.last_move_time = now
            return True, GameStateConsts.GameRunning
        # 碰墙（不移动）
        elif isinstance(new_pos_content, Wall):
            return True, GameStateConsts.crashWall


class Wall(Item):
    def __init__(self) -> None:
        super().__init__()
        self.visible = True


class Floor(Item):
    def __init__(self) -> None:
        super().__init__()
        self.passable = True
        self.identifying = '.'


class ExitPoint(Item):
    def __init__(self) -> None:
        super().__init__()
        self.visible = self.passable = True
        self.identifying = 'E'
