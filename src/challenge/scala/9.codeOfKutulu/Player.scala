import math._
import scala.util._
import scala.Array._
import scala.collection.mutable.ArrayBuffer

case class Position(x: Int, y: Int) {
  override def toString: String = s"($x, $y)"

  def distanceWith(that: Position): Double = {
    Math.sqrt((that.x - x) * (that.x - x) + (that.y - y) * (that.y - y))
  }

  def minus(that: Position): Position = {
    Position(this.x - that.x, this.y - that.y)
  }

  def plus(that: Position): Position = {
    Position(this.x + that.x, this.y + that.y)
  }
}

class Unit(
  id: Int,
  position: Position,
  owner: Int
) {
  override def toString: String = s"id: $id, owner: $owner, $position"
}

case class Explorer(
  val id: Int,
  val position: Position,
  val owner: Int,
  val sanity: Int,
  val ignore1: Int,
  val ignore2: Int
) extends Unit(id, position, owner) {
  override def toString: String = s"Explorer id: $id, owner: $owner, $position, HP: $sanity"
}

case class Wanderer(
  val id: Int,
  val position: Position,
  val owner: Int,
  val timeRecall: Int,
  val state: Int,
  val target: Int
) extends Unit(id, position, owner) {
  override def toString: String = s"Wanderer id: $id, owner: $owner, $position, timeRecal/spawn: $timeRecall, " +
      s"state: $state, target: $target"
}

case class Spawn(
  val id: Int,
  val position: Position,
  val owner: Int,
  val timeSpawn: Int
) extends Unit(id, position, owner) {
  override def toString: String = s"Spawn id: $id, owner: $owner, $position, timeSpawn: $timeSpawn"
}

case class Board(
  width: Int,
  height: Int,
  squares: Array[Array[String]],
  var units: List[Unit]
) {
  override def toString: String = s"==== Board ====\nheight: $height, width: $width\n${units.mkString("\n")}"

  def squaresToString: String = squares.map(x => x.mkString("")).mkString("\n")

  def getExplorers: List[Explorer] = units.collect { case unit: Explorer => unit }

  def getWanderers: List[Wanderer] = units.collect { case unit: Wanderer => unit }
}

case class Game(
  board: Board
) {
  override def toString: String = s"$board"
}

case class IA() {
  def glueOneExplorer(board: Board): String = {
    val ennemy = board.getExplorers.filter(explorer => explorer.owner != 1).head
    s"MOVE ${ennemy.position.x} ${ennemy.position.y}"
  }
}

object Player extends App {
  val width = readInt
  val height = readInt
  val boardString = for {i <- 0 until height
                         val line = readLine
  } yield line

  val boardSquares = boardString.toArray.map(x => x.split(""))
  val board = Board(width, height, boardSquares, List())
  val game = Game(board)
  val ia = IA()

  // sanitylosslonely: how much sanity you lose every turn when alone, always 3 until wood 1
  // sanitylossgroup: how much sanity you lose every turn when near another player, always 1 until wood 1
  // wandererspawntime: how many turns the wanderer take to spawn, always 3 until wood 1
  // wandererlifetime: how many turns the wanderer is on map after spawning, always 40 until wood 1
  val Array(sanitylosslonely,
  sanitylossgroup,
  wandererspawntime,
  wandererlifetime) = for (i <- readLine split " ") yield i.toInt

  // game loop
  while (true) {
    val entitycount = readInt // the first given entity corresponds to your explorer
    var firstUnit = true
    val units = for {
      i <- 0 until entitycount
      val Array(entitytype, _id, _x, _y, _param0, _param1, _param2) = readLine split " "
      val id = _id.toInt
      val x = _x.toInt
      val y = _y.toInt
      val param0 = _param0.toInt
      val param1 = _param1.toInt
      val param2 = _param2.toInt

      val unit: Unit = if (firstUnit) {
        firstUnit = false
        Explorer(id, Position(x, y), 1, param0, -1, -1)
      } else {
        if (entitytype == "EXPLORER") {
          Explorer(id, Position(x, y), -1, param0, -1, -1)
        } else if (entitytype == "WANDERER") {
          Wanderer(id, Position(x, y), 0, param0, param1, param2)
        } else {
          Spawn(id, Position(x, y), 0, param0)
        }
      }
    } yield unit

    board.units = units.toList

    Console.err.println(game)

    println(ia.glueOneExplorer(board))
  }
}
