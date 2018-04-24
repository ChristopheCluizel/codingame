import scala.collection.immutable

case class Position(val x: Int, val y: Int) {
  override def toString: String = s"p($x, $y)"

  def distanceWith(that: Position): Double = {
    Math.sqrt((that.x - x) * (that.x - x) + (that.y - y) * (that.y - y))
  }
}

case class Speed(val vx: Int, val vy: Int) {
  override def toString: String = s"v($vx, $vy)"
}

class Unit(val unitId: Int,
  val unitType: Int,
  val radius: Int,
  val position: Position) {
  override def toString: String = s"unitId: $unitId, unitType: $unitType, radius: $radius, position: $position"
}

class Looter(unitId: Int,
  unitType: Int,
  radius: Int,
  position: Position,
  val playerId: Int,
  val mass: Float,
  val speed: Speed,
  val water: Int,
  val waterCapacity: Int) extends Unit(unitId, unitType, radius, position) {

  override def toString: String = s"unitId: $unitId, unitType: $unitType, playerId: $playerId, radius: $radius, " +
      s"mass: $mass, position: $position, speed: $speed, water: $water, waterCapacity: $waterCapacity"

  def isInWreck(wreck: Wreck): Boolean = {
    position.distanceWith(wreck.position) < wreck.radius
  }

  def stop: String = "WAIT"
}

class Wreck(unitId: Int,
  unitType: Int,
  radius: Int,
  position: Position,
  val water: Int) extends Unit(unitId, unitType, radius, position) {

  override def toString: String = s"unitId: $unitId, unitType: $unitType, radius: $radius, water: $water " +
      s"position: $position"
}

object Player extends App {
  def degreToRadian(degre: Int): Double = (2 * Math.PI * degre) / 360

  def findWinningEnemy(score1: Int, score2: Int): Int = {
    if (score1 < score2) 2 else 1
  }

  def selectNearestTanker(myDestroyer: Looter, tankers: List[Looter]): Looter = {
    val orderedTankers = tankers.sortBy(tanker => myDestroyer.position.distanceWith(tanker.position))
    orderedTankers.head
  }

  def selectNearestWreck(myReaper: Looter, wrecks: List[Wreck]): Wreck = {
    val orderedWrecks = wrecks.sortBy(wreck => myReaper.position.distanceWith(wreck.position))
    orderedWrecks.head
  }

  def selectNearestEnemy(myDoof: Looter, enemies: List[Looter]): Looter = {
    val orderedEnemies = enemies.sortBy(enemy => myDoof.position.distanceWith(enemy.position))
    orderedEnemies.head
  }

  def selectBestTanker(myDestroyer: Looter, tankers: List[Looter]): Looter = {
    def score(myDestroyer: Looter, tanker: Looter): Double = {
      val speed = 300
      val distance = myDestroyer.position.distanceWith(tanker.position)
      val water = tanker.water
      (speed / (2 * distance)) + water * 100
    }

    tankers.map(tanker => (tanker, score(myDestroyer, tanker)))
        .sortBy(tuple => tuple._2)
        .reverse
        .head
        ._1
  }

  def selectBestwreck(myReaper: Looter, wrecks: List[Wreck]): Wreck = {
    def score(myReaper: Looter, wreck: Wreck): (Double, Double) = {
      val speed = 200
      val distance = myReaper.position.distanceWith(wreck.position)
      val water = wreck.water
      val score = (speed / (distance / 100)) + water * 10
      (score, distance)
    }

    val sortedScoredWrecks = wrecks.map(wreck => (wreck, score(myReaper, wreck)))
        .sortBy(tuple => tuple._2._1)
        .reverse
    Console.err.println(sortedScoredWrecks.mkString("\n"))
    sortedScoredWrecks.head._1
  }

  var theta = 0

