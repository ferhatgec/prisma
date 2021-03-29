#!/usr/bin/env bash

if ! [ -d "/usr/share/pixmaps/prism/" ]; then
  sudo mkdir /usr/share/pixmaps/prism/

  if [ "$EUID" -ne 0 ]; then
      echo "Run without super-user permissions"
    exit
  fi

  mkdir $HOME/.config/prism/
fi

if ! [ -D "~.config/prisma/" ]; then
  mkdir ~.config/prisma/
fi

sudo /bin/mkdir /usr/share/pixmaps/prism/homepage/

sudo cp resources/homepage/* /usr/share/pixmaps/prism/homepage/

sudo cp resources/*.png /usr/share/pixmaps/prism/

sudo cp prisma.py /bin/prisma

sudo chmod 755 /bin/prisma