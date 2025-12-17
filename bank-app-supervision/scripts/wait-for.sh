#!/usr/bin/env bash
# Usage: wait-for.sh host:port [-t timeout] [-- command args]
# Credit: https://github.com/eficode/wait-for
set -e
TIMEOUT=30
QUIET=0

echoerr() { if [ $QUIET -ne 1 ]; then printf "%s\n" "$*" 1>&2; fi }

usage()
{
    cat << USAGE >&2
Usage:
    $0 host:port [-t timeout] [-- command args]
USAGE
    exit 1
}

wait_for()
{
    for i in `seq $TIMEOUT` ; do
        nc -z "$HOST" "$PORT" >/dev/null 2>&1 && return 0
        sleep 1
    done
    return 1
}

while [ $# -gt 0 ]
do
    case "$1" in
        *:* )
        HOST=$(printf "%s\n" "$1"| cut -d : -f 1)
        PORT=$(printf "%s\n" "$1"| cut -d : -f 2)
        shift 1
        ;;
        -q | --quiet)
        QUIET=1
        shift 1
        ;;
        -t)
        TIMEOUT="$2"
        shift 2
        ;;
        --)
        shift
        break
        ;;
        *)
        echoerr "Unknown argument: $1"
        usage
        ;;
    esac
done

if [ -z "$HOST" ] || [ -z "$PORT" ]; then
    echoerr "Error: you need to provide a host and port to test."
    usage
fi

wait_for || {
    echoerr "Timeout after ${TIMEOUT}s waiting for $HOST:$PORT"
    exit 1
}

exec "$@"
