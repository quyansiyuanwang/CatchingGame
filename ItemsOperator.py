from typing import Optional, Literal, Dict, Any
from SupportBases import Location, Toward, GameStateConsts, ClockBase, Digit


class Item:
    def __init__(self):
        """相关属性"""
        self.visible = True  # 可视的
        self.passable = False  # 可穿过的
        self.movable = False  # 可移动的
        self.pushable = False  # 可推动的
        self.interactive = False  # 可操作的
        self.assailable = False  # 可攻击的
        self.vulnerable = False  # 可伤害的(代表有血条)

        self.blood = None  # 血条
        self.speed = None  # 移动速度

        """."""
        self.identifying: Optional[str] = None  # 显示标识

    def __repr__(self):
        return self.identifying


class Person(Item):
    def __init__(self, game_map, spawn: Location, blood: int, speed: int, clock: ClockBase):
        super().__init__()
        self.game_map = game_map
        self.clock = clock

        self.visible = self.movable = self.assailable = self.vulnerable = True
        self.blood = blood
        self.speed = speed

        self.location = spawn
        self.last_pos_info: Dict[Literal['Location', 'Item'], Any] = {
            'Location': self.location,
            'Item': self.game_map[self.location]
        }
        self.last_move_time = clock.now

    def move(self, toward: Toward):
        raise NotImplementedError(
            'The method should be override instead of using it.')

    def _real_move(self, new_pos):
        cached_last_info = self.last_pos_info
        self.last_pos_info = {
            'Location': new_pos,
            'Item': self.game_map[new_pos]
        }

        self.location = new_pos
        return self.game_map.update({
            cached_last_info['Location']: cached_last_info['Item'],
            new_pos: self
        })


class Player(Person):
    def __init__(self, game_map, spawn: Location, blood: int, speed: Digit, clock: ClockBase):
        super().__init__(game_map, spawn, blood, speed, clock)
        self.location = spawn
        self.identifying = 'P'
        self.speed = speed
        """断言层"""
        assert isinstance(self.game_map[spawn], Floor), 'spawn point should be Floor'
        """初始生成"""
        self.game_map.update({
            spawn: self
        })

    def move(self, toward: Toward):
        now = self.clock.now
        # 移动速度判断
        if now - self.last_move_time < self.speed:
            return True, GameStateConsts.timeNotReach
        # 基础量
        x, y = self.location
        dx, dy = toward
        except_location = (x + dx, y + dy)
        self.last_move_time = now
        # 是否在地图内
        if except_location not in self.game_map:
            return True, GameStateConsts.towardError
        new_pos_content = self.game_map[except_location]
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
            return True, GameStateConsts.GameRunning
        # 碰墙（不移动）
        elif isinstance(new_pos_content, Wall):
            return True, GameStateConsts.crashWall


class Ghost(Person):
    def __init__(self, game_map, spawn: Location, blood: int, speed: Digit, clock: ClockBase):
        super().__init__(game_map, spawn, blood, speed, clock)
        self.location = spawn
        self.identifying = 'G'
        self.speed = speed
        """断言层"""
        assert isinstance(self.game_map[spawn], Floor), 'spawn point should be Floor'
        """初始生成"""
        self.game_map.update({
            spawn: self
        })

    def move(self, toward: Toward):
        now = self.clock.now
        # 移动速度判断
        if now - self.last_move_time < self.speed:
            return True, GameStateConsts.timeNotReach
        # 基础量
        x, y = self.location
        dx, dy = toward
        except_location = (x + dx, y + dy)
        self.last_move_time = now
        # 是否在地图内
        if except_location not in self.game_map:
            return True, GameStateConsts.towardError
        new_pos_content = self.game_map[except_location]
        # 游戏内容判断
        # 碰玩家（结束）
        if isinstance(new_pos_content, Player):
            return False, GameStateConsts.MeetGhost
        # 地板（正常移动）
        elif isinstance(new_pos_content, Floor):
            self._real_move(except_location)
            return True, GameStateConsts.GameRunning
        # 碰墙（不移动）
        elif isinstance(new_pos_content, Wall):
            return True, GameStateConsts.crashWall


class Wall(Item):
    def __init__(self):
        super().__init__()
        self.visible = True


class Floor(Item):
    def __init__(self):
        super().__init__()
        self.passable = True
        self.identifying = '.'


class ExitPoint(Item):
    def __init__(self):
        super().__init__()
        self.visible = self.passable = True
        self.identifying = 'E'
