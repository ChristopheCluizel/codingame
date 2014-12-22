import math._
import scala.util._
import scala.collection.mutable.ArrayBuffer

class Elevator(val floor: Int, val pos: Int) {
    var direction: String = ""

    override def toString: String = "NumFloor : " + floor + ", pos : " + pos + ", direction : " + direction + "\n"
}

class Game(val nbFloors: Int, val width: Int, val nbRounds: Int, val exitFloor: Int, val exitPos: Int, val nbTotalClones: Int, val nbElevators: Int) {
    var elevators: ArrayBuffer[Elevator] = ArrayBuffer()

    def setElevatorsDirection = {
        for(i <- 0 until nbFloors - 1) {
            if(elevators(i).pos > elevators(i + 1).pos) elevators(i+1).direction = "LEFT" else elevators(i+1).direction = "RIGHT"
        }
        toString
    }

    override def toString: String = {
        var description = ""
        for(i <- elevators){
            description += i.toString
        }
        description
    }
}

object Player {

    def main(args: Array[String]) {
        // nbfloors: number of floors
        // width: width of the area
        // nbrounds: maximum number of rounds
        // exitfloor: floor on which the exit is found
        // exitpos: position of the exit on its floor
        // nbtotalclones: number of generated clones
        // nbadditionalelevators: ignore (always zero)
        // nbelevators: number of elevators
        val Array(nbfloors, width, nbrounds, exitfloor, exitpos, nbtotalclones, nbadditionalelevators, nbelevators) = for(i <- readLine split " ") yield i.toInt
        var game = new Game(nbfloors, width, nbrounds, exitfloor, exitpos, nbtotalclones, nbelevators)

        for(i <- 0 until nbelevators) {
            // elevatorfloor: floor on which this elevator is found
            // elevatorpos: position of the elevator on its floor
            val Array(elevatorfloor, elevatorpos) = for(i <- readLine split " ") yield i.toInt
            game.elevators += new Elevator(elevatorfloor, elevatorpos)
        }
        game.elevators += new Elevator(exitfloor, exitpos)

        game.elevators = game.elevators.sortBy(x => x.floor)
        game.setElevatorsDirection

        var firstRun = true
        // game loop
        while(true) {
            // clonefloor: floor of the leading clone
            // clonepos: position of the leading clone on its floor
            // direction: direction of the leading clone: LEFT or RIGHT
            val Array(_clonefloor, _clonepos, direction) = readLine split " "
            val clonefloor = _clonefloor.toInt
            val clonepos = _clonepos.toInt

            if(firstRun) {
                if(clonepos < game.elevators(0).pos) game.elevators(0).direction = "RIGHT" else game.elevators(0).direction = "LEFT"
                firstRun = false
                Console.err.println(game.toString)
            }

            // Write an action using println
            // To debug: Console.err.println("Debug messages...")

            println("WAIT") // action: WAIT or BLOCK
        }
    }
}
