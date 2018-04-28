import math._
import scala.util._

case class Position(val x: Int, val y: Int) {
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
  val remainingGold: Int, // -1 if unknown
  val maxGoldRate: Int, // -1 if unknown
  val position: Position,
  val radius: Int,
  val structureType: Int, // -1: No structure, 0: mine, 1: Tower, 2: Barracks
  val owner: Int, // -1 no structure, 0 friendly, 1 enemy
  val state: Int, // -1 if no structure, if tower remaining HP, if mine golden rate, else nb of turns
  val creepType: Int // -1 if no structure or mine, 0 for KNIGHT, 1 for ARCHER, 2 for GIANT. If tower attack radius
) {

  override def toString: String = s"$structureTypeName site $id at $position with $radius radius and max gold rate of" +
      s" $maxGoldRate is owned by " +
      s"$ownerName with turn/HP/golden rate $state to build/or with $creepTypeName"

  def structureTypeName = structureType match {
    case 0 => "mine"
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

  def mySide = if (getQueen(0).position.x < 960) "left" else "right"

  def getQueen(owner: Int): Unit = {
    getUnits(owner, -1).head
  }

  def getKnights(owner: Int): List[Unit] = {
    getUnits(owner, 0)
  }

  def getGiant(owner: Int): List[Unit] = {
    getUnits(owner, 2)
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

  def getBarracksGiant(owner: Int): List[Site] = {
    getBarracks(owner, 2)
  }

  def getBarracks(owner: Int, creepType: Int): List[Site] = {
    sites.filter(site => site.owner == owner && site.creepType == creepType)
  }

  def getTowers(owner: Int): List[Site] = {
    sites.filter(site => site.structureType == 1 && site.owner == owner)
  }

  def getMines(owner: Int): List[Site] = {
    sites.filter(site => site.structureType == 0 && site.owner == owner)
  }

  def queenAttacked(): Boolean = {
    val myQueen = getQueen(0)
    val ennemyDistances = units.filter(unit => unit.owner == 1 && unit.unitType == 0)
        .map(unit => (unit, myQueen.position.distanceWith(unit.position)))
        .filter { case (unit, distance) => distance < 300 }
    if (ennemyDistances.size >= 2) {
      Console.err.println("Queen under attack !!!")
      true
    } else {
      false
    }
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
  def trainUnits(board: Board, _gold: Int): String = {
    var gold = _gold
    val barracksKnightSite = board.getBarracksKnight(0)
    val barracksGiantSite = board.getBarracksGiant(0)
    // get nearest sites from ennemy
    val nearestSites: List[Site] = getNearestSitesForAUnit(board.getQueen(1),
      barracksKnightSite) ::: getNearestSitesForAUnit(board.getQueen(1), barracksGiantSite)
    val sitesToTrain: List[Site] = nearestSites.filter(site => site.creepType != -1)

    val siteIdsToTrain: List[Int] = sitesToTrain.map { site =>
      //      if (board.getGiant(0).size < 1 && site.creepType == 2 && gold >= site.creepCost) {
      //        gold = gold - site.creepCost
      //        site.id
      //      }
      if (board.getBarracksKnight(0).size >= 2 && site.creepType == 0 && _gold >= 2 * site.creepCost) {
        gold = gold - site.creepCost
        site.id
      }
      else if (board.getBarracksKnight(0).size < 2 && site.creepType == 0 && gold >= site.creepCost) {
        gold = gold - site.creepCost
        site.id
      }
      else {
        None
      }
    }.filter(site => site != None).asInstanceOf[List[Int]]
    val siteIdsToTrainString = siteIdsToTrain.mkString(" ")
    if (siteIdsToTrain.size > 0) "TRAIN " + siteIdsToTrainString else "TRAIN"
  }

  def buildNearestSite(board: Board): String = {
    val nearestSites: List[Site] = getNearestSitesForAUnit(board.getQueen(0), board.sites)
    // structureType != 1 because a queen can not build on existing tower
    val sitesToBuild = nearestSites.filter(site => (site.owner == -1 || site.owner == 1) && site.structureType != 1)
    var siteToBuild = sitesToBuild.head
    var buildType = -1
    val myMines = board.sites.filter(site => site.structureType == 0 && site.owner == 0)
    val initialization: Boolean = board.getTowers(0).size < 3
    val towerHealthTarget = if (initialization) 300 else 700

    if (board.queenAttacked()) {
      val safePosition = if (board.mySide == "left") {
        val sitePosition = if (board.getTowers(0).size > 0) {
          board.getTowers(0).sortBy(site => site.position.x).head.position
        } else {
          board.getBarracksKnight(0).sortBy(site => site.position.x).head.position
        }
        sitePosition.minus(Position(50, 0))
      }
      else {
        val sitePosition = if (board.getTowers(0).size > 0) {
          board.getTowers(0).sortBy(site => site.position.x).reverse.head.position
        } else {
          board.getBarracksKnight(0).sortBy(site => site.position.x).reverse.head.position
        }
        sitePosition.plus(Position(50, 0))
      }
      return s"MOVE ${safePosition.x} ${safePosition.y}"
    }

    // upgrade mines
    if (myMines.size > 0) {
      val ids = upgradeMines(board)
      if (ids.size > 0) {
        return s"BUILD ${ids.head} MINE"
      }
      // build mines
      else if (myMines.size < 3) {
        val id = buildXMines(board)
        return s"BUILD $id MINE"
      }
    }
    // build mines
    else if (myMines.size < 3) {
      val id = buildXMines(board)
      return s"BUILD $id MINE"
    }

    // build a knight barrack
    if (board.sites.filter(site => site.creepType == 0 && site.owner == 0).size < 1) {
      buildType = 0
    }
    // get number of my giant barracks
    //    else if (board.sites.filter(site => site.creepType == 2 && site.owner == 0).size < 1) {
    //      buildType = 2
    //    }

    // upgrade towers
    else if (board.getTowers(0).size > 0) {
      val ids = upgradeTowers(board, towerHealthTarget)
      if (ids.size > 0) {
        return s"BUILD ${ids.head} TOWER"
      }
      // build towers
      else if (board.getTowers(0).size < 3) {
        val id = buildXTowers(board)
        return s"BUILD $id TOWER"
      }
    }

    // build towers
    else if (board.getTowers(0).size < 3) {
      val id = buildXTowers(board)
      return s"BUILD $id TOWER"
    }

    // build 2 additional mines
    //    else if (myMines.size < 3) {
    //      buildType = 3
    //      val mineBuildingSign = if(board.getBarracksKnight(0).map(site => site.position.x).max < 960) 1 else -1
    //      val sitesOnTheLeft = sitesToBuild.filter(site => (site.position.x * mineBuildingSign) < (960 *
    // mineBuildingSign) && site.remainingGold != 0)
    //      siteToBuild = if (sitesOnTheLeft.size > 0) sitesOnTheLeft.head else siteToBuild
    //    }
    // add additional knight barracks
    //    if (board.sites.filter(site => site.creepType == 0 && site.owner == 0).size < 2) {
    //      buildType = 0
    //    }
    //    // build 2 additional mines if towers health > 100
    //    else if (myTowers.map(tower => tower.state).max > 100 && myMines.size < 5) {
    //      buildType = 3
    //      val sitesOnTheLeft = sitesToBuild.filter(site => site.position.x < 700 && site.remainingGold != 0)
    //      siteToBuild = if (sitesOnTheLeft.size > 0) sitesOnTheLeft.head else siteToBuild
    //    }
    //    else if (myTowers.map(tower => tower.state).max > 100 && myTowers.size < 5) {
    //      buildType = 10
    //    }

    // expand the towers
    if (board.getTowers(0).size > 0 && board.getTowers(0).map(site => site.state).min > 700) {
      val id = buildXTowers(board)
      return s"BUILD $id TOWER"
    }

    // repair towers with less HP
    if (board.getTowers(0).size > 0) {
      siteToBuild = board.sites
          .filter(site => site.owner == 0 && site.structureType == 1)
          .sortBy(site => site.state)
          .toList
          .head
      buildType = 10
    }

    buildType match {
      case 0 => s"BUILD ${siteToBuild.id} BARRACKS-KNIGHT"
      case 1 => s"BUILD ${siteToBuild.id} BARRACKS-ARCHER"
      case 2 => s"BUILD ${siteToBuild.id} BARRACKS-GIANT"
      case 3 => s"BUILD ${siteToBuild.id} MINE"
      case 10 => s"BUILD ${siteToBuild.id} TOWER"
      case _ => "WAIT"
    }
  }

  def buildXTowers(board: Board): Int = {
    val nearestSites: List[Site] = getNearestSitesForAUnit(board.getQueen(0), board.sites)
    val buildableSites = nearestSites.filter(site => (site.owner == -1 || site.owner == 1) && site.structureType != 1)
    val buildableSite = buildableSites.head

    return buildableSite.id
  }

  def getNearestSitesForAUnit(unit: Unit, sites: List[Site]): List[Site] = {
    sites.map(site => (site, unit.position.distanceWith(site.position)))
        .sortBy { case (site, distance) => distance }
        .map { case (site, distance) => site }
        .toList
  }

  def upgradeTowers(board: Board, limit: Int): List[Int] = {
    val myTowers = board.getTowers(0)
    myTowers.filter(site => site.state < limit).sortBy(site => site.state).map(site => site.id)
  }

  def buildXMines(board: Board): Int = {
    val nearestSites: List[Site] = getNearestSitesForAUnit(board.getQueen(0), board.sites)
    val buildableSites = nearestSites
        .filter(site => (site.owner == -1 || site.owner == 1) && site.structureType != 1 && site.remainingGold != 0)
    val buildableSite = buildableSites.head
    return buildableSite.id
  }

  def upgradeMines(board: Board): List[Int] = {
    val myMines = board.getMines(0)
    myMines.filter(site => site.state < site.maxGoldRate).sortBy(site => site.state).map(site => site.id)
  }
}

object Player extends App {
  val numsites = readInt
  val sites = for {
    i <- 0 until numsites
    val Array(siteid, x, y, radius) = for (i <- readLine split " ") yield i.toInt
    val site = Site(siteid, -1, -1, Position(x, y), radius, -1, -1, 0, -1)
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
      val Array(siteid,
      ignore1,
      ignore2,
      structuretype,
      owner,
      param1,
      param2) = for (i <- readLine split " ") yield i
          .toInt
      val currentSite: Site = board.sites.filter(site => site.id == siteid).head
    } yield Site(currentSite.id,
      ignore1,
      ignore2,
      currentSite.position,
      currentSite.radius,
      structuretype,
      owner,
      param1,
      param2)

    board.sites = newSites.toList

    val numunits = readInt
    val units = for {
      i <- 0 until numunits
      val Array(x, y, owner, unittype, health) = for (i <- readLine split " ") yield i.toInt
    } yield Unit(Position(x, y), owner, unittype, health)

    board.units = units.toList

    //    Console.err.println(game)

    // First line: A valid queen action
    // Second line: A set of training instructions
    println(ia.buildNearestSite(board))
    println(ia.trainUnits(board, game.goldAmount))
  }
}
