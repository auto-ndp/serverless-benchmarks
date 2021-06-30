#!/bin/bash

SCRIPT_PATH="`dirname \"$0\"`"
SCRIPT_PATH="`( cd \"$SCRIPT_PATH\" && pwd )`"
if [[ -z "$SCRIPT_PATH" ]] ; then
  echo "Can't determine script path"
  exit 1
fi

PINTOOL_PATH="$SCRIPT_PATH/../pin-NearMAP"
PINTOOL_PATH="`( cd \"$PINTOOL_PATH\" && pwd )`"
if [[ -z "$PINTOOL_PATH" ]] ; then
  echo "Can't determine pintool path"
  exit 1
fi

PIN_ROOT="$SCRIPT_PATH/../third-party/pin3.18"
PIN_ROOT="`( cd \"$PIN_ROOT\" && pwd )`"
if [[ -z "$PIN_ROOT" ]] ; then
  echo "Can't determine Pin root path"
  exit 1
fi
export PIN_ROOT

RESULT_PATH=$SCRIPT_PATH/specrunresults
mkdir -p $RESULT_PATH

cd $SCRIPT_PATH
source ./sebs-virtualenv/bin/activate

cd $PINTOOL_PATH
echo '===========' Compiling pintool
make tools
cd $PINTOOL_PATH/stublib
echo '===========' Compiling python stublib
make python

# Set strict options after sourcing spec rc
set -euo pipefail
IFS=$'\n\t'

BENCH_SIZES=(
  'test'
  'small'
  'large'
)

PIN_EXE=$PIN_ROOT/pin
if [[ ! -f "$PIN_EXE" ]]; then
  echo "Can't determine pin executable file location"
  exit 1
fi

NEARMAP_SO=$PINTOOL_PATH/obj-intel64/NearMAP.so
if [[ ! -f "$NEARMAP_SO" ]]; then
  echo "Can't determine NearMAP.so file location"
  exit 1
fi

cd $SCRIPT_PATH

echo '===========' Finding benchmarks
FUNCTIONS=$(find ./benchmarks -name function.py | sort -n)
for func in $FUNCTIONS; do
  echo 'Function.py found: ' $func
done

echo '===========' Running benchmarks

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1

for func in $FUNCTIONS; do
  fname=$(echo $func | grep -P -o '[0-9](?!00)[0-9][0-9]\.[a-zA-Z-]+')
  echo $fname
  echo "== Running $func"
  for size in "${BENCH_SIZES[@]}"; do
    echo "= Size $size"
    echo "= Running with pin"
    rresf=${RESULT_PATH}/${fname}_${size}.log
    echo > ${rresf} # erase old results
    echo "= Saving results to '$rresf'"
    "${PIN_EXE}" -t "${NEARMAP_SO}" -o "${rresf}" -- python ./pinruntool.py --py-file "$func" --size "$size" </dev/null >${rresf}.stdout 2>${rresf}.stderr || (echo "$fname::$size failed with error code $?" ; exit 1) &
  done
done
wait
