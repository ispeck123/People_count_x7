/*
 * Copyright 2019 Xilinx Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <iostream>
#include <opencv2/opencv.hpp>
#include <vitis/ai/yolov3.hpp>


#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

using namespace std;
using namespace cv;
namespace py = pybind11;
PYBIND11_MAKE_OPAQUE(std::vector<vitis::ai::YOLOv3Result::BoundingBox>);


std::unique_ptr<vitis::ai::YOLOv3> det;
std::vector<vitis::ai::YOLOv3Result::BoundingBox> vitis_ai_lib_yolo_run(py::buffer input,string model_file) {
  if(model_file == "again")
    ;
  else
    det = vitis::ai::YOLOv3::create(model_file, true);
  
  py::buffer_info buf = input.request();
  if (buf.ndim != 3)
    throw std::runtime_error("3-channel image must be 3 dims ");
  Mat image(buf.shape[0], buf.shape[1], CV_8UC3, (unsigned char*)buf.ptr);
  auto results = det->run(image);

  //auto yolo = vitis::ai::YOLOv3::create(argv[1], true);

  //  auto yolo =
  //    vitis::ai::YOLOv3::create(xilinx::ai::YOLOV3_VOC_416x416_TF, true);

  return results.bboxes;
}



PYBIND11_MODULE(yolov4_runner0, m) {
    m.doc() = "pybind11 vitis ai library yolo plugin"; // optional module docstring

    PYBIND11_NUMPY_DTYPE(vitis::ai::YOLOv3Result::BoundingBox, x, y, width, height, label, score);
    py::class_<vitis::ai::YOLOv3Result::BoundingBox>(m, "BoundingBox")
        .def_readwrite("x",&vitis::ai::YOLOv3Result::BoundingBox::x)
        .def_readwrite("y",&vitis::ai::YOLOv3Result::BoundingBox::y)
        .def_readwrite("width",&vitis::ai::YOLOv3Result::BoundingBox::width)
        .def_readwrite("height",&vitis::ai::YOLOv3Result::BoundingBox::height)
        .def_readwrite("label",&vitis::ai::YOLOv3Result::BoundingBox::label)
        .def_readwrite("score",&vitis::ai::YOLOv3Result::BoundingBox::score);

    py::bind_vector<std::vector<vitis::ai::YOLOv3Result::BoundingBox>>(m, "VectorBBox", py::buffer_protocol());

    m.def("run", &vitis_ai_lib_yolo_run);
   // m.def("refindet_demo", &refindet_demo, py::return_value_policy::reference);

    
}



/*
source ~/petalinux_sdk_2022.1/environment-setup-cortexa72-cortexa53-xilinx-linux
cd /home/zee/zee_wps/Vitis-AI/examples/Vitis-AI-Library/samples/yolov4
sh build.sh
sudo scp /home/zee/zee_wps/Vitis-AI/examples/Vitis-AI-Library/samples/yolov4/test_performance_yolov4 root@192.168.1.223:~/Vitis-AI/samples/yolov4
sudo scp -r ./libyolov4   root@192.168.1.223:/usr/lib/python3.9/site-packages/

./test_jpeg_yolov4 face_mask_detection_pt sample_yolov4.jpg

$CXX -std=c++17 -O2 -I"/home/zee/petalinux_sdk_2022.1/sysroots/cortexa72-cortexa53-xilinx-linux/usr/include/python3.9/" -o test_refinedet test_refinedet.cpp -lvitis_ai_library-refinedet -lvitis_ai_library-dpu_task -lvitis_ai_library-xnnpp -lvitis_ai_library-model_config -lvitis_ai_library-math -lvart-util -lxir -pthread -ljson-c -lglog ${OPENCV_FLAGS} -lopencv_core -lopencv_videoio -lopencv_imgproc -lopencv_imgcodecs -lopencv_highgui

 */
