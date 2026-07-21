. /etc/profile.d/00-customize.sh
POKEMAT=/home/ramuller/git/pokemat

addPath "$POKEMAT/bin"
addPath "$POKEMAT/pokemat"

export PYTHONPATH=:/home/ramuller/git/pokemat/lib
export PHONE_PORT=3001

