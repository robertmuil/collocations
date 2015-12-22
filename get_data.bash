#!/bin/bash
#TODO: use a makefile

pushd data
if [ ! -f "Conrad, Joseph - Heart of Darkness - pg526.txt" ]; then
	wget "http://www.gutenberg.org/cache/epub/526/pg526.txt"
	mv -v "pg526.txt" "Conrad, Joseph - Heart of Darkness - pg526.txt"
fi
popd
