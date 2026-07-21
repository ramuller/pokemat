# some useful macros
addManPath () { case "$MANPATH" in *$1*) ;; *) export MANPATH=$MANPATH:$1; esac }
addPath () { case "$PATH" in *$1*) ;; *) export PATH=$PATH:$1; esac }
addManPathHead () { case "$MANPATH" in *$1*) ;; *) export MANPATH=$1:$MANPATH; esac }
addPathHead () { case "$PATH" in *$1*) ;; *) export PATH=$1:$PATH; esac }


POKEMAT=/home/ramuller/git/pokemat
POKEMAT=/space/home/ralf/git/tmp/pokemat

addPathHead "$POKEMAT/bin"
addPathHead "$POKEMAT/pokemat"

export PYTHONPATH=:$POKEMAT/lib
export PHONE_PORT=3001

