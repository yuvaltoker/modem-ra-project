#!/bin/bash


# keep in mind you need a Dockerfile in path
# how many modems are there? then add 1
declare -i x=$(docker container ls -a | grep modem_NO_ | wc -l)
let "x += 1"
container_name="modem_NO_$x"

# if this is the first modem, built an image
if [ $x = 1 ]; then
    docker build --tag modem_image .
fi


# run the container, and connecting it to the_network
docker run -d -it --name $container_name --network=the_network modem_image

# adjusting the modem's name in the python program for redis usage in the program
sed -i "/^modem_name =/c\modem_name = '$container_name'" ./modem.py
#sed "s/# modem_name = 'modem_NO_/modem_name = '$container_name'/" ./modem.py
docker cp ./modem.py $container_name:/
