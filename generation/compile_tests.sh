#!/bin/sh

program=$1

ant -Dprogram=$program compile.tests
