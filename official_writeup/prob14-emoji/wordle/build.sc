import mill._
import $ivy.`com.lihaoyi::mill-contrib-playlib:`,  mill.playlib._

object wordle extends PlayModule with SingleModule {

  def scalaVersion = "2.13.12"
  def playVersion = "2.8.20"
  def twirlVersion = "1.6.0-RC2"

  object test extends PlayTests
}
