#!/bin/bash

if [ ! -f /tmp/x86-ubuntu-gpu-ml-isca ]; then
  cp x86-ubuntu-gpu-ml-isca.gz /tmp
  gunzip /tmp/x86-ubuntu-gpu-ml-isca.gz
fi

ln -s /tmp/x86-ubuntu-gpu-ml-isca .
