# ***目录***
  * [*代码架构*](#代码架构)
    1. [ItemsOperator.py](#itemsoperatorpy)
    2. [SupportBases.py](#supportbasespy)
    3. [main.py](#mainpy)

  * [*使用示例*](#使用示例)
    1. Map
    2. Player
    3. Ghost
    4. ClockBase
    5. closurer

  * [*实现期望*](#实现期望)
    * [TODO](#todo)

---
## ***代码架构***

### ItemsOperator.py
<details>
    <summary>内容</summary>

  * 基础地图元素类`Items`
      1. 基础属性定义`__init__`
      2. 元素显示方法实现`__repr__`

  * 基础实体类`Person(Items)`
      1. 基础属性定义`__init__`
          - 继承`Item`
          - 包括 ***出生位置`spawn`***, ***血量`blood`***, ***移速`speed`***

      2. 移动方法
          - `_real_move`: 这是移动方法, 不包含移动判断，只进行移动
          - `move`: 移动判断方法, 该方法应该被重载
  
  * 玩家类`Player(Person)`
    1. 基础属性定义`__init__`
        - 继承`Person`

    2. 移动方法
        - `move`: 移动判断方法, 用于判断移动合理性并做出操作

  * 鬼类`Ghost`
    1. 基础属性定义`__init__`
        - 继承`Person`

    2. 移动方法
        - `move`: 移动判断方法, 用于判断移动合理性并做出操作

  * 墙壁类`Wall`
    1. 基础属性定义`__init__`
          - 继承`Item`

  * 地板类`Floor`
    1. 基础属性定义`__init__`
          - 继承`Item`

  * 出口类`ExitPoint`
    1. 基础属性定义`__init__`
          - 继承`Item`

</details>

### SupportBases.py
<details>
    <summary>内容</summary>

  * 游戏状态常量类`GamestateConsts`
      - 包含游戏阶段常量用于传递

  * 地图类`Map`
    1. 基础属性定义`__init__`
        - `arg`: 继承`list`第一个参数
        - `a`: 地图宽
        - `b`: 地图高

    2. 获取魔术方法`__getitem__`
        - 用于获取目标位置的内容
      
    3. 包含魔术方法`__contains__`
        - 用于判断位置是否在地图内
      
    4. 设置魔术方法`__setitem__`
        - 用于设置目标位置的内容
      
    5. 打印魔术方法`__str__`
        - 用于`print`打印地图
    
    6. 更新方法`update`
        - 批量更新地图地板位置内容
    
    7. 判断存在`isExist`
        - 判断地图中是否存在目标元素
    
    8. 判断是否填满某内容`isFullOf`
        - 判断地图是否充满某元素

  * 时钟触发器`ClockBase`
    1. 基础属性定义`__init__`
        - `threadings`: 线程池
        - `strick_time`: 设置触发器检查进程时间
        - `stop`: 设置默认是否直接开始运行
    
        - 继承`threading.Thread`
    
    2. 线程添加`thread_add`
        - 添加线程

    3. 目前相对时间`now`
        - 该方法为属性(`@property`)
        - 返回从***实例化开始***以来的***相对时间***
    
    4. 停止进程`stop`
        - 用于停止运行进程
    
    5. 触发器`trigger`
        - 用于***检查并调用调整***线程池线程
        - 通过`yield`返回进程运行内容
    
    6. 开始运行`run`
        - 调用后进程开始运行
    
    7. 显示魔术方法`__str__`
        - 返回线程内容

  * 闭包器`closurer`
      - 用于闭包函数创造
  
  * 时间速度转化器`speed_time_disposer`
      - 可在时间与速度之间相互转化

</details>


### main.py
<details>
    <summary>内容</summary>

  * 地图创建`create_map`
      - 创建地图
      - `a`: 长
      - `b`: 高

  * 键盘方向映射`keyboard_reflect`
      - 传入 a, b, c, d 其中一个字符以返回移动方向

  * 用户键盘监视器`user_enter_monitor`
      - 监听会***阻断进程！！！***
      - 用户输入后取消阻断并返回用户按下的按键

</details>

---
## ***实现期望***
<details>
    <summary>TODO</summary>

  * `ItemsOperator` -> `Ghost`
      - 实现鬼的视野算法
      - 实现鬼的寻路算法
      - 实现鬼的跟随算法

  * `SupportBases` -> `ClockBase`
      - 实现线程关键参传递
      - 实现线程执行后返回值的接收判断

</details>

---
## ***使用示例***

<details>
    <summary><font size="4">前提</font></summary>

 ```python
 from typing import Tuple
 
 Toward = Location = Tuple[int, int]
 ```
</details>
<br></br>

### 1. ***`Map`***
<details>
    <summary>示例</summary>

  * 创建地图
    ```python
    def create_map(a: int, b: int):
        return SupportBases.Map(
            ([ItemsOperator.Floor() for _ in range(a)] for _ in range(b)), 
            a, b
            )
    
    m = create_map(3, 4)  # 长3高4的地图
    ```

  * 获取内容
    ```python
    location: Location = (0, 1)
    m[location]  # 获取(0, 1)位置的内容
    ```

  * 设置内容
    ```python
    m[location] = ItemsOperator.Player()  # 设置location位置内容为player()
    ```

  * 在地图内
    ```python
    location in m  # location是否在地图范围内 T/F
    ```

  * 打印地图
    ```python
    print(m)
    ```

  * 包含内容
    ```python
    target = ItemsOperator.Floor()
    m.isExist(target)  # 是否存在地板元素 T/F
    ```

  * 充满内容
    ```python
    target = ItemsOperator.Floor()
    m.isFullOf(target)  # 是否全部为地板元素 T/F
    ```
</details>

### 2. ***`closurer`***
<details>
    <summary>示例</summary>
    * 用法
    ```python
    def hello(greeting, *, name):
        print(greeting, name)

    close_package = closurer(hello, 
                             'Missing you like wildfire', 
                             name='Cheng')
    close_package()
    
    # output:
    #    Missing you like wildfire  Cheng 
    ```
</details>

### 3. ***`ClockBase`***
<details>
    <summary>示例</summary>

  * 实例化
    ```python
    c = SupportBases.ClockBase([], 33) # 约30FPS
    """c.thread_add([strick_time, increment_time, threading, pop, kwargs])
    Args:
        strick_time(int): ms, 触发时间
        increment_time(int): ms, 触发后`strick_time`的时间增量
        threading(callable): 运行的函数
        pop(int): 执行次数几次后弹出, 当其 <0 时 不弹出
        kwargs(dict): 关键词传参
    """
    
    # 0ms时触发, 增量1000ms, 线程为`Ghost().move`, 关键参 toward
    c.thread_add([0, 1000, Ghost().move, -1, {'toward': (1, 0)}])
    # 0ms时触发, 增量33ms, 线程为`print(m)`(打印地图), 关键参 无
    c.thread_add([0, 33, closurer(print, m), -1, {}])
    c.start()  # 开始执行
    ...
    raise NotImplemented('你的其他代码实现')
    ...
    c.stop()  # 停止执行
    ```
</details>

### 4. ***`Player`***
<details>
    <summary>示例</summary>

  * 实例化
    ```python
    p = ItemsOperator.Player(map=m, 
                             spawn=(0, 0), 
                             blood=100, 
                             speed=100, 
                             clock=c)
    ```

  * 移动
    ```python
    toward: Toward = (0, 1)
    running, info = p.move(toward)
    # running 代表是否继续进行游戏 T/F
    # info 一般来自`GameStateConsts`类, 额外用于判断的详细信息
    ```
</details>

### 5. ***`Ghost`***
<details>
    <summary>示例</summary>

  * 实例化
    ```python
    g = ItemsOperator.Ghost(map=m, 
                            spawn=(4, 4), 
                            blood=100, 
                            speed=80, 
                            clock=c)
    ```

  * 移动
    ```python
    toward: Toward = (0, 1)
    running, info = g.move(toward)
    # running 代表是否继续进行游戏 T/F
    # info 一般来自GameStateConsts类, 额外用于判断的详细信息
    ```
</details>
