# SmartController
 使用AWS IOT、GreenGrass結合樹梅派、紅外線發射器，來並透過Rotation Encoder或語音來控制Hue和傳統紅外線家電(控制器與GateWay部分，缺少紅外線部分)
	1. 所需設備
		1. Raspberry Pi and rotation encoder
		2. AWS IOT
		3. GreenGrass
		4. Amazon Lex
		5. Snowboy Hotword Detection
	2. 程式功能
		1. Controller部分
			1. 檢測有無連線
				1. 若有連線，使用GreenGrass(雲端)來控制Rotation Encoder(雲端控制的程式碼缺)
				2. 若無連線，使用本地端GPIO來控制Rotation Encoder
			2. 啟動GreenGrass和Shadow
			3. 啟動Hotword檢測
		2. Gateway
			1. 檢測有無連線
				1. 若有連線，使用GreenGrass(雲端)來控制
				2. 若有連線，使用GreenGrass使用(本地端)來控制
	3. 如何通訊
		1. 將各個裝置設在同個GreenGrass群組間，彼此利用AWS IOT的MQTT來進行通訊
		2. 利用Shadow控制設備狀態
	4. 	各程式功能
		1. RPiController(Android):撰寫一個APP透過RESTful的方法來獲取Hue的控制金鑰，並結合AWS IOT的MQTT功能方便獲取各控制組件的傳輸log(憑證已過期，無法使用)
		2. Controller(Raspberry):控制器的程式，檢測有無網路、啟動GreenGrass、HotWord Detection、語音溝通(憑證已過期，無法使用)
			1. app_start.sh:樹梅派開機所需要執行的指令
			2. config.py:基於RaspiWiFi來修改成所需要的功能(新增寫入Hue Key)並且寫成config.py，包含SSID、Password、Hue Key
			RaspiWiFi: https://github.com/jasbur/RaspiWiFi
			3.  main.py:主程式
		3. Gateway(Raspberry):Gateway的程式，存放GreenGrass的一切功能(群組、離線控制)(憑證已過期，無法使用)
			1. main.py:主程式
		