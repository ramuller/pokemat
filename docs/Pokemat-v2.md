# Pokemon go automation POKEMAT

## Goal

Pokemon GO is a greate game with nice interactive parts but also some boring parts such as sending/receiving gifts or trading pokemons in a large amount.

The job of POKEMAT is to offload the boring tasks from the trainer.

## Overview

POKEMAT is a set of commandline tools to perform certain jobs, like send gifts to friends. POKEMAT is running on a Linux PC and connnects to phone over IP based network connection


POKEMAT is using a patched version of [scrpy](https://github.com/Genymobile/scrcpy) to interact with the phone.


POKEMAT can handle as much phones as the master can handle

Perhaps a user interface for dummies (GUI) would be nice but perhaps in Version 2


## The scrcpy modification

Primary scrcpy has human interface but no machine 2 machine (m2m) interface to interact with tools like POKEMAT.

A REST interface has been added to provide some functionality to interact with a machine
Input screen taps or read the color of a pixel or the resolution of the phones display window.

POKEMAT is working with the resolution of scrcpy NOT the resolution of the phone!

REST API

coming:(


### architecture








