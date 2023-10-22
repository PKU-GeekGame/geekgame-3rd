addSbtPlugin("com.typesafe.play" % "sbt-plugin" % "2.8.20")
//addSbtPlugin("org.foundweekends.giter8" % "sbt-giter8-scaffold" % "0.16.2")
ThisBuild / libraryDependencySchemes += "org.scala-lang.modules" %% "scala-xml" % VersionScheme.Always
libraryDependencies += scalaOrganization.value % "scala-compiler" % scalaVersion.value