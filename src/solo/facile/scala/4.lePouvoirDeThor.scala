import math._
import scala.util._

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
object Player {

    def main(args: Array[String]) {
        // lx: the X position of the light of power
        // ly: the Y position of the light of power
        // tx: Thor's starting X position
        // ty: Thor's starting Y position
        var Array(lx, ly, tx, ty) = for(i <- readLine split " ") yield i.toInt

        // game loop
        while(true) {
            val e = readInt // The level of Thor's remaining energy, representing the number of moves he can still make.
            var order = ""

            if(ty < ly) {order="S"; ty+=1} else if(ty > ly) {order="N"; ty-=1}
            if(tx < lx) {order+="E"; tx+=1} else if(tx > lx) {order+="W"; tx-=1}
            //Console.err.print(tx + " -> " + ty)

            println(order) // A single line providing the move to be made: N NE E SE S SW W or NW
        }
    }
}
