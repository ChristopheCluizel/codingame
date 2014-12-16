import math._
import scala.util._

/**
 * The code below will read all the game information for you.
 * On each game turn, information will be available on the standard input, you will be sent:
 * -> the total number of visible enemies
 * -> for each enemy, its name and distance from you
 * The system will wait for you to write an enemy name on the standard output.
 * Once you have designated a target:
 * -> the cannon will shoot
 * -> the enemies will move
 * -> new info will be available for you to read on the standard input.
 **/
object Player {

    def main(args: Array[String]) {

        // game loop
        while(true) {
            val count = readInt // The number of current enemy ships within range
            var closestEnemy = ""
            var closerDistance = 1000
            for(i <- 0 until count) {
                // enemy: The name of this enemy
                // dist: The distance to your cannon of this enemy
                val Array(enemy, _dist) = readLine split " "
                val dist = _dist.toInt
                //Console.err.println(enemy + " -> " + dist)
                if(dist < closerDistance){
                    closerDistance = dist
                    closestEnemy = enemy
                }
            }

            // Write an action using println
            // To debug: Console.err.println("Debug messages...")

            println(closestEnemy) // The name of the most threatening enemy (HotDroid is just one example)
        }
    }
}
