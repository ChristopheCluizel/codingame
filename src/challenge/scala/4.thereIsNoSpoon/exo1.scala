package thereIsNoSpoon

/**
 * Don't let the machines win. You are humanity's last hope...
 */
class Coordonnee(val x: Int, val y: Int) {
  override def toString: String = x + " " + y
}

class Grille(val width: Int, val height: Int, val tab: Array[Array[Char]]) {
  def display {
    Console.err.println("width: " + width + ", height: " + height)
    for (i <- 0 until height) {
      for (j <- 0 until width) {
        Console.err.print(tab(j)(i))
      }
      Console.err.println()
    }
  }
}

object Player extends App {

  override def main(args: Array[String]): Unit = {
    val width = readInt // the number of cells on the X axis
    val height = readInt // the number of cells on the Y axis
    val tabGrille = Array.ofDim[Char](width, height)
    for (i <- 0 until height) {
      val line = readLine // width characters, each either 0 or .
      for (j <- 0 until width) tabGrille(j)(i) = line(j)
    }
    val grille = new Grille(width, height, tabGrille)
    //grille.display

    var res: String = ""
    for (i <- 0 until height) {
      for (j <- 0 until width) {
        if (grille.tab(j)(i).equals('0')) {
          val actualNode = new Coordonnee(j, i)
          val rightNode: Coordonnee = findRightNode(grille, actualNode)
          val bottomNode: Coordonnee = findBottomNode(grille, actualNode)
          res += actualNode + " " + rightNode + " " + bottomNode + "\n"
        }
      }
    }
    println(res)
  }

  def findRightNode(grille: Grille, actualNode: Coordonnee): Coordonnee = {
    for (i <- actualNode.x + 1 until grille.width) {
      if (grille.tab(i)(actualNode.y).equals('0')) {
        return new Coordonnee(i, actualNode.y)
      }
    }
    return new Coordonnee(-1, -1)
  }

  def findBottomNode(grille: Grille, actualNode: Coordonnee): Coordonnee = {
    for (i <- actualNode.y + 1 until grille.height) {
      if (grille.tab(actualNode.x)(i).equals('0')) {
        return new Coordonnee(actualNode.x, i)
      }
    }
    return new Coordonnee(-1, -1)
  }
}
