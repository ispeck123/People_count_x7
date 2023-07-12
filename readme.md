Steps to execute the project.
Performs People count in a perticular video, if ROI is provided counts people in that perticular zone otherwise in entire.

1. Clone this repository into the edge box.
2. In a RDS or Local database create a schema and use eSentinel_new.sql to create the necessary tables.
3. Need to create a pipeline_id as per pipeline master table manually. Make sure to link the table with camera, model and pipeline_class_map to get the necessary data to create an alert.
Get and Set the pipeline id in run.sh file.
4. If there is an requirement of ROI insert into ROI or leave as a blank list. 
5. determine the ROI by zoning_tool.py
6. Requires pretrained yolov4_leaky_512_tf xmodel in /usr/share/vitis-ai-library, pease download it before running the project.
7. execute the run file through sh run.sh to execute the project.