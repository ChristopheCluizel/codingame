import math._
import scala.util._

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
object Player {

    def main(args: Array[String]) {

        // game loop
        while(true) {
            var indexMax=0
            var heightMax=0
            val Array(sx, sy) = for(i <- readLine split " ") yield i.toInt
            for(i <- 0 until 8) {
                val mh = readInt // represents the height of one mountain, from 9 to 0. Mountain heights are provided from left to right.
                if(mh > heightMax) {indexMax = i; heightMax = mh}
            }
            if(sx == indexMax) println("FIRE") else println("HOLD")
        }
    }
}
