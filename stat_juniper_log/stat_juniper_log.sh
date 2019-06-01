#!/bin/bash

log=log.access
echo "Start parse $log"
output=stat_juniper.dat
time ./parse_juniper_log.py $log >$output
echo "Data produced: $output"

gnuplot stat_juniper.plt
