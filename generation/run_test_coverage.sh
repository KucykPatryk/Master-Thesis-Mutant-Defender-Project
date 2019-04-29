#!/bin/sh

testclass=$1
testcase=$2
nr=$3
program=$4

ant -Dprogram=$program testCoverage -Dtestclass=$testclass -Dtestcase=$testcase

ant -Dprogram=$program testCoverageReport -Dnr=$nr

