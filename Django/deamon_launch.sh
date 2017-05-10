if [ $# -ne 1 ]; then
  exit 1
fi
if [ $1 = "start" ]; then
  if [ -f .deamon_launch.pid ]; then
    echo "server already run"
  else
    nohup ./launch.sh &> .server.log 2>&1&
    echo $! > .deamon_launch.pid
  fi
elif [ $1 = "kill" ]; then
  kill $(cat .deamon_launch.pid)
  kill $(cat .postgres.pid)
  killall postgres
  killall python
  rm .deamon_launch.pid
  rm .postgres.pid
elif [ $1 = "status" ]; then
  less +G .server.log
fi
