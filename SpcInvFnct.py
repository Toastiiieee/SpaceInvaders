
class PlayerMovement:
    def __init__(self):
        self.playerMoveDown = False
        self.playerMoveUp = False
        self.playerMoveRight = False
        self.playerMoveLeft = False
        self.shooting = False
        self.escapePressed = False

    def keyboardDown(self, event=None):
        if event is not None:
            if event.char.lower() == 'a':
                self.playerMoveLeft = True
            if event.char.lower() == 'd':
                self.playerMoveRight = True
            if event.char.lower() == 'w':
                self.playerMoveUp = True
            if event.char.lower() == 's':
                self.playerMoveDown = True
            if event.char == ' ':
                self.shooting = True
            if event.keysym == 'Escape':
                self.escapePressed = True

    def keyboardUp(self, event=None):
        if event is not None:
            if event.char.lower() == 'a':
                self.playerMoveLeft = False
            if event.char.lower() == 'd':
                self.playerMoveRight = False
            if event.char.lower() == 'w':
                self.playerMoveUp = False
            if event.char.lower() == 's':
                self.playerMoveDown = False
            if event.char == ' ':
                self.shooting = False
            if event.keysym == 'Escape':
                self.escapePressed = False

    def mouse_is_up(self, event=None):
        self.shooting = False

    def mouse_is_down(self, event=None):
        self.shooting = True

def spawn_enemy(canvas, x, y):
    canvas.create_rectangle(x, y, x + 40, y - 40)  # body
    canvas.create_line(x + 10, y - 30, x + 10, y - 20)  # left eye
    canvas.create_line(x + 8, y - 32, x + 13, y - 27)  # left eyebrow
    canvas.create_line(x + 30, y - 30, x + 30, y - 20)  # right eye
    canvas.create_line(x + 32, y - 32, x + 27, y - 27)  # right eyebrow
    canvas.create_line(x + 15, y - 15, x + 26, y - 15)  # mouth
