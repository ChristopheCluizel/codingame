import math._
import scala.util._
import scala.collection.mutable.ArrayBuffer

object Solution {

    def main(args: Array[String]) {
        val nbValues = readInt
        val values_string = readLine
        var values: ArrayBuffer[Int] = ArrayBuffer()
        var diffMax = 0
        var diff = 0
        var i = 0
        var valueMax = 0

        for(i <- values_string split " ") {
            values += i.toInt
        }

        for( i <- 0 until values.length - 1) {
            if(values(i) > values(i+1)) {
                if(values(i) > valueMax) valueMax = values(i)
                diff += values(i+1) - values(i)
                if(abs(diff) > abs(diffMax)) diffMax = diff
            }
            else {
                diff += values(i+1) - values(i)
                if(values(i+1) > valueMax) diff = 0
            }
        }

        println(diffMax)
    }
}
