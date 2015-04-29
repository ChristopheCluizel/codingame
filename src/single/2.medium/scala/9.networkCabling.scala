import math._
import scala.io.StdIn._
import scala.collection.mutable.ArrayBuffer

class Coordinate(val x: Int, val y: Int) {

  def euclideanDistanceWith(that: Coordinate): Double = {
    sqrt((x - that.x) * (x - that.x) + (y - that.y) * (y - that.y));
  }

  override def toString: String = "(" + x + ", " + y + ")"
}

object CoordinateOrderingByAbscissa extends Ordering[Coordinate] {
  def compare(a: Coordinate, b: Coordinate) = a.x compare b.x
}

object CoordinateOrderingByOrdinate extends Ordering[Coordinate] {
  def compare(a: Coordinate, b: Coordinate) = a.y compare b.y
}

object Solution {
  def main(args: Array[String]): Unit = {

    var res: Double = 0
    val cableLength: ArrayBuffer[Double] = ArrayBuffer()
    val houses: ArrayBuffer[Coordinate] = ArrayBuffer()
    val numberOfHouses = readInt
    for (i <- 0 until numberOfHouses) {
      val Array(x, y) = for (i <- readLine split " ") yield i.toInt
      houses += new Coordinate(x, y)
    }
    var xMin = houses.min(CoordinateOrderingByAbscissa).x
    var xMax = houses.max(CoordinateOrderingByAbscissa).x
    var yMin = houses.min(CoordinateOrderingByOrdinate).y
    var yMax = houses.max(CoordinateOrderingByOrdinate).y

    Console.err.println("x min: " + xMin)
    Console.err.println("x max: " + xMax)
    Console.err.println("y min: " + yMin)
    Console.err.println("y max: " + yMax)
    res += new Coordinate(xMin, 0) euclideanDistanceWith new Coordinate(xMax, 0)
//    Console.err.println("length main cable: " + res)

    for (i <- yMin to yMax) {
      cableLength += res + connectHouses(i, houses)
    }
    Console.err.println(cableLength.mkString(", "))
    println((cableLength.min).toInt)
  }

  def connectHouses(yMainCable: Int, houses: ArrayBuffer[Coordinate]): Double = {
    var res: Double = 0
    for (house <- houses) { res += house euclideanDistanceWith new Coordinate(house.x, yMainCable) }
//    Console.err.println("res house: " + res)
    res
  }
}
