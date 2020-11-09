# modem-ra-project

# a comment

Here are the instructions for the user:


1. Open the terminal, get into "modem-ra-project" if you're not already in it. Then write the next commands:

    # build & run the snmpd, redis_db and the ra containers
    docker-compose up &

    # for list of all containers you can type the following
    docker container ls -a

    # now lets build and run the three modems' containers (every time running the following command it builds another 3 modems)
    ./create_new_modem.sh &

    # okay, so far we have: redis_db, snmpd, ra, and 3/6/9/.... modems, all are set and on. 
    # lets get inside them, and run the programs.

    # in a new terminal enter the ra container
    docker exec -it ra bash

    # then run the ra program
    ./ra.py

    # in a new terminal, I recommand to split the screen into 3 sections (I use tmux, you can use any other platform)
    # in every section of the splited terminal: 

    # in section 1, enter the first modem, then run the modem's program
    docker exec -it modem_NO_1

    # then
    ./modem.py

    # in section 2, enter the second modem, then run the modem's program
    docker exec -it modem_NO_2

    # then
    ./modem.py

    # in section 3, enter the third modem, then run the modem's program
    docker exec -it modem_NO_3

    # then
    ./modem.py
