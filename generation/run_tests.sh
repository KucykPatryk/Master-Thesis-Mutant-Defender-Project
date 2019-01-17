#!/bin/sh

MAJOR_HOME="../.."
export PATH=$PWD/bin:/opt/JDK/jdk1.7.0_80/bin/:$PATH  # Fix to force java 7
#export CLASSPATH=evosuite-standalone-runtime-1.0.6.jar:hamcrest-core-1.3.jar:triangle/Triangle:$CLASSPATH

echo
echo "Run tests with mutation analysis"
echo "(ant mutation.test)"

export PATH=$MAJOR_HOME/bin:$PATH
$MAJOR_HOME/bin/ant -Dbuild.compiler=major.ant.MajorCompiler mutation.test

#$MAJOR_HOME/bin/ant mutation.testSingle
