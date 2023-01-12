import ast
import shutil
import config
import os
import argparse


def op_cmd(cmd):
    print(cmd)
    os.system(cmd)


def get_module_version(mod_path, mod_name):
    mod_version = 'unknown'
    d1_dirs = os.listdir(mod_path)
    for d1_dir in d1_dirs:
        if d1_dir.startswith(mod_name):
            if d1_dir.endswith('aarch64.tar.gz'):
                mod_version = d1_dir.replace('_aarch64.tar.gz', '').split('_')[-1]
                break
            elif d1_dir.endswith('x86_64.tar.gz'):
                mod_version = d1_dir.replace('_x86_64.tar.gz', '').split('_')[-1]
                break
            elif d1_dir.endswith('.tar.gz'):
                mod_version = d1_dir.replace('.tar.gz', '').split('_')[-1]
                break

    return mod_version


def module_path_pcie(sdk_path, module_name):
    d1_dirs = os.listdir(sdk_path)
    mod_version = ''
    mod_path = ''
    for d1_dir in d1_dirs:
        if not d1_dir.startswith(module_name):
            continue
        mod_path = os.path.join(sdk_path, d1_dir)
        mod_version = get_module_version(mod_path, module_name)
        break

    return mod_path, mod_version


def module_path_soc(sdk_path, module_name):
    d1_dirs = os.listdir(sdk_path)
    mod_version = ''
    mod_path = ''
    for d1_dir in d1_dirs:
        if not d1_dir.startswith(module_name):
            continue
        mod_path = os.path.join(sdk_path, d1_dir)
        # for SOC mode
        if module_name == 'sophon-img':
            module_name = 'libsophon'
        mod_version = get_module_version(mod_path, module_name)
        break

    return mod_path, mod_version


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='SophonSDK init tool')
    parser.add_argument('-o', '--ostype', default=config.ARCH_TYPE, help='target platform type')
    parser.add_argument('-p', '--path', default=config.RELEASE_ROOT, help='the path of SophonSDK')
    parser.add_argument('-n', '--nntc-path', default='tpu-nntc', help='the install path for nntc sdk')
    parser.add_argument('-s', '--soc-sdk-create', action='store_true', help='create soc sdk')

    args = parser.parse_args()
    print(args)

    ostype = args.ostype
    sdk_path = args.path
    nntc_sdk_path = args.nntc_path
    is_create_soc_sdk = args.soc_sdk_create

    if ostype == "x86_64":
        # libsophon runtime
        module_path, module_version = module_path_pcie(sdk_path, 'libsophon')
        print("Detected libsophon version: {}".format(module_version))
        cmd = "cd {} && sudo dpkg -i sophon-libsophon_{}_amd64.deb"
        cmd2 = cmd.format(module_path, module_version)
        op_cmd(cmd2)

        # libsophon dev
        cmd = "cd {} && sudo dpkg -i sophon-libsophon-dev_{}_amd64.deb"
        cmd2 = cmd.format(module_path, module_version)
        op_cmd(cmd2)

        # sophon-mw
        module_path, module_version = module_path_pcie(sdk_path, 'sophon-mw')
        print("Detected sophon-mw version: {}".format(module_version))
        # ffmpeg runtime
        cmd = "cd {} && sudo dpkg -i sophon-mw-sophon-ffmpeg_{}_amd64.deb"
        cmd2 = cmd.format(module_path, module_version)
        op_cmd(cmd2)
        # ffmpeg dev
        cmd = "cd {} && sudo dpkg -i sophon-mw-sophon-ffmpeg-dev_{}_amd64.deb"
        cmd2 = cmd.format(module_path, module_version)
        op_cmd(cmd2)

        # opencv runtime
        cmd = "cd {} && sudo dpkg -i sophon-mw-sophon-opencv_{}_amd64.deb"
        cmd2 = cmd.format(module_path, module_version)
        op_cmd(cmd2)
        # opencv dev
        cmd = "cd {} && sudo dpkg -i sophon-mw-sophon-opencv-dev_{}_amd64.deb"
        cmd2 = cmd.format(module_path, module_version)
        op_cmd(cmd2)

        # tpu-nntc
        # get nntc name
        module_path, module_version = module_path_pcie(sdk_path, 'tpu-nntc')
        print("Detected tpu-nntc version: {}".format(module_version))
        if os.path.exists(nntc_sdk_path):
            shutil.rmtree(nntc_sdk_path)
        os.mkdir(nntc_sdk_path)
        cmd = "sudo tar zxf {}/tpu-nntc_{}.tar.gz -C {} && cp -fr {}/tpu-nntc_{}/* {}/ && " \
              "rm -fr {}/tpu-nntc_{}"
        cmd2 = cmd.format(module_path, module_version, nntc_sdk_path,
                          nntc_sdk_path, module_version, nntc_sdk_path,
                          nntc_sdk_path, module_version)
        op_cmd(cmd2)

        # create soc sdk
        if is_create_soc_sdk:
            soc_sdk_path = 'soc-sdk'
            if os.path.exists(soc_sdk_path):
                shutil.rmtree(soc_sdk_path)
            os.mkdir(soc_sdk_path)
            module_path, module_version = module_path_soc(sdk_path, 'sophon-img')
            cmd = "sudo tar zxf {}/libsophon_soc_{}_aarch64.tar.gz -C {} && cp -fr {}/libsophon_soc_{}_aarch64/* {}/ && " \
                  "rm -fr {}/libsophon_soc_{}_aarch64"
            cmd2 = cmd.format(module_path, module_version, soc_sdk_path,
                              soc_sdk_path, module_version, soc_sdk_path,
                              soc_sdk_path, module_version)
            op_cmd(cmd2)
            cmd = "cd {}/opt/sophon/ && sudo ln -s libsophon-{} libsophon-current".format(soc_sdk_path, module_version)
            op_cmd(cmd)

            module_path, module_version = module_path_soc(sdk_path, 'sophon-mw')
            cmd = "sudo tar zxf {}/sophon-mw-soc_{}_aarch64.tar.gz -C {} && cp -fr {}/sophon-mw-soc_{}_aarch64/* {}/ && " \
                  "rm -fr {}/sophon-mw-soc_{}_aarch64"
            cmd2 = cmd.format(module_path, module_version, soc_sdk_path,
                              soc_sdk_path, module_version, soc_sdk_path,
                              soc_sdk_path, module_version)
            op_cmd(cmd2)
            cmd = "cd {}/opt/sophon/ && sudo ln -s sophon-ffmpeg_{} sophon-ffmpeg-current".format(soc_sdk_path,
                                                                                                  module_version)
            op_cmd(cmd)
            cmd = "cd {}/opt/sophon/ && sudo ln -s sophon-opencv_{} sophon-opencv-current".format(soc_sdk_path,
                                                                                                  module_version)
            op_cmd(cmd)
            cmd = "cd {}/opt/sophon/ && sudo ln -s sophon-sample_{} sophon-sample-current".format(soc_sdk_path,
                                                                                                  module_version)
            op_cmd(cmd)

    elif ostype == "soc":
        # libsophon
        module_path, module_version = module_path_soc(sdk_path, 'sophon-img')
        print("Detected libsophon version: {}".format(module_version))
        cmd = "cd {} && sudo dpkg -i bsp-debs/sophon-soc-libsophon_{}_arm64.deb"
        cmd2 = cmd.format(module_path, module_version)
        op_cmd(cmd2)

        cmd = "cd {} && sudo dpkg -i bsp-debs/sophon-soc-libsophon-dev_{}_arm64.deb"
        cmd2 = cmd.format(module_path, module_version)
        op_cmd(cmd2)

        # sophon-mw
        # ffmpeg
        module_path, module_version = module_path_soc(sdk_path, 'sophon-mw')
        print("Detected sophon-mw version: {}".format(module_version))
        cmd = "cd {} && sudo dpkg -i sophon-mw-soc-sophon-ffmpeg_{}_arm64.deb && sudo dpkg -i " \
              "sophon-mw-soc-sophon-ffmpeg-dev_{}_arm64.deb"
        cmd2 = cmd.format(module_path, module_version, module_version)
        op_cmd(cmd2)

        # opencv
        cmd = "cd {} && sudo dpkg -i sophon-mw-soc-sophon-opencv_{}_arm64.deb && sudo dpkg -i " \
              "sophon-mw-soc-sophon-opencv-dev_{}_arm64.deb"
        cmd2 = cmd.format(module_path, module_version, module_version)
        op_cmd(cmd2)
