#!/bin/bash

if [ $# -ne 1 ]; then
    echo give pipe arg
    exit 1
fi

export PIPE="$1"

source poke-lib.sh

receive_gift()
{
    if [ "$open_limit_reached" != "true" ]; then
        printf "############# Open gift"
        printf "click:250,831,1,200\n" | tee $PIPE
        ## gift-send:color:218,831,0xFF,0xD0,0xF9
        ## gift-send:color:218,831,255,208,249
        # sleep 1
        check_color 205 838 151 218 147 10 10
        echo press open
        click 291 853
        ## gift-send:color:291,853,0x84,0xD4,0xA5
        ## gift-send:color:291,853,132,212,165
        sleep 2
        if check_color 150 519 232 128 181 10 ; then
            echo Limit reached
            printf "click:290,945,3,200\n" | tee $PIPE
            sleep 1
            no_gift="true"
            open_limit_reached="true"
        else
            printf "click:291,853,1,200\n" | tee $PIPE
            sleep 1
            for (( i = 0; i < 10; i ++)); do
                click 165 885
                check_color 131 1002 255 255 253 10 && break
            done
            sleep 1
        fi
    else
        echo limit reached don not open
        click 289 950
        no_gift="true"
        sleep 1
    fi
}

wait_friend_page()
{
   # while ! check_color 285 182 255 255 255 5 ; do
   while ! check_color 258 121 255 255 255 16 ; do
        timeout=$(( timeout - 1 ))
        echo "Countdown $timeout"
        if [ $timeout -le 0 ]; then
            echo Timeout try from begining
            back_home
            friends_page
        fi
        # if [ $(( $timeout % 50 )) -eq 0 ]; then
        #    echo Takes too long try on stup up
        # fi
        # click friends
        # printf "click:291,100,1,200\n" | tee $PIPE
        echo Wait for tainer screen
        sleep 0.5
    done
    
}

friends_page()
{
    echo Go to friend page
    # click avatar
    printf "click:75,925,1,200\n" | tee $PIPE
    sleep 3
    # click friends
    printf "click:291,100,1,200\n" | tee $PIPE
    sleep 0.5
    printf "click:291,100,1,200\n" | tee $PIPE
    ## gift-s7:color:75,925,0x1A,0x13,0x0A
    # don't wait forever
    timeout=10
    wait_friend_page
}

gift_cycle()
{
    # check which round
    # Search trainer
    # type dela
    # if check_color 515 244 12 202 165 5
    # printf "click:470,239,1,200\n" | tee $PIPE
    printf "click:350,239,1,200\n" | tee $PIPE
    sleep 3
    echo "key:\b" | tee $PIPE
    echo "key:\b" | tee $PIPE
    echo "key:\b" | tee $PIPE
    echo "key:\b" | tee $PIPE
    echo "key:\!" | tee $PIPE
    echo "key:f" | tee $PIPE
    echo "key:f" | tee $PIPE
    sleep 0.5
    click 490 582
    sleep 1
    click 241 415
    sleep 1
    # Check pixel for a gift
    # if check_color 283 686 204 35 185 30 3 ; then
    if check_color 268 593 216 30 218 30 2 || check_color 283 686 204 35 185 30 2 ; then
        receive_gift
    else
        echo No gift present
        no_gift="true"
        sleep 1
    fi
    
    echo Send gift
    sleep 1
    printf "click:117,862,1,200\n" | tee $PIPE
    ## gift-s7:color:117,862,0xF6,0xD0,0x68
    sleep 2
    echo Check if not gift can be send
    # if check_color 150 519 232 128 181  ; then
    if check_color 138 854 182 167 172 15 1 || check_color 115 861 230 227 228 15 1 || check_color 113 859 213 213 213 15 1 ; then
        echo Do not send gift
        no_send="true"
        sleep 1
    else
        echo "Click send gift"
        click 111 870
        check_color 398 346 255 255 255 10 10
        click 398 346
        check_color 205 838 151 218 147 10 10
        click 365 840
        check_color 289 934 28 135 149 10 10
        click 289 934
    fi
    echo Go back to friend screen
    click 292 947
}

sort_has_gifts()
{
    printf "click:497,945,1,100\n" | tee $PIPE
    sleep 1
    printf "click:501,739,1,100\n" | tee $PIPE
    sleep 1
    if ! check_color 542 952 31 134 115 5
    then
        echo arrow up
        printf "click:497,945,1,100\n" | tee $PIPE
        sleep 1
        printf "click:501,739,1,100\n" | tee $PIPE
        sleep 1
    fi
    echo Sort has date
}

sort_can_receive()
{
    printf "click:497,945,1,100\n" | tee $PIPE
    sleep 1
    printf "click:501,839,1,100\n" | tee $PIPE
    sleep 1
    if ! check_color 542 952 31 134 115 5
    then
        echo arrow up
        printf "click:497,945,1,100\n" | tee $PIPE
        sleep 1
        printf "click:501,839,1,100\n" | tee $PIPE
        sleep 1
    fi
    echo Sort has date
}

main()
{
    
    back_home
    friends_page
    sort_has_gifts

    while true
    do
        no_gift="done"
        no_send="done"
        gift_cycle
        # return 1 if nothing to send and nothing to receive
        echo no_gift "$no_gift"
        echo no_send "$no_send"
        if [ "$open_limit_reached" == "true" ] ; then
            printf "############ Daily limit reached.\n"
            break
        fi
        
        if [[ "$no_gift" != "done" && "$no_send" != "done" ]]; then
            printf "############ Nothing to send nothing to get\n"
            break
        else
            printf "############ Continue sending gifts\n"
        fi
        wait_friend_page
    done

    printf "################### Change to send only\n"
    open_limit_reached="true"
    back_home
    friends_page
    sort_can_receive
    while true
    do
        no_gift="done"
        no_send="done"
        gift_cycle
        # return 1 if nothing to send and nothing to receive
        echo no_gift "$no_gift"
        echo no_send "$no_send"
        
        if [[ "$no_gift" != "done" && "$no_send" != "done" ]] ; then
            printf "############ Nothing to receive nothing to get\n"
            break
        else
            printf "############ Continue opening\n"
        fi
        # exit 0
        wait_friend_page
    done

    printf "Well done, all sent\n"
}
   
main 
