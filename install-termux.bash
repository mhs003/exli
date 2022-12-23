#!/data/data/com.termux/files/usr/bin/bash

furi="/data/data/com.termux/files/usr/bin/exli"

echo -e "\e[1;34mInstalling...\e[0m

if [ -f $furi ] ;
then
  rm $furi
fi
cp termux.exli.py $furi
chmod +x $furi

echo -e "\e[1;32mInstallation finished!\e[0m"