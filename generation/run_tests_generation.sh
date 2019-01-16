#!/bin/sh

export PATH=$PWD/bin:/usr/lib/jvm/java-1.8.0-openjdk-amd64/bin/:$PATH # Change to java 8

#export CLASSPATH=evosuite-standalone-runtime-1.0.6.jar:hamcrest-core-1.3.jar:triangle/Triangle:$CLASSPATH
#export CLASSPATH=target/classes:evosuite-standalone-runtime-1.0.6.jar:evosuite-tests:junit-4.12.jar:hamcrest-core-1.3.jar

echo
echo "Generating tests"
echo "(ant compile.tests)"
echo

#ant compile.tests
#$MAJOR_HOME/bin/ant -Dbuild.compiler=major.ant.MajorCompiler compile.tests

#export EVOSUITE=java -jar libs/evosuite-1.0.6.jar

javac testing/triangle/Triangle.java

java -jar libs/evosuite-1.0.6.jar -class triangle.Triangle -projectCP testing/
