import scala.util._
import scala.collection.mutable.ArrayBuffer

class Elevator(val floor: Int, val pos: Int, var direction: String = "") {}

class Game(val nbFloors: Int, val width: Int, val nbRounds: Int, val exitFloor: Int, val exitPos: Int, val nbTotalClones: Int, val nbElevators: Int) {
    var elevators: ArrayBuffer[Elevator] = ArrayBuffer()

    def setElevatorsDirection = {
        for(i <- 0 until nbFloors - 1) {
            if(elevators(i).pos > elevators(i + 1).pos) elevators(i+1).direction = "LEFT" else elevators(i+1).direction = "RIGHT"
        }
    }
}

object Player {
    def main(args: Array[String]) {
        val Array(nbfloors, width, nbrounds, exitfloor, exitpos, nbtotalclones, nbadditionalelevators, nbelevators) = for(i <- readLine split " ") yield i.toInt
        var game = new Game(nbfloors, width, nbrounds, exitfloor, exitpos, nbtotalclones, nbelevators)

        for(i <- 0 until nbelevators) {
            val Array(elevatorfloor, elevatorpos) = for(i <- readLine split " ") yield i.toInt
            game.elevators += new Elevator(elevatorfloor, elevatorpos)
        }
        game.elevators += new Elevator(exitfloor, exitpos)

        game.elevators = game.elevators.sortBy(x => x.floor)
        game.setElevatorsDirection

        var firstRun = true
        while(true) {
            val Array(_clonefloor, _clonepos, direction) = readLine split " "
            val clonefloor = _clonefloor.toInt
            val clonepos = _clonepos.toInt

            if(firstRun) {
                if(clonepos < game.elevators(0).pos) game.elevators(0).direction = "RIGHT" else game.elevators(0).direction = "LEFT"
                firstRun = false
            }

            if(clonefloor == -1) println("WAIT")
            else {
                if(direction == game.elevators(clonefloor).direction) println("WAIT") else println("BLOCK")
            }
        }
    }
}
