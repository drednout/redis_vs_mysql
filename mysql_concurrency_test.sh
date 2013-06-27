#!/bin/sh
CONCURRENCY=10
time python test_weekly_tournament.py -n 5 -t mysql_update_test -d '{person_count: 100000, warmup_time: 5}' -c $CONCURRENCY > bench_results/mysql_update_test_c${CONCURRENCY}_1_right_indexes.txt 2>&1 &
wait
sleep 60

CONCURRENCY=75
time python test_weekly_tournament.py -n 5 -t mysql_update_test -d '{person_count: 100000, warmup_time: 5}' -c $CONCURRENCY > bench_results/mysql_update_test_c${CONCURRENCY}_1_right_indexes.txt 2>&1 &
time python test_weekly_tournament.py -n 5 -t mysql_update_test -d '{person_count: 100000, shift: 100000, warmup_time: 5}' -c $CONCURRENCY > bench_results/mysql_update_test_c${CONCURRENCY}_2_right_indexes.txt 2>&1 &
wait
sleep 60

CONCURRENCY=125
time python test_weekly_tournament.py -n 5 -t mysql_update_test -d '{person_count: 100000, warmup_time: 5}' -c $CONCURRENCY > bench_results/mysql_update_test_c${CONCURRENCY}_1_right_indexes.txt 2>&1 &
time python test_weekly_tournament.py -n 5 -t mysql_update_test -d '{person_count: 100000, shift: 100000, warmup_time: 5}' -c $CONCURRENCY > bench_results/mysql_update_test_c${CONCURRENCY}_2_right_indexes.txt 2>&1 &
wait
sleep 60

CONCURRENCY=500
time python test_weekly_tournament.py -n 5 -t mysql_update_test -d '{person_count: 100000, warmup_time: 5}' -c $CONCURRENCY > bench_results/mysql_update_test_c${CONCURRENCY}_1_right_indexes.txt 2>&1 &
time python test_weekly_tournament.py -n 5 -t mysql_update_test -d '{person_count: 100000, shift: 100000, warmup_time: 5}' -c $CONCURRENCY > bench_results/mysql_update_test_c${CONCURRENCY}_2_right_indexes.txt 2>&1 &
wait
sleep 60

CONCURRENCY=1250
time python test_weekly_tournament.py -n 5 -t mysql_update_test -d '{person_count: 100000, warmup_time: 5}' -c $CONCURRENCY > bench_results/mysql_update_test_c${CONCURRENCY}_1_right_indexes.txt 2>&1 &
time python test_weekly_tournament.py -n 5 -t mysql_update_test -d '{person_count: 100000, shift: 100000, warmup_time: 5}' -c $CONCURRENCY > bench_results/mysql_update_test_c${CONCURRENCY}_2_right_indexes.txt 2>&1 &
wait
sleep 60

CONCURRENCY=2500
time python test_weekly_tournament.py -n 5 -t mysql_update_test -d '{person_count: 100000, warmup_time: 5}' -c $CONCURRENCY > bench_results/mysql_update_test_c${CONCURRENCY}_1_right_indexes.txt 2>&1 &
time python test_weekly_tournament.py -n 5 -t mysql_update_test -d '{person_count: 100000, shift: 100000, warmup_time: 5}' -c $CONCURRENCY > bench_results/mysql_update_test_c${CONCURRENCY}_2_right_indexes.txt 2>&1 &
wait
sleep 60

CONCURRENCY=5000
time python test_weekly_tournament.py -n 5 -t mysql_update_test -d '{person_count: 100000, warmup_time: 5}' -c $CONCURRENCY > bench_results/mysql_update_test_c${CONCURRENCY}_1_right_indexes.txt 2>&1 &
time python test_weekly_tournament.py -n 5 -t mysql_update_test -d '{person_count: 100000, shift: 100000, warmup_time: 5}' -c $CONCURRENCY > bench_results/mysql_update_test_c${CONCURRENCY}_2_right_indexes.txt 2>&1 &
wait
sleep 60

CONCURRENCY=7500
time python test_weekly_tournament.py -n 5 -t mysql_update_test -d '{person_count: 100000, warmup_time: 5}' -c $CONCURRENCY > bench_results/mysql_update_test_c${CONCURRENCY}_1_right_indexes.txt 2>&1 &
time python test_weekly_tournament.py -n 5 -t mysql_update_test -d '{person_count: 100000, shift: 100000, warmup_time: 5}' -c $CONCURRENCY > bench_results/mysql_update_test_c${CONCURRENCY}_2_right_indexes.txt 2>&1 &
wait
