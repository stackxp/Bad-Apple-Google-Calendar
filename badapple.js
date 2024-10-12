const onColor = "#1A73E8"
const calendarSize = [4, 4]
const screenSize = [calendarSize[0] * 7, calendarSize[1] * 6]
const wsHost = `ws://${window.location.hostname}:8001`
let pixels
let wsConn

function updatePixels(newPixels) {
	for (let index in newPixels) {
		if (index >= pixels.length)
			break
		pixels[index].style.background = newPixels[index] == "0" ? onColor : "none"
		pixels[index].style.color = newPixels[index] == "0" ? "white" : ""
	}
}

function init() {
	let tempPixels = Array.from(document.querySelectorAll(".AOhf0c .nUt0vb.sOjuj"))
	pixels = []
	
	for (let row = 0; row < calendarSize[1]; row++) {
		for (let weekOffset = 0; weekOffset < 6; weekOffset++) {
			for (let column = 0; column < calendarSize[0]; column++) {
				pixels.push(...tempPixels.slice(42 * calendarSize[1] * row + 42 * column + weekOffset * 7, 42 * calendarSize[1] * row + 42 * column + weekOffset * 7 + 7))
			}
		}
	}
	for (let pixel of pixels) {
		pixel.style.background = "#1A73E8"
		pixel.style.color = "white"
	}
}

function run() {
	wsConn = new WebSocket(wsHost)
	wsConn.onmessage = (message) => updatePixels(message.data)
	wsConn.onopen = () => {
		console.log("Connected to WebScoket!")
		wsConn.send(screenSize.join())
	}
}

let testIndex = 0
function testPixels() {
	let pixelArray = new Array(pixels.length).fill("0")
	pixelArray[testIndex] = "1"
	updatePixels(pixelArray.join(""))

	testIndex++

	if (testIndex >= pixels.length)
		return
	setTimeout(testPixels, 100)
}