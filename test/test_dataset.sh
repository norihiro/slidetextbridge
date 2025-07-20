#! /bin/bash

set -e

exe=${EXE:-slidetextbridge}

for cfg in test/data/*.yaml; do
	set -e
	echo "Running $cfg..."
	$exe -q -c $cfg < ${cfg/.yaml/.in} |
		diff -u - ${cfg/.yaml/.out}
done
