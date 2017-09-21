#!/bin/bash

shuf worldcitiespop.txt | shuf | head -n 100 > random_coords.txt
