click()
{
    if [ $USE_IP -eq 1 ] ; then
 	  raw_data="$(curl --silent http://localhost:$PORT/v1/click:$1,$2)"
 	  get_rgb $1 $2 
    else
    	echo click:$1,$2,1,30 >$PORT
    	echo click:$1,$2,1,30
    	sleep 0.04
    fi
}

motion()
{
    echo motion:$1,$2
    if [ $USE_IP -eq 1 ] ; then
       curl --silent http://localhost:$PORT/v1/motion:$1,$2 
    else
        echo motion:$1,$2 >$PORT
    fi
}

key()
{
    if [ $USE_IP -eq 1 ] ; then
        curl --silent http://localhost:$PORT/v1/key:$1
    else
        echo "key:$1" >$PORT
    fi
}

button_up()
{
    if [ $USE_IP -eq 1 ] ; then
        curl --silent http://localhost:$PORT/v1/button_up:$1,$2,1,50
    else
        echo button_up:$1,$2,1,50 >$PORT
    fi
}

button_down()
{
    if [ $USE_IP -eq 1 ] ; then
        curl --silent http://localhost:$PORT/v1/button_down:$1,$2,1,50
    else
        echo button_down:$1,$2,1,50 >$PORT
    fi
}

start_trade()
{
    click 494,849
}

get_friend()

{
    click 59 931 1
    sleep  0.5
    click 475 236 1
}


get_rgb()
{

    if [ $# -lt 2 ] ; then
        echo get_rgb needs  x y 
        echo "Got count $# '$@'" 
        exit 1
    fi
    if [ $USE_IP -eq 1 ] ; then
 	    raw_data="$(curl --silent http://localhost:$PORT/v1/color:$x,$y)"
        [ -z "$DEBUG" ] || echo raw_dat $raw_data
 	    rgb=($(echo "$raw_data" | jq -r '.red') $(echo "$raw_data" | jq -r '.green')  $(echo "$raw_data" | jq -r '.blue'))
    else
    	printf "color:$1,$2\n" >$PORT
    
    	sleep 0.75
    	values="$(tail -n 1 ${PORT}.sh | sed "s/.*color://")"
    	echo RGB values = $values
    	rgb=($(echo $values |cut -d ',' -f 3) $(echo $values |cut -d ',' -f 4) $(echo $values |cut -d ',' -f 5))
    fi
    [ -z "$DEBUG" ] || echo RGB ${rgb[@]}
}

check_color()
{
    max=3
    if [[ $# -ne 6 && $# -ne 7 ]] ; then
        echo check_color needs  x y r g b threshold
        echo "Got count $# '$@'" 
        return 1
    fi
    x=$1;  y=$2
    r=$3;  g=$4 ; b=$5
    t=$6
    [ $# -eq 7 ] && max=$7
    
    echo "check color : ${@}"
    for (( i = 0; i < $max; i++ )); do
        echo "RGB round $i"
        get_rgb $x $y
        echo $r,$g,$b t=$t ${rgb[0]},${rgb[1]},${rgb[2]}
        if [[ ${rgb[0]} -lt $(( r + t ))  && ${rgb[1]} -lt $(( g + t ))  && ${rgb[2]} -lt $(( b + t  )) &&  ${rgb[0]} -gt $(( r - t ))  && ${rgb[1]} -gt $(( g - t ))  && ${rgb[2]} -gt $(( b - t  )) ]]
        then
            echo "Color match"
            return 0
        fi
    done
    echo "Color miss"
    return 1
}

wait_color()
{
    timeout=10
    [ -z "$7" ] || timeout=$(( $7 * 1 ))
    
    while ! check_color $1 $2 $3 $4 $5 $6 1
    do
        echo Waiting for RGB $3 $4 $5 thres $6
        # sleep 0.5 
        timeout=$(( timeout - 1 ))
        if [ $timeout -le 0 ]; then
            false
            return
        fi
    done
    true
    return
}

wait_color_fail()
{
    while check_color $1 $2 $3 $4 $5 $6
    do
        echo Waiting for RGB $3 $4 $5 thres $6
        sleep 0.5
    done
}

click_ok()
{
    click 237 898 1
}

# click 237 898 1
go_battle()
{
    click 285 945
    sleep 1
    click 458 547 1
    sleep 1
}

fight()
{
    # while sleep 0.01
    while ! check_color 285 182 0 0 0 5
    do
        click 245 890
        click 145 890

        click 164 821 1

        for (( x = 50; x < 450 ; x += 130 ))
        do
            check_color 285 182 0 0 0 5 || return
            for (( y = 520; y < 777; y += 130 ))
            do
                click $x $y
            done
            click 164 821 1
        done        
    done
}

back_home()
{
    echo "Back home"
    sleep 1
    # get_rgb 285 916
    # while [[ ${rgb[0]} -lt 255 && ${rgb[1]} -gt 100 && ${rgb[2]} -gt 100 ]]
    while ! check_color 285 916 245 55 72 20 1
    do
    	get_rgb 285 916
        echo Not home color ${rgb[@]}
        sleep 1
        get_rgb 285 916
        click 285 945
        if check_color 285 916 254 55 72 10
        then
           echo Send home screen step bak
           # click 275 945
        fi
        # get_rgb 285 916
        echo Not home color ${rgb[@]}
    done
}

if [ $# -ne 1 ]; then
    echo give pipe arg
fi

export PORT="$1"

USE_IP=0
echo $PORT | grep --silent "/tmp" || USE_IP=1
echo Use IP : $USE_IP
