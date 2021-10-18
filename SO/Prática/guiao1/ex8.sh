#!/bin/bash

z()
{
    case $# in
        0) echo "No arguments were given";;
        1) echo "One argument was given";;
        2|3) echo "Two or three arguments were given";;
        *) echo "More than three arguments were given";;
    esac
}
z
z aa
z aa bb
z aa bb cc
z aa bb cc dd
z aa bb cc dd ee
