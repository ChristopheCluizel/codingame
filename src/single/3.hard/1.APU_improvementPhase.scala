
import math._
import scala.util._

/**
 * The machines are gaining ground. Time to show them what we're really made of...
 */
class Coordonnee(val x: Int, val y: Int) {
  override def toString: String = x + " " + y
}

class Grille(val width: Int, val height: Int, val tab: Array[Array[Node]]) {
  def display {
    Console.err.println("width: " + width + ", height: " + height)
    for (i <- 0 until height) {
      for (j <- 0 until width) {
        Console.err.print(tab(j)(i) + " # ")
      }
      Console.err.println()
    }
  }
}

class Node(val coordonnee: Coordonnee, var degre: Int) {

  def decroitreDegre = degre -= 1
  def accroitreDegre = degre += 1
  override def toString: String = "node: " + coordonnee + ", degre: " + degre
}

object Player {

  def main(args: Array[String]): Unit = {
    val width = readInt // the number of cells on the X axis
    val height = readInt // the number of cells on the Y axis
    val tabGrille = Array.ofDim[Node](width, height)
    for (i <- 0 until height) {
      val line = readLine // width characters, each either a number or a '.'
      for (j <- 0 until width) {
        var degre = 0
        if (line(j).equals('.')) degre = -1
        else degre = line(j).asDigit
        tabGrille(j)(i) = new Node(new Coordonnee(j, i), degre)
      }
    }
    val grille = new Grille(width, height, tabGrille)
    // grille.display
    var res = ""
    for (i <- 0 until height) {
      for (j <- 0 until width) {
        var counterRight = 0
        var counterBottom = 0
        var counterTop = 0
        var counterLeft = 0
        val actualNode = grille.tab(j)(i)
        if (actualNode.degre != 0) { // si case pas vide
          while (actualNode.degre > 0) {
            val rightNode: Node = findRightNode(grille, actualNode)
            val bottomNode: Node = findBottomNode(grille, actualNode)
            val topNode: Node = findTopNode(grille, actualNode)
            val leftNode: Node = findLeftNode(grille, actualNode)
            if (rightNode != null && counterRight < 2) {
              res += creerArrete(actualNode, rightNode) + "\n"
              counterRight += 1
            }
            else if (bottomNode != null && counterBottom < 2) {
              res += creerArrete(actualNode, bottomNode) + "\n"
              counterBottom += 1
            }
            else if (topNode != null && counterTop < 2) {
              res += creerArrete(actualNode, bottomNode) + "\n"
              counterTop += 1
            }
            else if (bottomNode != null && counterLeft < 2) {
              res += creerArrete(actualNode, bottomNode) + "\n"
              counterLeft += 1
            }
          }
        }
      }
    }
    println(res) // Two coordinates and one integer: a node, one of its neighbors, the number of links connecting them.
  }

  def findRightNode(grille: Grille, actualNode: Node): Node = {
    for (i <- actualNode.coordonnee.x + 1 until grille.width) {
      if (grille.tab(i)(actualNode.coordonnee.y).degre > 0) {
        return grille.tab(i)(actualNode.coordonnee.y)
      }
    }
    return null
  }

  def findBottomNode(grille: Grille, actualNode: Node): Node = {
    for (i <- actualNode.coordonnee.y + 1 until grille.height) {
      if (grille.tab(actualNode.coordonnee.x)(i).degre > 0) {
        return grille.tab(actualNode.coordonnee.x)(i)
      }
    }
    return null
  }

  def findTopNode(grille: Grille, actualNode: Node): Node = {
    for (i <- Math.max(actualNode.coordonnee.y - 1, 0) to 0) {
      if (grille.tab(actualNode.coordonnee.x)(i).degre > 0) {
        return grille.tab(actualNode.coordonnee.x)(i)
      }
    }
    return null
  }

  def findLeftNode(grille: Grille, actualNode: Node): Node = {
    for (i <- Math.max(actualNode.coordonnee.x - 1, 0) to 0) {
      if (grille.tab(i)(actualNode.coordonnee.y).degre > 0) {
        return grille.tab(i)(actualNode.coordonnee.y)
      }
    }
    return null
  }

  def creerArrete(actualNode: Node, targetNode: Node): String = {
    actualNode.decroitreDegre
    targetNode.decroitreDegre
    val res = actualNode.coordonnee.x + " " + actualNode.coordonnee.y + " " + targetNode.coordonnee.x + " " + targetNode.coordonnee.y + " 1"
    Console.err.println(res)
    res
  }
}
