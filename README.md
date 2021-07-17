# Bird Classifier
:triumph: :triumph:  :triumph: Ongoing..... :triumph: :triumph: :triumph:

# Why?
- This Project is part of adventure of me and my friend trying to explore ML , API 
- To create a platform for detecting any kind of bird that is known to man
- To try creating a platform that end-user could train YOLOv5's model to detect bird with simple-to-use API
- To create an endpoint for detecting bird with one simple script

# Developer's Note
- Now working on writing web scraping scripts that could be used on CMD 
- Exploring ideas and structures to make Bird_Classifier one complete platform on-the-go
- GCP is very useful for deployment
- I'm confident enough that Docker Container is not so hard to use

# understanding my messy code
- yolo_detect.py : Based on [MY OLD word](https://github.com/RioRocker97/my_yolov5) which it loosely based on [YOLOv5](https://github.com/ultralytics/yolov5/blob/master/detect.py). it not perfect but it get the detection process done.
- webhook.py : proposed scripts for running bot-server that could be used in LINE uOA
- extract.py : lazy web scraping scripts that use full static HTML file from yandex.com to extract birb pictures
- bird-engine.py : proposed scripts for running fully-function Web-API for bird_classifier.