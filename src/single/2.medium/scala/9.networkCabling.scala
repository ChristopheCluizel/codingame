import scala.collection.mutable.ArrayBuffer
import scala.io.StdIn._
import scala.math._

class Coordinate(val x: Double, val y: Double) {

  def euclideanDistanceWith(that: Coordinate): Double = {
    sqrt((x - that.x) * (x - that.x) + (y - that.y) * (y - that.y))
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
    Console.err.println("length main cable: " + res)

//    val mean = (houses.map(house => house.y).sum / houses.size).round
//    Console.err.println("Mean: " + mean)
    val theta0 = learnTheta0(houses).round
    Console.err.println("Theta0: " + theta0)
    println((res + cost(houses, theta0)).toLong)
  }

  def connectHouses(yMainCable: Double, houses: ArrayBuffer[Coordinate]): Double = {
    var res: Double = 0
    for (house <- houses) { res += house euclideanDistanceWith new Coordinate(house.x, yMainCable) }
    //    Console.err.println("res house: " + res)
    res
  }

  def learnTheta0(houses: ArrayBuffer[Coordinate]): Double = {
//    Console.err.println(houses.mkString(" "))
    val mean = (houses.map(house => house.y).sum / houses.size)
    Console.err.println("Mean: " + mean)
    var theta0 = mean
    var thetaOld = mean
    var costOld = 10000.0
    var costNew = 0.0
    val alpha = 0.1
    val m = houses.size
    for (i <- 0 until 100) {
      costOld = cost(houses, theta0)
      if (cost(houses, theta0 + alpha) < costOld) {
        theta0 = theta0 + alpha
      } else {
        theta0 = theta0 - alpha
      }
      costNew = cost(houses, theta0)
      Console.err.println("cost: " + costNew + " -> theta0: " + theta0)
      Console.err.println("CostOld: " + costOld)
    } //while (abs(costNew - costOld) > 0.1)
    theta0
  }

  def cost(houses: ArrayBuffer[Coordinate], theta0: Double): Double = {
    val m = houses.size.toDouble
    //    Console.err.println("m: " + m)
    val distance = houses.map(house => abs(theta0 - house.y))
    //    Console.err.println(distanceCarre.mkString(" "))
    val sum = distance.sum
    //    Console.err.println("Sum: " + sum)
    val res = /*(1.0 / (2.0 * m)) **/ sum
    res
  }
}
