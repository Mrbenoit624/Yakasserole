if [ $# -ne 1 ]; then
  exit 1
fi
if [ $1 = "start" ]; then
  if [ -f .deamon_launch.pid ]; then
    echo "server already run"
  else
    ./launch.sh& 2>&1 > .server.log
    echo $! > .deamon_launch.pid
  fi
elif [ $1 = "kill" ]; then
  kill $(cat .deamon_launch.pid)
  kill $(cat .postgres.pid)
  killall postgres
  killall python
  rm .deamon_launch.pid
  rm .postgres.pid
fi
