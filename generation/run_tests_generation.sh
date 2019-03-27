#!/bin/sh

export PATH=$PWD/bin:/usr/lib/jvm/java-1.8.0-openjdk-amd64/bin/:$PATH # Change to java 8

echo
echo "Generating and compiling tests"
echo "(ant compile.tests)"
echo

folder_name=$1
file_name=$2

javac testing/*/*.java

java -jar libs/evosuite-1.0.6.jar -class $1.$2 -projectCP testing/

ant compile.tests
