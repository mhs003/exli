#!/data/data/com.termux/files/usr/bin/bash

furi="/data/data/com.termux/files/usr/bin/exli"

if [ -f $furi ] ;
then
  echo -e "\e[1;31mUn-installing...\e[0m"
  rm $furi
  echo -e "\e[1;34m'exli' has been removed from your system. I you want install it again, see https://github.com/mhs003/exli\e[0m"
else
  echo -e "\e[1m'exli' is not installed in this system\e[0m"
fi