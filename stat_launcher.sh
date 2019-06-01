#!/bin/bash

function print_stderr {
    echo "$@" >&2
}

function warn {
    print_stderr "Warning -" $@
}

function raise_error {
    print_stderr "Error -" $@
    exit 8
}



DATA_DIR=./var

prog_name=$(basename $0 .sh)
dir_name=$(dirname $0)
cd $dir_name
output=$DATA_DIR/${prog_name}.dat
py=${prog_name}.py
input=$DATA_DIR/${prog_name}.csv
plot=${prog_name}.plt

while getopts "co:i:" opt
do
    case $opt in
    c)
        flag='clean'
        ;;
    o)
        output=$OPTARG
        ;;
    i)
        input=$OPTARG
        ;;
    *)
        ;;
    esac
done

# Check
if [ ! -d $DATA_DIR ] ; then
    raise_error "Need $DATA_DIR for input data and output results"
fi
if [ ! -f $input ] ; then
    raise_error "No data files '$input'"
fi
python=python3
if ! which $python 2>/dev/null 1>&2 ; then
    raise_error "Need $python in path for program"
fi
gnuplot=gnuplot
if ! which $gnuplot 2>/dev/null 1>&2 ; then
    raise_error "Need $gnuplot in path for plotting data"
fi

case $flag in
clean)
    rm $DATA_DIR/*.png $DATA_DIR/*.dat 2>/dev/null
    ;;
*)
    echo "Execution of $py $input redirect to $output"
    if $python ./$py $input >$output ; then
        echo "Plotting data from $output with $plot instructions"
        exec gnuplot -e "basename=\"${prog_name}\"" -e "data_file=\"$output\"" -e "var=\"$DATA_DIR\"" $plot
    else
        raise_error "$python execution error"
    fi
    ;;
esac
