#!/bin/bash
## script to get quota sum

if [ $# -lt 2 ]; then
  echo "$0 filer volume"
  echo "or"
  echo "$0 filer vfiler volume"
fi

if [ $# -eq 2 ]; then
  filer=$1
  volume=$2
  echo "Checking quota for volume: $2"
  echo -e "\tSpace available in AFS: \c"
  ssh -n -l root $filer df -h $volume | egrep -v "Filesystem|snap" | awk '{print $2}'
  echo -e "\tTotal quota size: \c"
  ssh -n -l root $filer quota report | grep $volume | awk 'BEGIN{sum=0} {sum=sum+$6} END{print sum}'
else
  if [ $# -eq 3 ]; then
    filer=$1
    vfiler=$2
    volume=$3
    echo "Checking quota for volume: $3"
    echo -e "\tSpace available in AFS: \c"
    ssh -n -l root $filer df -h $volume | egrep -v "Filesystem|snap" | awk '{print $2}'
    echo -e "\tTotal quota size: \c"
    ssh -n -l root $filer vfiler run $vfiler quota report | grep $volume | awk 'BEGIN{sum=0} {sum=sum+$6} END{print sum}'
  fi
fi
