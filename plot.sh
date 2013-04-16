#!/bin/bash

path=$PWD

echo "set terminal postscript enhanced color" > ${path}/graphs/ggraphs.p
echo "set output '${path}/graphs/grades_temp.ps'" >> ${path}/graphs/graphs.p
echo "plot '"${path}/tetra_anneal_stats"' using 6:2 title 'boardGrade', '"${path}/tetra_anneal_stats"' using 6:3 title 'proposedGrade'" >> ${path}/graphs/graphs.p

echo "plot '"${path}/tetra_anneal_stats"' using 1:2 title 'boardGrade', '"${path}/tetra_anneal_stats"' using 1:3 title 'proposedGrade'" >> ${path}/graphs/graphs.p

echo "plot '"${path}/tetra_anneal_stats"' using 1:5 title 'swaps', '"${path}/tetra_anneal_stats"' using 1:3 title 'boardGrade'" >> ${path}/graphs/graphs.p

echo "set terminal postscript enhanced color" > ${path}/graphs/graphs.p
echo "set output '${path}/graphs/swaps_temp.ps'" >> ${path}/graphs/graphs.p
echo "plot '"${path}/tetra_anneal_stats"' using 6:5 title 'swaps', '"${path}/tetra_anneal_stats"' using 6:3 title 'boardGrade'" >> ${path}/graphs/graphs.p



gnuplot ${path}/graphs/grades_temp.p
