#!/bin/bash


# keep in mind you need a Dockerfile in path
declare -i x=$(docker container ls -a | grep modem | wc -l)
let "x += 1"
# how many modems are there? then add 1

contName="modem_NO_$x"
# if this is the first modem, built an image
if [ $x = 1 ]; then
    docker build --tag modem_image .
fi


# run the container, and connecting it to the_network
docker run -d -it --name $contName --network=the_network modem_image
