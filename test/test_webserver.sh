#! /usr/bin/bash

exe=${EXE:-slidetextbridge}

port=$(awk '
$3 == "00000000:0000" {
	port = strtonum("0x" substr($2, 10, 4));
	ports[port] = 1
}
END {
	port = 8080;
	while (port in ports)
		port++;
	print port;
}
' /proc/net/tcp)

cfg=$(mktemp '.cfg-XXXXXXX.yaml')

cat > $cfg <<EOF
steps:
  - type: stdin
  - type: webserver
    port: $port
    host: 127.0.0.1
EOF

(sleep 1m | $exe -q -c $cfg) &
subshell_pid=$!
pid="$(pgrep -P $subshell_pid)"

retried=0
until curl --silent "http://127.0.0.1:$port/" > /dev/null; do
	retried=$((retried+1))
	if ((retried > 10)); then
		exit 1
	fi
	sleep 0.$retried
done

for f in index.html script.js style.css; do
	url="http://127.0.0.1:$port/$f" 
	echo "Checking $url..."
	curl --silent "$url" | diff -u src/slidetextbridge/plugins/data/webserver/default/$f -
done

kill -s SIGINT $pid
wait $subshell_pid

rm -f $cfg
