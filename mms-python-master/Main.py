import API
import sys

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

class MazeMapper:
    MazeSize = [API.mazeWidth(), API.mazeHeight()]
    Finish = [
            [int(MazeSize[0] / 2), int(MazeSize[1] / 2)], 
            [int(MazeSize[0] / 2 - 1), int(MazeSize[1] / 2)], 
            [int(MazeSize[0] / 2), int(MazeSize[1] / 2 - 1)],
            [int(MazeSize[0] / 2 - 1), int(MazeSize[1] / 2 - 1)]
        ]
    Map = []
    def MazeSetup():
        for x in range(MazeMapper.MazeSize[1]):
            MazeMapper.Map.append([])
            for y in range(MazeMapper.MazeSize[0]):
                MazeMapper.Map[x].append(15)
        log(MazeMapper.Map)
        API.setText(0, 0, "abc")
        for pos in MazeMapper.Finish:
            API.setColor(pos[0], pos[1], "A")
            API.setText(pos[0], pos[1], "END")

    def Mapper():
        # 0 = No walls
        # 1 = north wall
        # 2 = east wall
        # 4 = south wall
        # 8 = west wall
        # 15 = all wall
        if API.wallLeft():
            WallDirection = Movement.Direction - 1
            if WallDirection < 0:
                WallDirection += 4
        if API.wallFront():
            WallDirection = Movement.Direction
        if API.wallRight():
            WallDirection = Movement.Direction + 1
            if WallDirection > 4:
                WallDirection -= 4
        Walls = 0
        if WallDirection == 0:
            Walls += 1
        elif WallDirection == 1:
            Walls += 2
        elif WallDirection == 2:
            Walls += 4
        elif WallDirection == 3:
            Walls += 8
        MazeMapper.Map[Movement.Position[1]][Movement.Position[0]] = Walls
        log(MazeMapper.Map)

class Movement:
    Compas = ["North", "East", "South", "West"]
    Position = [0, 0]
    Direction = 0
    History = []
    Last = "Still"
    def Forward():
        if tuple(Movement.Position) not in Movement.History:
            API.setColor(Movement.Position[0], Movement.Position[1], "G")
        else:
            API.setColor(Movement.Position[0], Movement.Position[1], "Y")
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
        if Movement.Last == "Left":
            Movement.History.append(tuple(Movement.Position))
        Movement.Last = "Left"

    def Right():
        API.turnRight()
        Movement.Direction = Movement.Direction + 1
        if Movement.Direction > 3:
            Movement.Direction -= 4
        if Movement.Last == "Right":
            Movement.History.append(tuple(Movement.Position))
        Movement.Last = "Right"

def main():
    log("Running...")
    MazeMapper.MazeSetup()
    while True:
        log(f"[{Movement.Position[0] + 1}, {Movement.Position[1] + 1}] [{Movement.Compas[Movement.Direction]}]")
        MazeMapper.Mapper   ()
        if not API.wallLeft():
            Movement.Left()
        while API.wallFront():
            Movement.Right()
        Movement.Forward()

if __name__ == "__main__":
    main()