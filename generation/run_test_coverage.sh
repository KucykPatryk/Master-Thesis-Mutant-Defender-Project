#!/bin/sh

testclass=$1
testcase=$2
nr=$3

ant testCoverage -Dtestclass=$testclass -Dtestcase=$testcase

ant testCoverageReport -Dnr=$nr

