#!/bin/bash

if [ $# -ne 1 ]; then
    echo give pipe arg
    exit 1
fi

export PORT="$1"


get_rgb()
{

    if [ $# -lt 2 ] ; then
        echo get_rgb needs  x y 
        echo "Got count $# '$@'" 
        exit 1
    fi
    printf "color:$1,$2\n" >$PORT
    sleep 1
    values="$(tail -n 1 ${PIPE}.sh | sed "s/.*color://")"
    rgb=($(echo $values |cut -d ',' -f 3) $(echo $values |cut -d ',' -f 4) $(echo $values |cut -d ',' -f 5))
    echo RGB ${rgb[@]}
}

check_color()
{
    if [ $# -ne 6 ] ; then
        echo check_color needs  x y r g b threshold
        echo "Got count $# '$@'" 
        exit 
    fi
    x=$1;  y=$2
    r=$3;  g=$4 ; b=$5
    t=$6
    echo "check color : ${@}"
    get_rgb $x $y
    if [[ \
          ${rgb[0]} -lt $(( r + t ))  && ${rgb[1]} -lt $(( g + t ))  && ${rgb[2]} -lt $(( b + t  )) && \
          ${rgb[0]} -gt $(( r - t ))  && ${rgb[1]} -gt $(( g - t ))  && ${rgb[2]} -gt $(( b - t  ))
       ]]
    then
        echo "Color match"
        return 0
    else
        echo "Collor miss"
        return 1
    fi

}

back_home()
{
    echo "Back home"
    sleep 1
    get_rgb 285 916
    while [[ ${rgb[0]} -lt 255 && ${rgb[1]} -gt 100 && ${rgb[2]} -gt 100 ]]
    do
        echo Not home color ${rgb[@]}
        sleep 1
        get_rgb 285 916
        if [[ ${rgb[0]} -lt 255 && ${rgb[1]} -gt 100 && ${rgb[2]} -gt 100 ]]; then
            echo Send home screen step bak
            printf "click:290,945,3,200\n" | tee $PORT
        fi
        get_rgb 285 916
        echo Not home color ${rgb[@]}
    done
}

receive_gift()
{
    echo Do not send gift
    if [ "$open_limit_reached" != "true" ]
    then
        printf "############# Open gift"
        printf "click:250,831,1,200\n" | tee $PORT
        ## gift-send:color:218,831,0xFF,0xD0,0xF9
        ## gift-send:color:218,831,255,208,249
        # sleep 1
        sleep 4
        echo press open
        printf "click:291,853,1,200\n" | tee $PORT
        ## gift-send:color:291,853,0x84,0xD4,0xA5
        ## gift-send:color:291,853,132,212,165
        sleep 2
        if check_color 150 519 232 128 181 10 ; then
            echo Limit reached
            printf "click:290,945,3,200\n" | tee $PORT
            sleep 1
            no_gift="true"
            open_limit_reached="true"
        else
            printf "click:291,853,1,200\n" | tee $PORT
            ## gift-send:color:165,885,0xD4,0xFD,0xDF
            ## gift-send:color:165,885,212,253,223
            sleep 1
            printf "button_up:165,885,1,200\n" | tee $PORT
            sleep 0
            printf "button_down:165,885,1,200\n" | tee $PORT
            ## gift-send:color:165,885,0xF3,0xE7,0xD0
            ## gift-send:color:165,885,243,231,208
            sleep 0
            printf "button_up:165,885,1,200\n" | tee $PORT
            sleep 1
            printf "button_down:165,885,1,200\n" | tee $PORT
            ## gift-send:color:165,885,0xF3,0xE7,0xD0
            ## gift-send:color:165,885,243,231,208
            sleep 0
            printf "button_up:165,885,1,200\n" | tee $PORT
            sleep 0
            printf "button_down:165,885,1,200\n" | tee $PORT
            ## gift-send:color:165,885,0xF3,0xE7,0xD0
            ## gift-send:color:165,885,243,231,208
            # sleep 1
            # printf "button_up:165,885,1,200\n" | tee $PORT
            # sleep 0
            # printf "button_down:165,885,1,200\n" | tee $PORT
            ## gift-send:color:165,885,0xF3,0xE7,0xD0
            ## gift-send:color:165,885,243,231,208
            sleep 0
            printf "button_up:165,885,1,200\n" | tee $PORT
            sleep 1
            printf "button_down:165,885,1,200\n" | tee $PORT
            ## gift-send:color:165,885,0xF3,0xE7,0xD0
            ## gift-send:color:165,885,243,231,208
            sleep 0
            printf "button_up:165,885,1,200\n" | tee $PORT
            sleep 0
            printf "button_down:165,885,1,200\n" | tee $PORT
            ## gift-send:color:165,885,0xF3,0xE7,0xD0
            ## gift-send:color:165,885,243,231,208
            sleep 1
            printf "button_up:165,885,1,200\n" | tee $PORT
            sleep 0
            printf "button_down:165,885,1,200\n" | tee $PORT
            ## gift-send:color:165,885,0xF3,0xE7,0xD0
            ## gift-send:color:165,885,243,231,208
            sleep 0
            printf "button_up:165,885,1,200\n" | tee $PORT
            sleep 2
            printf "button_down:165,885,1,200\n" | tee $PORT
            ## gift-send:color:165,885,0xFF,0xE9,0xED
            ## gift-send:color:165,885,255,233,237
            sleep 1
            printf "button_up:165,885,1,200\n" | tee $PORT
            sleep 2
        fi
    else
        echo limit reached don not open
        printf "click:289,950,1,100\n" | tee $PORT
        sleep 1
    fi
}

friends_page()
{
    echo Go to friend page
    # click avatar
    printf "click:75,925,1,200\n" | tee $PORT
    sleep 3
    # click friends
    printf "click:291,100,1,200\n" | tee $PORT
    ## gift-s7:color:75,925,0x1A,0x13,0x0A
    # don't wait forever
    timeout=12
    while ! check_color 285 182 255 255 255 5 ; do
        $(( timeout = timeout -1 ))
        echo "Countdown $timeout"
        if [ $timeout -le 0 ]; then
            echo Timeout exit
            exit 1
        fi
        echo Wait for tainer screen
        sleep 0.5
    done
    
}
gift_cycle()
{
    # check which round
    # Search trainer
    # type dela
    if check_color 515 244 12 202 165 5
    then
        echo "second round"
        printf "click:515,244,1,200\n" | tee $PORT
        sleep 0.5
        printf "click:489,239,1,200\n" | tee $PORT
        sleep 3
    else
        echo Frist round more delay
        printf "click:489,239,1,200\n" | tee $PORT
        sleep 3
    fi
    printf "key:\!\n" | tee $PORT
    sleep 0
    printf "key:f\n" | tee $PORT
    sleep 0
    printf "key:f\n" | tee $PORT
    sleep 0.5
    printf "button_down:488,583,1,200\n" | tee $PORT
    ## gift-s7:color:488,583,0xFF,0xFF,0xFF
    sleep 0
    printf "button_up:491,582,1,200\n" | tee $PORT
    sleep 3
    printf "button_down:241,415,1,200\n" | tee $PORT
    ## gift-s7:color:241,415,0xFF,0xFF,0xFF
    sleep 0
    printf "button_up:241,415,1,200\n" | tee $PORT
    sleep 3
    # Check pixel for a gift
    # sleep 2
    get_rgb 288 706
    if [[ ${rgb[0]} -gt 200 && ${rgb[1]} -lt 100 && ${rgb[2]} -gt 175 ]]
    then
        receive_gift
    else
        echo no gift
        no_gift="true"
    fi
    


    echo Send gift
    printf "click:117,862,1,200\n" | tee $PORT
    ## gift-s7:color:117,862,0xF6,0xD0,0x68
    sleep 2
    echo Check if not gift can be send
    if check_color 150 519 232 128 181 10 ; then
        echo Do not send gift
        no_send="true"
    else
        printf "button_down:314,383,1,200\n" | tee $PORT
        ## gift-s7:color:314,383,0xB6,0xB3,0x65
        sleep 0
        printf "button_up:314,383,1,200\n" | tee $PORT
        sleep 3
        printf "button_down:285,843,1,200\n" | tee $PORT
        ## gift-s7:color:285,843,0x84,0xD4,0xA5
        sleep 0
        printf "button_up:285,843,1,200\n" | tee $PORT
        sleep 5
        # printf "button_down:292,947,1,200\n" | tee $PORT
        ## gift-s7:color:292,947,0x3D,0x79,0x75
        # sleep 0
        # printf "button_up:292,947,1,200\n" | tee $PORT
    fi
    echo echo friend screen
    printf "click:292,947,1,200\n" | tee $PORT
}

main()
{
    while true
    do
        back_home
        friends_page
        no_gift="done"
        no_send="done"
        gift_cycle
        # return 1 if nothing to send and nothing to receive
        echo no_gift "$no_gift"
        echo no_send "$no_send"
        
        if [[ "$no_gift" != "done" && "$no_send" != "done" ]] ; then
            echo Nothing to send nothing to get
            exit 1
        fi
        # exit 0
    done
}
   
main 
