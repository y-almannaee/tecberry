* leader.py checks   
	* NAME for the name of the website: String
	* OPT_OUT_TELEMETRY to opt out of telemetry: Any string will opt you out
	* AUTH_LOCATIONS for authenticator folder location: String(filepath from root)
	* REDIS_HOST for the hostname of the Redis DB: String(hostname, no port)
	* REDIS_PORT for the port of the Redis DB: String(port number, should decode to integer)
	* LOGGING_FILE for the logfile location: String(logging file location from root)
	* LOGGING_DEBUG for loglevel: String(logging level, should decode to integer)

* To set up the touchscreen
	* https://die-antwort.eu/techblog/2017-12-setup-raspberry-pi-for-kiosk-mode/

* To set up the camera
``
ffmpeg \
    -f video4linux2 -framerate 15 -video_size 640x480 -i /dev/video0 \
    -c:v libx264 -b:v 1600k -preset ultrafast \
    -x264opts keyint=50 -g 25 -pix_fmt yuv420p \
    -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf: \
text='%{localtime\:%Y-%m-%dT%T}': fontcolor=white@0.8: fontsize=16: x=10: y=10: box=1: boxcolor=black: boxborderw=6" \
    -f flv "rtmp:localhost:4935/live/cam1?streamkey=5555f6f63737"
``

* To run wg wg-quick up wg_ubuntu