import pyautogui
from time import sleep

def check_screen(img_path):
    '''checking the screen against an image in a set path'''
    try:
        pyautogui.locateOnScreen(img_path, grayscale=False, confidence=0.9)
    except pyautogui.ImageNotFoundException:
        return False
    return True

def check_state():
    '''checking the state of the game'''
    state_checks = {
        'qp': ['imgs/big_qp_q.png', 'imgs/small_qp_q.png'],
        'arcade': ['imgs/big_arcade_q.png', 'imgs/small_arcade_q.png'],
    }
    for state, imgs in state_checks.items():
        for img in imgs:
            if check_screen(img):
                return state
    return None

if __name__ == '__main__':
    while True:
        print(check_state())
        sleep(1)