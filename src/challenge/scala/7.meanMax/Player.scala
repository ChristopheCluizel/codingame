import scala.collection.immutable

case class Position(val x: Int, val y: Int) {
  override def toString: String = s"p($x, $y)"
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

class Reaper(unitId: Int,
  unitType: Int,
  radius: Int,
  position: Position,
  val playerId: Int,
  val mass: Float,
  val speed: Speed) extends Unit(unitId, unitType, radius, position) {

  override def toString: String = s"unitId: $unitId, unitType: $unitType, playerId: $playerId, radius: $radius, " +
      s"mass: $mass, position: $position, speed: $speed"
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
      val unit = if (unittype == 0) {
        new Reaper(unitid, unittype, radius, Position(x, y), player, mass, Speed(vx, vy))
      } else {
        new Wreck(unitid, unittype, radius, Position(x, y), extra)
      }
    } yield unit

    val units = rawUnits.toList
    val (reapers, wrecks) = units.partition(unit => unit.unitType == 0)
    Console.err.println("==== reapers ====")
    Console.err.println(reapers.mkString("\n"))
    Console.err.println("==== wrecks ====")
    Console.err.println(wrecks.mkString("\n"))

    val firstTarget = wrecks.head

    // Write an action using println
    // To debug: Console.err.println("Debug messages...")

    println(s"${firstTarget.position.x} ${firstTarget.position.y} 100")
    println("WAIT")
    println("WAIT")
  }
}