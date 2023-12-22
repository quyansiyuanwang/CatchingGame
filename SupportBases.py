import threading as threadingLib
import time
from typing import Dict, Tuple, Final

from ItemsOperator import Floor

Location = Toward = Tuple[int, int]
Digit = int | float


class GameStateConsts:
    MeetGhost: Final[str] = 'You was caught by ghost'
    ReachExit: Final[str] = 'You Win!'
    GameRunning: Final[str] = 'Meet wall, the game continue'
    crashWall: Final[str] = 'Crash to the Wall'
    towardError: Final[str] = 'Got a location raised error'
    timeNotReach: Final[str] = 'This time should not move'


class Map(list):
    def __init__(self, arg: any, a: int, b: int) -> None:
        """地图初始化

        Args:
            arg (any): 继承list的第一个arg
        """
        # 以下属性不应被修改
        # 基础类全局变量区
        super().__init__(arg)
        self.a = a
        self.b = b

    def __contains__(self, location: Location) -> bool:
        """判断坐标是否位于对象内

        Args:
            location (Location): 需要检测的位置
            
        Returns:
            返回是否在对象内 T/F
        """
        x, y = location
        if (x < 0 or x >= self.b) or (y < 0 or y >= self.a):
            return False
        return True

    def __getitem__(self, __location: Location) -> any:
        x, y = __location
        return super().__getitem__(x)[y]

    def __setitem__(self, __location: Location, __value: any) -> None:
        x, y = __location
        super().__getitem__(x)[y] = __value

    def __str__(self):
        board = '-' * 15 + '\n'
        for line in self:
            for item in line:
                board += item.__repr__() + ' '
            board += '\n'
        return board

    # 相关功能methods
    def update(self, dictionary: Dict[Location, any]) -> bool:
        """使用字典更新地图内容

        Args:
            dictionary (Dict[Location, 'Player']): 
                更新内容的字典，
                键为元组存储坐标，值为更新内容
                example:
                    `{(0, 1): Player()}`

        Returns:
            bool: 是否更新成功 T/F
        """
        for location, player in dictionary.items():
            if isinstance(self[location], Floor):
                return False

            self[location] = player
        return True

    def isFullOf(self, target: any) -> bool:
        """判断地图是否存在非target因素
        warning: 该判断逻辑为逻辑运算符 `=`,非 `is`
        
        Args:
            target (any): 检测的目标内容

        Returns:
            bool: 是否填满`target` T/F
        """
        return not any(any(item != target for item in line) for line in self)

    def isExist(self, target: any) -> bool:
        """判断地图是否存在target因素
        warning: 该判断逻辑为运算 `in`
        
        Args:
            target (any): 检测的目标内容

        Returns:
            bool: 是否存在`target` T/F
        """
        return any(target in line for line in self)


class ClockBase(threadingLib.Thread):
    def __init__(self, threading: list, struck_time: int, stop: bool = False):
        """Clock事件耦合触发器

        Args:
            threading (list): 线程事件
                example: `[[struck_time, increment_time, threading, pop, kwargs], ...]`
                    args:
                        `struck_time`: 触发时间, 当`now`大于该值时触发事件
                        `increment_time`: 时间增量, 当`pop`为`False`时, 更新`struck_time`(`+=`)
                        `threading`: 触发的事件, 请注意并不提供相关参数传递方法, 
                            若有需求请使用闭包函数`closure`
                        `pop`: 触发事件次数, `-1`为无限
            struck_time (int): 下一次触发的时间
        """
        super().__init__()
        self.threading = threading  # 更新线程CallBack
        self.struck_time = struck_time  # 检测更新时间
        self.__stop = stop

        self.relative_start = time.perf_counter() * 1000

    def thread_add(self, thread):
        """thread example:`[struck_time, increment_time, threading, pop, kwargs]`"""
        self.threading.append(thread)

    @property
    def now(self):
        return time.perf_counter() * 1000 - self.relative_start  # 相对时间(ms)

    def stop(self):
        self.__stop = True

    def trigger(self):
        pop_stack = []
        for idx, (struck_time, increment_time, threading, pop, kwargs) in enumerate(self.threading):
            # TODO 
            if self.now > struck_time:
                self.threading[idx][0] += increment_time
                yield threading()

                self.threading[idx][3] -= 1
                if self.threading[idx][3] == 0:
                    pop_stack.append(idx)

            if self.now < struck_time:
                break

        while pop_stack:
            tar_idx = pop_stack.pop()
            self.threading.pop(tar_idx)

        self.threading.sort(key=lambda x: x[0])

        yield not not self.threading, 'Everything is alright'  # -可暂时设为False用于测试

    def run(self):
        # TODO
        while True:
            if self.__stop:
                exit(self.__stop)
            results = self.trigger()

            for result in results:
                if result is not None:
                    res, info = result
                    if not res:
                        return

            time.sleep(self.struck_time // 1000)

    def __str__(self):
        return f'{self.threading}'


def closure_device(func: callable, *args, **kwargs):
    def inclusion():
        return func(*args, **kwargs)

    return inclusion


def speed_time_disposer(value: Digit) -> Digit:
    """速度转等待时间(ms), 等待时间转速度

    Args:
        value (Digit): 等待时间/速度
        
    Returns:
        等待时间/速度 (Digit)
    """
    return 1000 / value


def _test():
    c = ClockBase([], speed_time_disposer(30))
    c.thread_add([0, speed_time_disposer(1), closure_device(print, 'hello'), 5, {}])
    c.start()
    t = 5
    while t > 0:
        print('world')
        time.sleep(1)
        t -= 1
    c.join()


if __name__ == '__main__':
    _test()
