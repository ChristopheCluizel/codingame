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
  val unitType: Int, // -1 for Queen, 0 for KNIGHT, 1 for ARCHER, 2 GIANT
  health: Int) {

  override def toString: String = s"$unitTypeName $health PV $position is $ownerName"

  def ownerName = if (owner == 0) "friendly" else "enemy"

  def unitTypeName = unitType match {
    case -1 => "queen"
    case 0 => "knight"
    case 1 => "archer"
    case 2 => "giant"
  }
}

case class Site(
  val id: Int,
  val position: Position,
  val radius: Int,
  val structureType: Int, // -1: No structure, 1: Tower 2: Barracks
  val owner: Int, // -1 no structure, 0 friendly, 1 enemy
  val remainingTrainingTurns: Int, // -1 if no structure, if tower remaining HP, else nb of turns
  val creepType: Int // -1 if no structure, 0 for KNIGHT, 1 for ARCHER, 2 for GIANT. If tower attack radius
) {

  override def toString: String = s"$structureTypeName site $id at $position with $radius radius is owned by " +
      s"$ownerName with turn/HP $remainingTrainingTurns to build/or with $creepTypeName"

  def structureTypeName = structureType match {
    case 1 => "tower"
    case 2 => "barrack"
    case _ => "NONE"
  }

  def ownerName = if (owner == -1) "NONE" else if (owner == 0) "friendly" else "enemy"

  def creepTypeName = creepType match {
    case 0 => "BARRACKS-KNIGHT"
    case 1 => "BARRACKS-ARCHER"
    case 2 => "BARRACKS-GIANT"
    case -1 => "NONE"
    case _ => s"attack radius: $creepType"
  }

  def creepCost: Int = creepType match {
    case 0 => 80
    case 1 => 100
    case 2 => 140
    case _ => 0
  }
}


case class Board(
  val siteNumber: Int,
  var sites: List[Site],
  var units: List[Unit]
) {
  override def toString: String = s"==== Board ====\nnb of sites: $siteNumber\n${sites.mkString("\n")}\n${
    units.mkString("\n")
  }"

  def getQueen(owner: Int): Unit = {
    getUnits(owner, -1).head
  }

  def getKnights(owner: Int): List[Unit] = {
    getUnits(owner, 0)
  }

  def getUnits(owner: Int, unitType: Int): List[Unit] = {
    units.filter(unit => unit.owner == owner && unit.unitType == unitType)
  }

  def getArchers(owner: Int): List[Unit] = {
    getUnits(owner, 1)
  }

  def getBarracksKnight(owner: Int): List[Site] = {
    getBarracks(owner, 0)
  }

  def getBarracksArcher(owner: Int): List[Site] = {
    getBarracks(owner, 1)
  }

  def getBarracks(owner: Int, creepType: Int): List[Site] = {
    sites.filter(site => site.owner == owner && site.creepType == creepType)
  }
}

case class Game(
  var goldAmount: Int,
  var touchedSiteId: Int, // -1 if none
  val board: Board
) {
  override def toString: String = s"goldAmount: $goldAmount, touchedSite: $touchedSiteId\n$board"
}

case class IA() {
  def buildNearestSite(board: Board, creepType: Int): String = {
    val nearestSites: List[Site] = getNearestSitesForAUnit(board.getQueen(0), board.sites)
    if (nearestSites.size > 0) {
      val siteToBuild = nearestSites.filter(site => (site.owner == -1 || site.owner == 1) && site.structureType != 1).head
      if (creepType == 0) {
        s"BUILD ${siteToBuild.id} BARRACKS-KNIGHT"
      } else if (creepType == 1) {
        s"BUILD ${siteToBuild.id} BARRACKS-ARCHER"
      } else {
        ""
      }
    }
    else {
      s"WAIT"
    }
  }

  def getNearestSitesForAUnit(unit: Unit, sites: List[Site]): List[Site] = {
    sites.map(site => (site, unit.position.distanceWith(site.position)))
        .sortBy { case (site, distance) => distance }
        .map { case (site, distance) => site }
        .toList
  }

  def trainUnits(board: Board, _gold: Int): String = {
    var gold = _gold
    val barracksKnightSite = board.getBarracksKnight(0)
    // get nearest sites from ennemy
    val nearestSites: List[Site] = getNearestSitesForAUnit(board.getQueen(1), barracksKnightSite)
    val sitesToTrain: List[Site] = nearestSites.filter(site => site.creepType != -1)

    val siteIdsToTrain: List[Int] = sitesToTrain.map { site =>
      if (gold >= site.creepCost) {
        gold = gold - site.creepCost
        site.id
      } else {
        None
      }
    }.filter(site => site != None).asInstanceOf[List[Int]]
    val siteIdsToTrainString = siteIdsToTrain.mkString(" ")
    if (siteIdsToTrain.size > 0) "TRAIN " + siteIdsToTrainString else "TRAIN"
  }
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
  val ia = IA()

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
    println(ia.buildNearestSite(board, 0))
    println(ia.trainUnits(board, game.goldAmount))
  }
}
