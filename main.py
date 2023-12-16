import keyboard
from random import choice
import ItemsOperator
import SupportBases
from SupportBases import speed_time_disposer as sTD
from SupportBases import closurer


def create_map(a: int, b: int):
    return SupportBases.Map(
        ([ItemsOperator.Floor() for _ in range(a)] for _ in range(b)), 
        a, b
        )

def keyboard_reflect(key: str):
    refl = {
        'w': (-1, 0),
        'a': (0, -1),
        's': (1, 0),
        'd': (0, 1)
    }
    
    return refl.get(key, None)

def user_enter_monitor():
    while True:
        try:
            key_event = keyboard.read_event()
            if key_event.event_type == keyboard.KEY_DOWN:
                return key_event.name
        except KeyboardInterrupt:
            pass

def test():
    m = create_map(6, 6)
    c = SupportBases.ClockBase([], sTD(30)) # FPS
    p = ItemsOperator.Player(map=m, spawn=(0, 0), blood=100, speed=100, clock=c)
    g = ItemsOperator.Ghost(map=m, spawn=(4, 4), blood=100, speed=80, clock=c)
    
    def ghost_move():
        x, y = g.location
        res, info = g.move(keyboard_reflect(choice(('a', 'w', 's', 'd'))))
        if not res:
            print(info)
            exit()
        
    c.thread_add([500, 80, ghost_move, -1, {}])
    c.thread_add([0, sTD(30), closurer(print, m), -1, {}])
    c.start()
    
    while True:
        toward = keyboard_reflect(user_enter_monitor())
        if toward is not None:
            running, info = p.move(toward)
            if not running:
                break
        
    c.stop()
    print(info)
    
if __name__ == '__main__':
    test()
