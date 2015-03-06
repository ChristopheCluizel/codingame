import math._
import scala.util._

object Solution {

    def main(args: Array[String]) {
        var first = readInt
        val lineToDisplay = readInt

        def iterForALine(list: List[Int], res: List[Int], acc: Int, headPrec: Int): List[Int] = list match {
        	case Nil => headPrec :: acc :: res
        	case x :: xs => if (x == headPrec) iterForALine(xs, res, acc + 1, headPrec)
        					else iterForALine(xs, headPrec :: acc :: res, 1, x)
        }

        var list = List[List[Int]](List[Int](first))

        for(i <- 1 until lineToDisplay) {
        	list = (iterForALine(list.head, List[Int](), 0, first).reverse) :: list
        	first = list.head.head
        }

        println(list.head.mkString(" "))
    }
}
