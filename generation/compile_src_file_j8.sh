#!/bin/sh

export PATH=$PWD/bin:/usr/lib/jvm/java-1.8.0-openjdk-amd64/bin/:$PATH # Change to java 8

program=$1
src_file=$2

javac programs/$1/testing/$1/$2.java
