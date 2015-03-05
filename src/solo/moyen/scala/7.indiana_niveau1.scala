import math._
import scala.util._

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
 class Piece (val _type: Int, val exits: List[(String, String)]) {
    def findTheExit(entrance: String): String = {
        (for(i <- exits if i._1 == entrance) yield i._2).head
    }

    def display {
        Console.err.println("type : " + _type + " -> exits : " + exits.toString)
    }
 }

object Player {

    def main(args: Array[String]) {

        val mapPieceType = Map(
            0 -> new Piece(0, List()),
            1 -> new Piece(1, List(("LEFT", "BOTTOM"), ("RIGHT", "BOTTOM"), ("TOP", "BOTTOM"))),
            2 -> new Piece(2, List(("LEFT", "RIGHT"), ("RIGHT", "LEFT"))),
            3 -> new Piece(3, List(("TOP", "BOTTOM"))),
            4 -> new Piece(4, List(("TOP", "LEFT"), ("RIGHT", "BOTTOM"))),
            5 -> new Piece(5, List(("TOP", "RIGHT"), ("LEFT", "BOTTOM"))),
            6 -> new Piece(6, List(("RIGHT", "LEFT"), ("LEFT", "RIGHT"))),
            7 -> new Piece(7, List(("TOP", "BOTTOM"), ("RIGHT", "BOTTOM"))),
            8 -> new Piece(8, List(("LEFT", "BOTTOM"), ("RIGHT", "BOTTOM"))),
            9 -> new Piece(9, List(("LEFT", "BOTTOM"), ("TOP", "BOTTOM"))),
            10 -> new Piece(10, List(("TOP", "LEFT"))),
            11 -> new Piece(11, List(("TOP", "RIGHT"))),
            12 -> new Piece(12, List(("RIGHT", "BOTTOM"))),
            13 -> new Piece(13, List(("LEFT", "BOTTOM")))
        )

        // w: number of columns.
        // h: number of rows.
        val Array(w, h) = for(i <- readLine split " ") yield i.toInt
        var labyrinth = Array.ofDim[Piece](h, w)

        for(i <- 0 until h) {
            val line = readLine split " "
            for(j <- 0 until w) {
                labyrinth(i)(j) = mapPieceType(line(j).toInt)
            }
        }
        val ex = readInt // the coordinate along the X axis of the exit (not useful for this first mission, but must be read).

        // game loop
        while(true) {
            val Array(_xi, _yi, entrancePosition) = readLine split " "
            val xi = _xi.toInt
            val yi = _yi.toInt

            val exit =  labyrinth(yi)(xi) findTheExit(entrancePosition)
            exit match {
                case "TOP" => println(xi + " " + (yi - 1).toString)
                case "BOTTOM" => println(xi + " " + (yi + 1).toString)
                case "LEFT" => println((xi - 1).toString + " " + yi)
                case "RIGHT" => println((xi + 1).toString + " " + yi)
            }
        }
    }
}
