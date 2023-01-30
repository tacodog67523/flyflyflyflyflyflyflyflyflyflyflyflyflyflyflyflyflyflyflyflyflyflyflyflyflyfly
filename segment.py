from ibm import Imbtts, wrap, Voices
import os, time, concurrent.futures, requests, base64

uuu = "0.tcp.ngrok.io:10496"
voice = Voices.michael_expressive
corrections = lambda x: x.replace("chapter", "chapter ").replace("CHAPTER", "CHAPTER ").replace("OceanofPDF.com", "").replace("OceanofPDF .com", "").replace("OceanofPDF", "").replace("«", "").replace("»", "").replace("ﬀ", "")
ibb = None
def get():

	ibb = Imbtts()
	
	

	while True:
		t = time.time()
		try:
			data, name = requests.get("http://"+uuu+"/next/").json()
			az = os.path.join("/tmp/", name+".mp3")
			size = ibb.download(ibb.chunck(wrap( corrections( base64.b64decode(data.encode("utf-8")).decode("utf-8") ) )), az, voice)

			os.system(f'(curl -s -i -X POST -H "Content-Type: multipart/form-data" -F "file=@{az}" {uuu}/submit && rm "{az}") &')
			print(name, time.time()-t)
		except Exception as e:
			print(e)
			while True:
				try:
					ibb = Imbtts()
					break
				except: time.sleep(3)
	

if __name__ == "__main__":
	# get()
	with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
		for _ in range(3):
			executor.submit(get)
