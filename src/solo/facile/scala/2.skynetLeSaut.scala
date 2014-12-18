import math._
import scala.util._

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
object Player {

    def main(args: Array[String]) {
        val r = readInt // the length of the road before the gap.
        val g = readInt // the length of the gap.
        val l = readInt // the length of the landing platform.
        val speedOrder = g+1
        var hasJumped = false

        // game loop
        while(true) {
            val s = readInt // the motorbike's speed.
            val x = readInt // the position on the road of the motorbike.

            if(!hasJumped){
                if(r < (x + s)) {println("JUMP"); hasJumped = true}
                else{
                    if(s < speedOrder) println("SPEED")
                    else if(s > speedOrder) println("SLOW")
                    else println("WAIT")
                }
            }
            else println("SLOW")
        }
    }
}
