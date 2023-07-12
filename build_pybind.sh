#
# Copyright 2019 Xilinx Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

result=0 && pkg-config --list-all | grep opencv4 && result=1
if [ $result -eq 1 ]; then
	OPENCV_FLAGS=$(pkg-config --cflags --libs-only-L opencv4)
else
	OPENCV_FLAGS=$(pkg-config --cflags --libs-only-L opencv)
fi

CXX=${CXX:-g++}


#$CXX -std=c++17 -O2 -I. -I"/home/zee/petalinux_sdk/sysroots/cortexa72-cortexa53-xilinx-linux/usr/include/python3.9/" -o test_refinedet test_refinedet.cpp -lvitis_ai_library-refinedet -lvitis_ai_library-dpu_task -lvitis_ai_library-xnnpp -lvitis_ai_library-model_config -lvitis_ai_library-math -lvart-util -lxir -pthread -ljson-c -lglog ${OPENCV_FLAGS} -lopencv_core -lopencv_videoio -lopencv_imgproc -lopencv_imgcodecs -lopencv_highgui
$CXX -std=c++17 -fPIC -O3 -Wall -shared -I"/home/zee/petalinux_sdk_2022.1/sysroots/cortexa72-cortexa53-xilinx-linux/usr/include/python3.9/" \
-o ./libyolov4/yolov4_runner0.so pybind_yolov4.cpp -lvitis_ai_library-yolov3 \
-lvitis_ai_library-dpu_task -lvitis_ai_library-xnnpp -lvitis_ai_library-model_config -lvitis_ai_library-math -lvart-util -lxir -pthread -ljson-c -lglog ${OPENCV_FLAGS} -lopencv_core \
-lopencv_videoio -lopencv_imgproc -lopencv_imgcodecs -lopencv_highgui