#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
  echo 'Please run as sudo'
  exit
fi

furi="/usr/bin/exli"

echo -e "\e[1;34mInstalling...\e[0m"

if [ -f $furi ];
then
  rm $furi
fi
cp linux.exli.py $furi
chmod +x $furi

echo -e "\e[1;32mInstallation finished!\e[0m"