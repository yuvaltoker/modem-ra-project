#!/bin/bash


for i in {1..3}
do
    # how many modems are there? then add 1
    declare -i x=$(docker container ls -a | grep modem_NO_ | wc -l)
    let "x += 1"
    container_name="modem_NO_$x"

    # if this is the first modem, built an image
    if [ $x = 1 ]; then
        # keep in mind you need a Dockerfile and the file which used by the Dockerfile in path
        docker build --tag modem_image ./modem/dock_modem/
    fi


    # run the container, and connecting it to the_network
    docker run -d -it --name $container_name --network=the_network modem_image

    # adjusting the modem's name in the python program for redis usage in the program
    sed -i "/^modem_name=/c\modem_name='$container_name'" ./modem/dock_modem/modem.py

    # copying the adjusted python progrm into the container instead of the previous "not adjusted" one which already inside the container
    docker cp ./modem/dock_modem/modem.py $container_name:/
done




