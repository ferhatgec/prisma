#!/usr/bin/env bash

if ! [ -d "/usr/share/pixmaps/prism/" ]; then
  sudo mkdir /usr/share/pixmaps/prism/
  sudo cp resource/*.png /usr/share/pixmaps/prism/

  if [ "$EUID" -ne 0 ]; then
      echo "Run without super-user permissions"
    exit
  fi

  mkdir $HOME/.config/prism/
fi

sudo cp prisma.py /bin/prisma

sudo chmod 755 /bin/prisma