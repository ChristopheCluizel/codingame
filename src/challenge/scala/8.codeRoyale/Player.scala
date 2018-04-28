import math._
import scala.util._

case class Position(val x: Int, val y: Int) {
  override def toString: String = s"($x, $y)"

  def distanceWith(that: Position): Double = {
    Math.sqrt((that.x - x) * (that.x - x) + (that.y - y) * (that.y - y))
  }
}

case class Unit(
  val position: Position,
  val owner: Int, // 0 = Friendly; 1 = Enemy
  val unitType: Int, // -1 for Queen, 0 for KNIGHT, 1 for ARCHER
  health: Int) {

  override def toString: String = s"$unitTypeName $health PV $position is $ownerName"

  def ownerName = if (owner == 0) "friendly" else "enemy"

  def unitTypeName = if (unitType == -1) "queen" else if (unitType == 0) "knight" else "archer"
}

case class Site(
  val id: Int,
  val position: Position,
  val radius: Int,
  val structureType: Int, // -1: No structure, 2: Barracks
  val owner: Int, // -1 no structure, 0 friendly, 1 enemy
  val remainingTrainingTurns: Int, // -1 if no structure
  val creepType: Int // -1 if no structure, 0 for KNIGHT, 1 for ARCHER
) {

  override def toString: String = s"$structureTypeName site $id at $position with $radius radius is owned by " +
      s"$ownerName with $remainingTrainingTurns to build $creepTypeName"

  def structureTypeName = if (structureType == -1) "no structure" else "barracks"

  def ownerName = if (owner == -1) "none" else if (owner == 0) "friendly" else "enemy"

  def creepTypeName = if (creepType == -1) "none" else if (creepType == 0) "knight" else "archer"
}


case class Board(
  val siteNumber: Int,
  var sites: List[Site],
  var units: List[Unit]
) {
  override def toString: String = s"==== Board ====\nnb of sites: $siteNumber\n${sites.mkString("\n")}\n${
    units.mkString("\n")
  }"
}

case class Game(
  var goldAmount: Int,
  var touchedSiteId: Int, // -1 if none
  val board: Board
) {
  override def toString: String = s"goldAmount: $goldAmount, touchedSite: $touchedSiteId\n$board"
}

object Player extends App {
  val numsites = readInt
  val sites = for {
    i <- 0 until numsites
    val Array(siteid, x, y, radius) = for (i <- readLine split " ") yield i.toInt
    val site = Site(siteid, Position(x, y), radius, -1, -1, 0, -1)
  } yield site

  val board = Board(numsites, sites.toList, List())
  val game = Game(0, -1, board)

  while (true) {
    val Array(gold, touchedsite) = for (i <- readLine split " ") yield i.toInt
    game.touchedSiteId = touchedsite
    game.goldAmount = gold

    val newSites = for {
      i <- 0 until numsites
      val Array(siteid, ignore1, ignore2, structuretype, owner, param1, param2) = for (i <- readLine split " ") yield i
          .toInt
      val currentSite: Site = board.sites.filter(site => site.id == siteid).head
    } yield Site(currentSite.id, currentSite.position, currentSite.radius, structuretype, owner, param1, param2)

    board.sites = newSites.toList

    val numunits = readInt
    val units = for {
      i <- 0 until numunits
      val Array(x, y, owner, unittype, health) = for (i <- readLine split " ") yield i.toInt
    } yield Unit(Position(x, y), owner, unittype, health)

    board.units = units.toList

    Console.err.println(game)

    // First line: A valid queen action
    // Second line: A set of training instructions
    println("BUILD 6 BARRACKS-KNIGHT")
    println("TRAIN 6")
  }
}
