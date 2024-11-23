import pyautogui
from time import sleep
from pushsafer import Client
from dotenv import load_dotenv
import os


def check_screen(img_path):
    """
    Checks if an image exists on the screen.
    
    Args:
        img_path (str): Path to the image to locate on the screen.
        
    Returns:
        bool: True if the image is found, False otherwise.
    """
    try:
        location = pyautogui.locateOnScreen(img_path, grayscale=False, confidence=0.9)
        return location is not None
    except pyautogui.ImageNotFoundException:
        return False


def check_state():
    """
    Checks the current state of the game by matching predefined images.
    
    Returns:
        str: The name of the state if found, otherwise None.
    """
    state_checks = {
        'found': ['imgs/found.png'],
        # Future enhancements can include additional states below:
        # 'qp': ['imgs/big_qp_q.png', 'imgs/small_qp_q.png'],
        # 'arcade': ['imgs/big_arcade_q.png', 'imgs/small_arcade_q.png'],
    }
    for state, img_paths in state_checks.items():
        for img in img_paths:
            if check_screen(img):
                return state
    return None


def notify_game_found(client):
    """
    Sends a notification using PushSafer when the game is found.
    
    Args:
        client (Client): PushSafer client instance.
        
    Returns:
        None
    """
    try:
        response = {'status': 0}
        while response.get('status') != 1:
            response = client.send_message(
                "Overwatch game found.",
                "Game Found!",
                vibration=3,
                priority=1
            )
            print("Notification Response:", response)
            sleep(1)  # To avoid overwhelming the API
    except Exception as e:
        print("Error sending notification:", e)


if __name__ == '__main__':
    load_dotenv()
    pushsafer_key = os.getenv('PUSHSAFER_KEY')

    if not pushsafer_key:
        print("Error: PUSHSAFER_KEY environment variable not set.")
        exit(1)

    client = Client(pushsafer_key)
    print("Game state checker started...")

    while True:
        try:
            state = check_state()
            if state == 'found':
                print("Game state detected: 'found'")
                notify_game_found(client)
                sleep(10)  # Avoid repeated notifications
            else:
                print("No relevant game state detected.")
        except Exception as e:
            print("Error during state checking:", e)
        sleep(1)
