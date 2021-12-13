import API
import sys
import json

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
    Path = {}

    def MazeSetup():
        API.setText(0, 0, "abc")
        for pos in MazeMapper.Finish:
            API.setColor(pos[0], pos[1], "A")
            API.setText(pos[0], pos[1], "END")

    def Write_Json(Data):
        with open("Path.json", "w") as f:
            json.dump(Data, f)

    def Mapper():
        Paths = []
        if tuple(Movement.Position) not in Movement.History:
            try:
                Paths.append(Movement.History[-1])
            except IndexError:
                pass
            if not API.wallLeft():
                WallDirection = Movement.Rotation - 1
                if WallDirection < 0:
                    WallDirection += 4
                if WallDirection == 0:
                    Paths.append((Movement.Position[0], Movement.Position[1] + 1))
                elif WallDirection == 1:
                    Paths.append((Movement.Position[0] + 1, Movement.Position[1]))
                elif WallDirection == 2:
                    Paths.append((Movement.Position[0], Movement.Position[1] - 1))
                elif WallDirection == 3:
                    Paths.append((Movement.Position[0] - 1, Movement.Position[1]))
            if not API.wallFront():
                WallDirection = Movement.Rotation
                if WallDirection == 0:
                    Paths.append((Movement.Position[0], Movement.Position[1] + 1))
                elif WallDirection == 1:
                    Paths.append((Movement.Position[0] + 1, Movement.Position[1]))
                elif WallDirection == 2:
                    Paths.append((Movement.Position[0], Movement.Position[1] - 1))
                elif WallDirection == 3:
                    Paths.append((Movement.Position[0] - 1, Movement.Position[1]))
            if not API.wallRight():
                WallDirection = Movement.Rotation + 1
                if WallDirection > 4:
                    WallDirection -= 4
                if WallDirection == 0:
                    Paths.append((Movement.Position[0], Movement.Position[1] + 1))
                elif WallDirection == 1:
                    Paths.append((Movement.Position[0] + 1, Movement.Position[1]))
                elif WallDirection == 2:
                    Paths.append((Movement.Position[0], Movement.Position[1] - 1))
                elif WallDirection == 3:
                    Paths.append((Movement.Position[0] - 1, Movement.Position[1]))
            MazeMapper.Path[str(Movement.Position)] = Paths
            MazeMapper.Write_Json(MazeMapper.Path)
        
class Movement:
    Compas = ["North", "East", "South", "West"]
    Position = [0, 0]
    Rotation = 0
    Direction = "North"
    History = []
    Last = "Still"
    # Movement using rotation
    def Forward():
        if tuple(Movement.Position) not in Movement.History:
            API.setColor(Movement.Position[0], Movement.Position[1], "G")
        else:
            API.setColor(Movement.Position[0], Movement.Position[1], "Y")
        Movement.History.append(tuple(Movement.Position))
        API.moveForward()
        if Movement.Rotation == 0:
            Movement.Position[1] += 1
        elif Movement.Rotation == 1:
            Movement.Position[0] += 1
        elif Movement.Rotation == 2:
            Movement.Position[1] -= 1
        elif Movement.Rotation == 3:
            Movement.Position[0] -= 1
        Movement.Last = "Forward"

    def Left():
        API.turnLeft()
        Movement.Rotation = Movement.Rotation - 1
        if Movement.Rotation < 0:
            Movement.Rotation += 4
        if Movement.Last == "Left":
            Movement.History.append(tuple(Movement.Position))
        Movement.Last = "Left"

    def Right():
        API.turnRight()
        Movement.Rotation = Movement.Rotation + 1
        if Movement.Rotation > 3:
            Movement.Rotation -= 4
        if Movement.Last == "Right":
            Movement.History.append(tuple(Movement.Position))
        Movement.Last = "Right"
    # Movement using directions
    def North():
        if Movement.Direction == "North":
            API.moveForward()
        elif Movement.Direction == "East":
            API.turnLeft()
            API.moveForward()
        elif Movement.Direction == "South":
            API.turnLeft()
            API.turnLeft()
            API.moveForward
        elif Movement.Direction == "West":
            API.turnRight()
            API.moveForward()
        Movement.Direction = "North"
        Movement.Position[1] += 1

    def East():
        if Movement.Direction == "North":
            API.turnRight
            API.moveForward()
        elif Movement.Direction == "East":
            API.moveForward()
        elif Movement.Direction == "South":
            API.turnLeft()
            API.moveForward
        elif Movement.Direction == "West":
            API.turnLeft()
            API.turnLeft()
            API.moveForward()
        Movement.Direction = "East"
        Movement.Position[0] += 1

    def South():
        if Movement.Direction == "North":
            API.turnLeft()
            API.turnLeft()
            API.moveForward()
        elif Movement.Direction == "East":
            API.turnRight()
            API.moveForward()
        elif Movement.Direction == "South":
            API.moveForward
        elif Movement.Direction == "West":
            API.turnLeft()
            API.moveForward()
        Movement.Direction = "South"
        Movement.Position[1] -= 1
        
    def West():
        if Movement.Direction == "North":
            API.turnLeft()
            API.moveForward()
        elif Movement.Direction == "East":
            API.turnLeft()
            API.turnLeft()
            API.moveForward()
        elif Movement.Direction == "South":
            API.turnRight()
            API.moveForward()
        elif Movement.Direction == "West":
            API.moveForward()
        Movement.Direction = "West"
        Movement.Position[0] += 1


def main():
    log("Running...")
    MazeMapper.MazeSetup()
    while True:
        log(f"[{Movement.Position[0]}, {Movement.Position[1]}] [{Movement.Compas[Movement.Rotation]}]")
        MazeMapper.Mapper()
        if not API.wallLeft():
            Movement.Left()
        while API.wallFront():
            Movement.Right()
        Movement.Forward()

if __name__ == "__main__":
    main()