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
  val waterCapacity: Int) extends Unit(unitId, unitType, radius, position) {

  override def toString: String = s"unitId: $unitId, unitType: $unitType, playerId: $playerId, radius: $radius, " +
      s"mass: $mass, position: $position, speed: $speed"

  def isInWreck(wreck: Wreck): Boolean = {
    position.distanceWith(wreck.position) < wreck.radius
  }

  def stop: String = "WAIT"
}

class Wreck(unitId: Int,
  unitType: Int,
  radius: Int,
  position: Position,
  val extra: Int) extends Unit(unitId, unitType, radius, position) {

  override def toString: String = s"unitId: $unitId, unitType: $unitType, radius: $radius, extra: $extra " +
      s"position: $position"
}

object Player extends App {

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
        new Looter(unitid, unittype, radius, Position(x, y), player, mass, Speed(vx, vy), extra2)
      }
    } yield unit

    val units = rawUnits.toList
    val reapers = units.filter(unit => unit.unitType == 0).map(unit => unit.asInstanceOf[Looter])
    val destroyers = units.filter(unit => unit.unitType == 1).map(unit => unit.asInstanceOf[Looter])
    val tankers = units.filter(unit => unit.unitType == 3).map(unit => unit.asInstanceOf[Looter])
    val wrecks = units.filter(unit => unit.unitType == 4).map(unit => unit.asInstanceOf[Wreck])

    Console.err.println("==== reapers ====")
    Console.err.println(reapers.mkString("\n"))
    Console.err.println("==== destroyers ====")
    Console.err.println(destroyers.mkString("\n"))
    Console.err.println("==== tankers ====")
    Console.err.println(tankers.mkString("\n"))
    Console.err.println("==== wrecks ====")
    Console.err.println(wrecks.mkString("\n"))

    val myReaper = reapers.filter(repear => repear.playerId == 0 && repear.unitType == 0).head
    val myDestroyer = destroyers.filter(destroyer => destroyer.playerId == 0 && destroyer.unitType == 1).head

    Console.err.println("==== myReaper ====")
    Console.err.println(myReaper)
    Console.err.println("==== myDestoyer ====")
    Console.err.println(myDestroyer)

    val orderedTankers = tankers.sortBy(tanker => myDestroyer.position.distanceWith(tanker.position))
    val nearestTanker = orderedTankers.head

    Console.err.println("==== closest tanker ====")
    Console.err.println(nearestTanker)

    val myReaperTarget = if (wrecks.nonEmpty) {
      val orderedWrecks = wrecks.sortBy(wreck => myReaper.position.distanceWith(wreck.position))
      val nearestWreck = orderedWrecks.head

      Console.err.println("==== closest wreck ====")
      Console.err.println(nearestWreck)

      nearestWreck
    } else nearestTanker

    println(s"${myReaperTarget.position.x} ${myReaperTarget.position.y} 200")
    println(s"${nearestTanker.position.x} ${nearestTanker.position.y} 200")
    println("WAIT")
  }
}