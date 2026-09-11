# PS 1 test script: ./pm < test.pm
start hog   taskset -c 5 ./worker hog
start tick  taskset -c 5 ./worker tick
start mem   ./worker mem 64
start three ./worker exit 3
start crash ./worker crash
start nope  ./no-such-program
sleep 3
list
stop hog
sleep 2
list
cont hog
kill hog
kill tick
kill mem
list
list
wait
quit
