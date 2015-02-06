import math._
import scala.util._

class Dragon(val id: Int, var nbWall: Int) {
}

object Player {

    def main(args: Array[String]) {
        // w: width of the board
        // h: height of the board
        // playercount: number of players (2,3, or 4)
        // myid: id of my player (0 = 1st player, 1 = 2nd player, ...)
        val Array(w, h, playercount, myid) = for(i <- readLine split " ") yield i.toInt

        // game loop
        while(true) {
            for(i <- 0 until playercount) {
                // x: x-coordinate of the player
                // y: y-coordinate of the player
                // wallsleft: number of walls available for the player
                val Array(x, y, wallsleft) = for(i <- readLine split " ") yield i.toInt
            }
            val wallcount = readInt // number of walls on the board
            for(i <- 0 until wallcount) {
                // wallx: x-coordinate of the wall
                // wally: y-coordinate of the wall
                // wallorientation: wall orientation ('H' or 'V')
                val Array(_wallx, _wally, wallorientation) = readLine split " "
                val wallx = _wallx.toInt
                val wally = _wally.toInt
            }

            // Write an action using println
            // To debug: Console.err.println("Debug messages...")

            println("RIGHT") // action: LEFT, RIGHT, UP, DOWN or "putX putY putOrientation" to place a wall
        }
    }
}
