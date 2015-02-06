import math._
import scala.util._
import scala.collection.mutable.ArrayBuffer

object Orientation extends Enumeration {
    type Orientation = Value
    val H, V = Value
}

import Orientation._

class Dragon(var id: Int, var nbWallLeft: Int, var position: Position) {
    override def toString: String = "Dragon id : " + id + " position : "  + position + " nbWallLeft : " + nbWallLeft
}

class Position(var y: Int, var x: Int) {
    override def toString: String = "(" + x + ", " + y + ")"
}

class Wall(var position: Position, var orientation: String) {
    override def toString: String = "Wall position " + position + ", orientation : " + orientation
}

class Labyrinth(val width: Int, val height: Int, val nbPlayers: Int, val myId: Int) {
    var nbWallDeployed = 0
    var walls: ArrayBuffer[Wall] = ArrayBuffer()

    override def toString: String = {
        var string = "Labyrinth width : " + width + ", height : " + height + ", nbPlayer : " + nbPlayers + ", myId : " + myId +
            ",  nbWallDeployed : " + nbWallDeployed + "\n"
        for(i <- 0 until walls.length) string += walls(i) + "\n"
        string
    }
}

object Player {

    def main(args: Array[String]) {
        // w: width of the board
        // h: height of the board
        // playercount: number of players (2,3, or 4)
        // myid: id of my player (0 = 1st player, 1 = 2nd player, ...)
        val Array(width, height, nbPlayer, myId) = for(i <- readLine split " ") yield i.toInt
        var labyrinth = new Labyrinth(width, height, nbPlayer, myId)
        var dragons = new Array[Dragon](nbPlayer)
        for(i <- 0 until nbPlayer) {
            dragons(i) = new Dragon(i, 0, new Position(0, 0))
        }

        // game loop
        while(true) {
            for(i <- 0 until nbPlayer) {
                // x: x-coordinate of the player
                // y: y-coordinate of the player
                // wallsleft: number of walls available for the player
                val Array(x, y, wallsleft) = for(i <- readLine split " ") yield i.toInt
                dragons(i).id = i
                dragons(i). nbWallLeft = wallsleft
                dragons(i).position = new Position(y, x)
                Console.err.println(dragons(i).toString)
            }

            val wallcount = readInt // number of walls on the board
            labyrinth.nbWallDeployed = wallcount
            while(labyrinth.walls.length < wallcount) labyrinth.walls += new Wall(new Position(0, 0), "")

            for(i <- 0 until wallcount) {
                // wallx: x-coordinate of the wall
                // wally: y-coordinate of the wall
                // wallorientation: wall orientation ('H' or 'V')
                val Array(_wallx, _wally, wallorientation) = readLine split " "
                val wallx = _wallx.toInt
                val wally = _wally.toInt
                labyrinth.walls(i).position = new Position(wally, wallx)
                labyrinth.walls(i).orientation = wallorientation
            }

            Console.err.println(labyrinth)

            // Write an action using println
            // To debug: Console.err.println("Debug messages...")

            println("RIGHT") // action: LEFT, RIGHT, UP, DOWN or "putX putY putOrientation" to place a wall
        }
    }
}
