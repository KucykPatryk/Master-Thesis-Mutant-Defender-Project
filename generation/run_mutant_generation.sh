#!/bin/sh
#export PATH=$PWD/bin:$PATH # Major compiler change path, do when in the major folder
export PATH=$PWD/bin:/opt/JDK/jdk1.7.0_80/bin/:$PATH  # Fix to force java 7
#export PATH=/usr/lib/jvm/java-7-openjdk/bin/:$PATH  # Fix to force java 7
MAJOR_HOME="../major"

echo
echo "Compiling and mutating project"
echo
$MAJOR_HOME/bin/ant -DmutOp="=$MAJOR_HOME/mml/all.mml.bin" clean mutate


