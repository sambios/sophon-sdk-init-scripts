# sophon-sdk-init-scripts
> create soc-sdk/tpu-nntc and install debs based on release directory.<br>
> This program is tested on ubuntu20.04 <br>
> SophonSDK based on libncurses5-dev, you should install it at first. <br>
> ``` $ sudo apt install libncurses-dev ```
# Usage
1. show help information
> $ python3 main.py --help

2. Install libsophon,ffmpeg, opencv and tpu-nntc modules
```
python3 main.py -o x86_64 -p Release_221201-public -i sgnnsdk
```     
     
3. If you want to install soc sdk for cross compile, you should add -s or --install-soc-sdk option to command line, like this:
```commandline
python3 main.py -o x86_64 -p Release_221201-public -i sgnnsdk --install-soc-sdk
```
4. After install, the tree of install directory will be like this:
```commandline
..
├── soc-sdk
│   └── opt
│       └── sophon
│           ├── driver-0.4.4
│           ├── libsophon-0.4.4
│           ├── libsophon-current -> libsophon-0.4.4
│           ├── sophon-ffmpeg_0.5.1
│           ├── sophon-ffmpeg-current -> sophon-ffmpeg_0.5.1
│           ├── sophon-opencv_0.5.1
│           ├── sophon-opencv-current -> sophon-opencv_0.5.1
│           ├── sophon-sample_0.5.1
│           └── sophon-sample-current -> sophon-sample_0.5.1
└── tpu-nntc
    ├── bin
    ├── doc
    ├── include
    ├── kernel
    ├── lib
    ├── scripts
    └── wheel
    ...
```
5. Enjoy!
