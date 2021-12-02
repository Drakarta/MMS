import API
import sys

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

class Movement:
    Compas = ["North", "East", "South", "West"]
    Position = [1, 1]
    Direction = 0
    History = []
    Last = "Still"
    def Forward():
        if tuple(Movement.Position) not in Movement.History:
            API.setColor(Movement.Position[0] - 1, Movement.Position[1] - 1, "G")
        else:
            API.setColor(Movement.Position[0] - 1, Movement.Position[1] - 1, "Y")
        Movement.History.append(tuple(Movement.Position))
        API.moveForward()
        if Movement.Direction == 0:
            Movement.Position[1] += 1
        elif Movement.Direction == 1:
            Movement.Position[0] += 1
        elif Movement.Direction == 2:
            Movement.Position[1] -= 1
        elif Movement.Direction == 3:
            Movement.Position[0] -= 1
        
        Movement.Last = "Forward"

    def Left():
        API.turnLeft()
        Movement.Direction = Movement.Direction - 1
        if Movement.Direction < 0:
            Movement.Direction += 4
        log(Movement.Last)
        if Movement.Last == "Left":
            API.setColor(Movement.Position[0] - 1, Movement.Position[1] - 1, "Y")
        Movement.Last = "Left"

    def Right():
        API.turnRight()
        Movement.Direction = Movement.Direction + 1
        if Movement.Direction > 3:
            Movement.Direction -= 4
        log(Movement.Last)
        if Movement.Last == "Right":
            log(Movement.Position)
            API.setColor(Movement.Position[0] - 1, Movement.Position[1] - 1, "Y")
            log("done")
        Movement.Last = "Right"

def StartnFinish():
    MazeSize = [API.mazeWidth(), API.mazeHeight()]
    finish = [
        [int(MazeSize[0] / 2), int(MazeSize[1] / 2)], 
        [int(MazeSize[0] / 2 - 1), int(MazeSize[1] / 2)], 
        [int(MazeSize[0] / 2), int(MazeSize[1] / 2 - 1)],
        [int(MazeSize[0] / 2 - 1), int(MazeSize[1] / 2 - 1)]
    ]
    API.setText(0, 0, "abc")
    for pos in finish:
        API.setColor(pos[0], pos[1], "A")
        API.setText(pos[0], pos[1], "END")

def main():
    log("Running...")
    StartnFinish()
    while True:
        log(f"{Movement.Position} [{Movement.Compas[Movement.Direction]}]")
        if not API.wallLeft():
            Movement.Left()
        while API.wallFront():
            Movement.Right()
        Movement.Forward()

if __name__ == "__main__":
    main()