  // game loop
  while (true) {
    val myscore = readInt
    val enemyscore1 = readInt
    val enemyscore2 = readInt
    val myrage = readInt
    val enemyrage1 = readInt
    val enemyrage2 = readInt
    val unitcount = readInt
    val rawUnits: immutable.Seq[Unit] = for {
      i <- 0 until unitcount
      val Array(_unitid, _unittype, _player, _mass, _radius, _x, _y, _vx, _vy, _extra, _extra2) = readLine split " "
      val unitid = _unitid.toInt
      val unittype = _unittype.toInt
      val player = _player.toInt
      val mass = _mass.toFloat
      val radius = _radius.toInt
      val x = _x.toInt
      val y = _y.toInt
      val vx = _vx.toInt
      val vy = _vy.toInt
      val extra = _extra.toInt
      val extra2 = _extra2.toInt
      val unit = if (unittype == 4) {
        new Wreck(unitid, unittype, radius, Position(x, y), extra)
      } else {
        new Looter(unitid, unittype, radius, Position(x, y), player, mass, Speed(vx, vy), extra, extra2)
      }
    } yield unit

    val units = rawUnits.toList
    val reapers = units.filter(unit => unit.unitType == 0).map(unit => unit.asInstanceOf[Looter])
    val destroyers = units.filter(unit => unit.unitType == 1).map(unit => unit.asInstanceOf[Looter])
    val doofs = units.filter(unit => unit.unitType == 2).map(unit => unit.asInstanceOf[Looter])
    val tankers = units.filter(unit => unit.unitType == 3).map(unit => unit.asInstanceOf[Looter])
    val wrecks = units.filter(unit => unit.unitType == 4).map(unit => unit.asInstanceOf[Wreck])

//    Console.err.println("==== reapers ====")
//    Console.err.println(reapers.mkString("\n"))
//    Console.err.println("==== destroyers ====")
//    Console.err.println(destroyers.mkString("\n"))
//    Console.err.println("==== doofs ====")
//    Console.err.println(doofs.mkString("\n"))
//    Console.err.println("==== tankers ====")
//    Console.err.println(tankers.mkString("\n"))
//    Console.err.println("==== wrecks ====")
//    Console.err.println(wrecks.mkString("\n"))

    val myReaper = reapers.filter(repear => repear.playerId == 0 && repear.unitType == 0).head
    val myDestroyer = destroyers.filter(destroyer => destroyer.playerId == 0 && destroyer.unitType == 1).head
    val myDoof = doofs.filter(doof => doof.playerId == 0 && doof.unitType == 2).head

//    val enemies = units.filter(unit => unit.unitType != 4).map(unit => unit.asInstanceOf[Looter]).filter(looter => looter.playerId != 0 && looter.unitType != 3)
    val reaperEnemies = reapers.filter(repear => repear.playerId != 0)

    Console.err.println("==== myReaper ====")
    Console.err.println(myReaper)
    Console.err.println("==== myDestoyer ====")
    Console.err.println(myDestroyer)
    Console.err.println("==== myDoof ====")
    Console.err.println(myDoof)

    // get the tankers arrived in the big circle
    val tankersInTheGame = tankers.filter(tanker => tanker.position.distanceWith(Position(0, 0)) < 6000)

    // choose the target for my destroyer
    val myDestroyerTarget = if (tankersInTheGame.nonEmpty) {
      val bestTanker = selectNearestTanker(myDestroyer, tankersInTheGame)
      Console.err.println("==== best tanker ====")
      Console.err.println(bestTanker)
      bestTanker
    } else myReaper

    // choose the target for my reaper
    val myReaperTarget = if (wrecks.nonEmpty) {
      val bestWreck = selectNearestWreck(myReaper, wrecks)

      Console.err.println("==== best wreck ====")
      Console.err.println(bestWreck)
      bestWreck
    } else myDestroyer

    // choose the target for my doof
    val thetaRadian = degreToRadian(theta)
    val x_circle = 5000 * Math.cos(thetaRadian)
    val y_circle = 5000 * Math.sin(thetaRadian)
    val myDoofTargetPosition = Position(x_circle.toInt, y_circle.toInt)
    theta = (theta + 10) % 360

    if(myReaper.position.distanceWith(myReaperTarget.position) < myReaperTarget.radius && (myReaper.speed.vx > myReaperTarget.radius ||  myReaper.speed.vy > myReaperTarget.radius))
      println(s"${-myReaperTarget.position.x} ${-myReaperTarget.position.y} 300")
    else
      println(s"${myReaperTarget.position.x} ${myReaperTarget.position.y} 300")
    println(s"${myDestroyerTarget.position.x} ${myDestroyerTarget.position.y} 300")
    println(s"${myDoofTargetPosition.x} ${myDoofTargetPosition.y} 300")
  }
}