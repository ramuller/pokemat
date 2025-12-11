# Schlumpiz
export SN_3001=ce091609f2237a1904
# Pokeralle
export SN_3007=ce091719d290250304
# White
export SN_3003=ce12160c4dac273705
# Gold
export SN_3004=ce0117119076d82a0c
# black 
export SN_3005=ce091609ec79190d04
# Broken dev
export SN_3006=ce11160bc1ce7d1705
# Gold from Eoija
export SN_3002=ce01182118d5b02a0c

# Aphex
export SN_3008=R58N648E8EX

my_args=$*
export my_args

# echo len now "${#my_args[@]}"
serial()
{
    if [[ "${#my_args[@]}" -eq 0 || "${my_args[0]}" = "" ]]; then
        echo "All" >&2
        adb devices |grep -v List | cut -f 1
    else
        
        for a in ${my_args[@]}; do
            a="SN_$a"
            echo -ne "${!a} "
        done
    fi
}
