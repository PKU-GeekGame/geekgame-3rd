name := """wordle"""
organization := "cn.edu.pku.geekgame"

version := "1.0-SNAPSHOT"

lazy val root = (project in file(".")).enablePlugins(PlayScala)

scalaVersion := "2.13.12"

libraryDependencies += guice
libraryDependencies += "org.scalatestplus.play" %% "scalatestplus-play" % "5.1.0" % Test
libraryDependencies += "ch.qos.logback" % "logback-classic" % "1.4.3"
libraryDependencies += "ch.qos.logback" % "logback-core" % "1.4.3"

// Adds additional packages into Twirl
//TwirlKeys.templateImports += "cn.edu.pku.geekgame.controllers._"

// Adds additional packages into conf/routes
// play.sbt.routes.RoutesKeys.routesImport += "cn.edu.pku.geekgame.binders._"
