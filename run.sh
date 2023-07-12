# ---------------------------------------------- Databse and Pipeline Configuration
# export DB_HOST="" # Database host URL or IP
# export DB_PORT="" # Database port
# export DB_USER="" # Database username
# export DB_PASSWORD= # Database Password
# export DB_SCHEMA="" # Db schema for storing and dashboarding Alerts, eSentinel DB is used 
# export pipeline_id= # pipeline on which the model runs and generated events by deault is 607.

# ---------------------------------------------- Model Alert and Processing Configuration.

export RTSP_URL=sample.webm # Video source, webcam, rtsp or network feed
export INSIGHTS_UPDATE_MODE_TIME_INTERVAL=10 # in seconds Time interval after each successful db insert.
export SAVE_IMAGE=yes # yes/no to save alert images.
export SHOW_IMAGE=True # In boolean to See the output annotated result. 
export DIRECTORY_SAVE_IMAGE=OUT # Directory in which the alert images are saved.
export SAVE_INSIGHT=yes # yes/no to store the generated alerts in db
export SKIP_FRAMES=5 # Skips number of frames after processing.
# export MODEL_WEIGHT="" # Xmodel path for processing, by default yolov4_leaky_512_tf is used.
export ROI=[]
#[[234,312],[542,275],[947,366],[1274,435],[1275,714],[1015,716],[674,559],[297,405]] # Require co-ordinated in a list format, blank if there is no ROI
export MODEL_CONF=0.5 # Model Confidence on detection, below this neglects detection.

# ---------------------------------------------- MODEL RUN

# ./dist/run
python run.py