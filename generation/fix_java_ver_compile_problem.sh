#!/bin/sh

program=$1

export PATH=$PWD/bin:/opt/JDK/jdk1.7.0_80/bin/:$PATH  # Fix to force java 7
MAJOR_HOME="../major"
$MAJOR_HOME/bin/ant -DmutOp="=$MAJOR_HOME/mml/all.mml.bin" -Dprogram=$program mutateFix
