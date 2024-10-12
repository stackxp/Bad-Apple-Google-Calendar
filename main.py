import argparse, cv2, flask, websockets.sync.server as websockets, threading, os, time, logging, pathlib

parser = argparse.ArgumentParser(description="Hosts an HTTP and WebSocket server to play Bad Apple in Google Calendar!")
parser.add_argument("--video-path", type=pathlib.Path, required=True, help="The path to the video file")
parser.add_argument("--flask-host", type=str, default="0.0.0.0", help="The Flask host address")
parser.add_argument("--flask-port", type=int, default=8000, help="The Flask host port")
parser.add_argument("--ws-host", type=str, default="0.0.0.0", help="The WebSocket host address")
parser.add_argument("--ws-port", type=int, default=8001, help="The WebSocket host port")
parser.add_argument("--frame-delay", type=int, default=30, help="The delay between frames")
parser.add_argument("--flask-debug", action="store_true", help="Print Flask requests")
parser.add_argument("--debug", action="store_true", help="Print general debug messages")
parser.add_argument("--no-preview", action="store_true", help="Don't open a preview window")
args = parser.parse_args()

logger = logging.getLogger(__name__)
if args.debug:
	logger.setLevel(logging.DEBUG)

### FLASK HOSTING
def flask_server():
	app = flask.Flask(__file__)
	if not args.flask_debug:
		logging.getLogger("werkzeug").setLevel(logging.ERROR)

	@app.route("/")
	def index():
		return flask.send_file("./index.html")
	
	@app.route("/index_files/<path:path>")
	def files(path : str):
		if not os.path.exists("./index_files/" + path):
			return flask.Response(status=404)
		return flask.send_file("./index_files/" + path)
	
	@app.route("/badapple.js")
	def badapple():
		return flask.send_file("./badapple.js")
	
	app.run(args.flask_host, args.flask_port)

logger.debug("Starting Flask...")
threading.Thread(target=flask_server, daemon=True).start()

### WEBSOCKET SERVER
ws_client = None

def handler(conn : websockets.Connection):
	global ws_client
	if ws_client:
		conn.close(websockets.CloseCode.TRY_AGAIN_LATER)
		return
	
	logger.debug("Connected to WebSocket!")
	ws_client = conn

	while ws_client:
		time.sleep(1)

logger.debug("Starting WebSocket server...")
ws_server = websockets.serve(handler, args.ws_host, args.ws_port)
threading.Thread(target=ws_server.serve_forever, daemon=True).start()

### MAIN LOOP
while True:
	while not ws_client:
		time.sleep(1)
	
	# Get the wanted video size
	ws_video_size = [int(x) for x in ws_client.recv().strip().split(",")[0:2]]

	# Load the video file
	capture = cv2.VideoCapture(args.video_path)
	# TODO Add audio support

	while True:
		ok, frame = capture.read()
		if not ok:
			logger.debug("Couldn't read frame! (End of video?)")
			break
		if not args.no_preview:
			cv2.imshow("Preview", frame)
		
		# Scale down the frame and convert it to a string ("1100100101")
		frame = cv2.cvtColor(cv2.resize(frame, ws_video_size), cv2.COLOR_BGR2GRAY)
		data = ""
		for y in range(frame.shape[0]):
			for x in range(frame.shape[1]):
				data += "1" if frame[y][x] > 127 else "0"
		
		# TODO Add compression or smth, so that it doesn't send 1's and 0's as "1" and "0"
		ws_client.send(data)

		if cv2.waitKey(args.frame_delay) & 0xFF == ord("q"):
			logger.debug("Stopped playback by pressing Q!")
			break

	# Clean up
	capture.release()
	cv2.destroyAllWindows()
	ws_client.close()
	ws_client = None