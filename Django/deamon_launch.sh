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
  while IFS='' read -r line;do
    echo -e "$(sed -r 's/(.*200.*)/\\033\[32m\0\\e\[39m/' |
    sed -r 's/(.*304.*)/\\033\[33m\0\\e[39m/' |
    sed -r 's/(.*404.*)/\\033\[31m\0\\e[39m/') $line" ;
  done < .server.log | less -R
#  less -R +G +F .server.log
elif [ $1 = "restart" ]; then
  $0 kill
  sleep 1s
  $0 start
fi
