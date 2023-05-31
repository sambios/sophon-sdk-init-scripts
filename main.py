import ast
import shutil
import config
import os
import argparse


def op_cmd(cmd):
    print(cmd)
    os.system(cmd)

def op_rmtree(cmd):
    os.system('sudo rm -fr '+cmd)


def get_module_version(mod_path, mod_name):
    mod_version = 'unknown'
    d1_dirs = os.listdir(mod_path)
    for d1_dir in d1_dirs:
        if mod_name.startswith("tpu-nntc"):
          if d1_dir.startswith(mod_name+'_v'):
            if d1_dir.endswith('aarch64.tar.gz'):
                mod_version = d1_dir.replace('_aarch64.tar.gz', '').split('_')[-1]
                break
            elif d1_dir.endswith('x86_64.tar.gz'):
                mod_version = d1_dir.replace('_x86_64.tar.gz', '').split('_')[-1]
                break
            elif d1_dir.endswith('.tar.gz'):
                x=d1_dir.replace('.tar.gz', '')
                print(x)
                mod_version = x.split('_')[-1]
                break
        else:
          if d1_dir.startswith(mod_name):
            if d1_dir.endswith('aarch64.tar.gz'):
                mod_version = d1_dir.replace('_aarch64.tar.gz', '').split('_')[-1]
                break
            elif d1_dir.endswith('x86_64.tar.gz'):
                mod_version = d1_dir.replace('_x86_64.tar.gz', '').split('_')[-1]
                break
            elif d1_dir.endswith('.tar.gz'):
                mod_version = d1_dir.replace('.tar.gz', '').replace(mod_name + '_', '')
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

def get_extract_module_dir(module_path, module_name):
    dirs = os.listdir(module_path)
    for dir in dirs:
        if dir.startswith(module_name):
            return dir


def module_install_pcie(sdk_path, module_name, install_sdk_path):
    module_path, module_version = module_path_pcie(sdk_path, module_name)
    print("Detected {} version: {}".format(module_name, module_version))
    if not os.path.exists(install_sdk_path):
        os.mkdir(install_sdk_path)
    real_path = os.path.join(install_sdk_path, module_name)
    if os.path.exists(real_path):
        op_rmtree(real_path)
    os.mkdir(real_path)
    cmd_args = "sudo tar zxf {}/{}_{}.tar.gz -C {}"
    cmd = cmd_args.format(module_path, module_name, module_version, real_path)
    op_cmd(cmd)
    module_extract_dir = get_extract_module_dir(real_path, module_name)
    print("module_extract_dir=%s" % (module_extract_dir))
    cmd_args = "sudo cp -fr {}/{}/* {}/ && sudo rm -fr {}/{}"
    cmd = cmd_args.format(real_path, module_extract_dir, real_path,
                          real_path, module_extract_dir)
    op_cmd(cmd)
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='SophonSDK init tool')
    parser.add_argument('-o', '--ostype', default=config.ARCH_TYPE, help='target platform type:x86_64|soc')
    parser.add_argument('-p', '--path', default=config.RELEASE_ROOT, help='the path of SophonSDK')
    parser.add_argument('-m', '--install-mode', default='standard', help='install mode:standard, all')
    parser.add_argument('-i', '--install-path', default='sgnnsdk', help='the install path for sdk')
    parser.add_argument('-s', '--install-soc-sdk', action='store_true', help='install soc sdk')

    args = parser.parse_args()
    print(args)

    ostype = args.ostype
    sdk_path = args.path
    install_sdk_path = args.install_path
    install_mode = args.install_mode
    is_create_soc_sdk = args.install_soc_sdk

    if ostype == "x86_64":
        op_cmd("sudo apt install libncurses-dev")
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

        if install_mode == 'all':
            # tpu-nntc
            module_install_pcie(sdk_path, 'tpu-nntc', install_sdk_path)
            # sophon-demo
            module_install_pcie(sdk_path, 'sophon-demo', install_sdk_path)
            # sophon-pipeline
            module_install_pcie(sdk_path, 'sophon-pipeline', install_sdk_path)
            # sophon-sail
            module_install_pcie(sdk_path, 'sophon-sail', install_sdk_path)

        # create soc sdk
        if is_create_soc_sdk:
            soc_sdk_path = os.path.join(install_sdk_path, 'soc-sdk')
            if os.path.exists(soc_sdk_path):
                op_rmtree(soc_sdk_path)
            os.makedirs(soc_sdk_path)
            module_path, module_version = module_path_soc(sdk_path, 'sophon-img')
            cmd = "sudo tar zxf {}/libsophon_soc_{}_aarch64.tar.gz -C {} && cp -fr {}/libsophon_soc_{}_aarch64/* {}/ && " \
                  "sudo rm -fr {}/libsophon_soc_{}_aarch64"
            cmd2 = cmd.format(module_path, module_version, soc_sdk_path,
                              soc_sdk_path, module_version, soc_sdk_path,
                              soc_sdk_path, module_version)
            op_cmd(cmd2)
            cmd = "cd {}/opt/sophon/ && sudo ln -s libsophon-{} libsophon-current".format(soc_sdk_path, module_version)
            op_cmd(cmd)

            module_path, module_version = module_path_soc(sdk_path, 'sophon-mw')
            cmd = "sudo tar zxf {}/sophon-mw-soc_{}_aarch64.tar.gz -C {} && cp -fr {}/sophon-mw-soc_{}_aarch64/* {}/ && " \
                  "sudo rm -fr {}/sophon-mw-soc_{}_aarch64"
            cmd2 = cmd.format(module_path, module_version, soc_sdk_path,
                              soc_sdk_path, module_version, soc_sdk_path,
                              soc_sdk_path, module_version)
            op_cmd(cmd2)
            cmd = "cd {}/opt/sophon/ && sudo ln -s sophon-ffmpeg_{} sophon-ffmpeg-latest".format(soc_sdk_path,
                                                                                                 module_version)
            op_cmd(cmd)
            cmd = "cd {}/opt/sophon/ && sudo ln -s sophon-opencv_{} sophon-opencv-latest".format(soc_sdk_path,
                                                                                                 module_version)
            op_cmd(cmd)
            cmd = "cd {}/opt/sophon/ && sudo ln -s sophon-sample_{} sophon-sample-latest".format(soc_sdk_path,
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
