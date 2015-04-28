import math._
import scala.util._


object Player {

    def main(args: Array[String]) {
        val n = readInt // the number of points used to draw the surface of Mars.
        var time = 0 //-1
        val g = -3.711
        val z0 = 2501
        val v0 = 0

        for(i <- 0 until n) {
            // land_x: X coordinate of a surface point. (0 to 6999)
            // land_y: Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
            val Array(land_x, land_y) = for(i <- readLine split " ") yield i.toInt
        }

        // game loop
        while(true) {
            // horizontalSpeed: the horizontal speed (in m/s), can be negative.
            // verticalSpeed: the vertical speed (in m/s), can be negative.
            // fuel: the quantity of remaining fuel in liters.
            // angle: the rotation angle in degrees (-90 to 90).
            // power: the thrust power (0 to 4).
            time +=1
            var angleOrder: Int = 0
            var powerOrder: Int = 0
            var verticalSpeedOrder: Int = -40
            val Array(x, z, horizontalSpeed, verticalSpeed, fuel, angle, power) = for(i <- readLine split " ") yield i.toInt

            if(abs(verticalSpeed) > abs(verticalSpeedOrder) - 1) powerOrder = 4 else 0

            Console.err.println("t = " + time)
            Console.err.println("power : " + powerOrder)

            println(angleOrder + " " + powerOrder) // R P. R is the desired rotation angle. P is the desired thrust power.
        }
    }
}
