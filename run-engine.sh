#!/bin/bash
PATH=/home/j/bin:/home/j/.local/bin:/home/j/miniconda3/bin:/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin
cd /home/j/scraper/scrape_earnings
source /home/j/miniconda3/etc/profile.d/conda.sh
source activate scraper
python motley_engine.py
