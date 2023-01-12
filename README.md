# sophon-sdk-init-scripts
> create soc-sdk/tpu-nntc and install debs based on release directory.<br>
> This program is tested on ubuntu20.04
# Usage
1. show help information
> $ python3 main.py --help

     SophonSDK init tool
    options:
      -h, --help            show this help message and exit
      -o OSTYPE, --ostype OSTYPE
                            target platform type
      -p PATH, --path [PATH]  the path of SophonSDK
      -n NNTC_PATH, --nntc-path [NNTC install path]
                            the install path for nntc sdk
      -s, --soc-sdk-create  create soc sdk 

2. Install libsophon,ffmpeg, opencv and tpu-nntc modules
```
python3 main.py -o x86_64 -p Release_221201-public -n tpu-nntc
```     
     
3. If you want to install soc sdk for cross compile, you should add -s or --soc-sdk-create option to command line, like this:
```commandline
python3 main.py -o x86_64 -p Release_221201-public -n tpu-nntc --soc-sdk-create
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
