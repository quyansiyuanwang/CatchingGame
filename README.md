# CatchingGame


## 简介
  * 这是一个躲避鬼的游戏
  * 通过命令行显示内容

## 游玩操作
  * 运行游戏以***开始游戏***
  * 通过***键盘`WASD`***进行***上左下右移动***

---

## 文件内容代码目录
  * [ItemsOperator.py](#ItemsOperator.py)
  * [SupportBases.py](#SupportBases.py)
  * [main.py](#main.py)


### ItemsOperator.py
  * 基础地图元素类`Items`
      1. 基础属性定义`__init__`
      2. 元素显示方法实现`__repr__`

  * 基础实体类`Person(Items)`
      1. 基础属性定义`__init__`
        - 继承`Item`
        - 包括***出生位置`spawn`***, ***血量`blood`***, ***移速`speed`***
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

### SupportBases.py
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
  
### main.py
  * 地图创建`create_map`
    - 创建地图
    - `a`: 长
    - `b`: 高

  * 键盘方向映射`keyboard_reflect`
    - 传入 a, b, c, d 其中一个字符以返回移动方向

  * 用户键盘监视器`user_enter_monitor`
    - 监听会***阻断进程！！！***
    - 用户输入后取消阻断并返回用户按下的按键
