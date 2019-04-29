#!/bin/sh

testclass=$1
testcase=$2
program=$3

echo $testclass
echo $testcase

MAJOR_HOME="../major"
#export PATH=$PWD/bin:/opt/JDK/jdk1.7.0_80/bin/:$PATH  # Fix to force java 7
#export CLASSPATH=evosuite-standalone-runtime-1.0.6.jar:hamcrest-core-1.3.jar:triangle/Triangle:$CLASSPATH
export PATH=$MAJOR_HOME/bin:$PATH

$MAJOR_HOME/bin/ant -Dprogram=$program mutation.testSelected -Dbuild.compiler=major.ant.MajorCompiler -Dtestclass=$testclass -Dtestcase=$testcase
#$MAJOR_HOME/bin/ant -Dbuild.compiler=major.ant.MajorCompiler mutation.test

#$MAJOR_HOME/bin/ant mutation.testSingle
