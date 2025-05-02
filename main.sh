# Just a convenient way to launch the SSG
outputdir="public"
python3 src/main.py $outputdir && cd $outputdir && python3 -m http.server 8888