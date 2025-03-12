from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    Import: Any = None
    env: Any = {}

from os.path import join, isfile, exists, dirname, basename
from os import rename, remove, makedirs

import gzip
import glob

Import("env") # type: ignore

FRAMEWORK_DIR = env.PioPlatform().get_package_dir("framework-arduinoespressif32")
patchflag_path = join(FRAMEWORK_DIR, ".patched")
board_mcu = env.BoardConfig()
mcu = board_mcu.get("build.mcu", "")

# # patch file only if we didn't do it befored
# if not isfile(join(FRAMEWORK_DIR, ".patched")):
#     original_file = join(FRAMEWORK_DIR, "tools", "sdk", mcu, "lib", "libnet80211.a")
#     patched_file = join(FRAMEWORK_DIR, "tools", "sdk", mcu, "lib", "libnet80211.a.patched")
# 
#     env.Execute("pio pkg exec -p toolchain-xtensa-%s -- xtensa-%s-elf-objcopy  --weaken-symbol=s %s %s" % (mcu, mcu, original_file, patched_file))
#     if(isfile("%s.old"%(original_file))):
#         remove("%s.old"%(original_file))
#     rename(original_file,"%s.old"%(original_file))
#     env.Execute("pio pkg exec -p toolchain-xtensa-%s -- xtensa-%s-elf-objcopy  --weaken-symbol=ieee80211_raw_frame_sanity_check %s %s" % (mcu, mcu, patched_file, original_file))
#
#    def _touch(path):
#        with open(path, "w") as fp:
#            fp.write("")
#
#    env.Execute(lambda *args, **kwargs: _touch(patchflag_path))

# gzip web files
def prepare_www_files():
    HEADER_FILE = join(env.get('PROJECT_DIR'), 'include', 'webFiles.h')
    filetypes_to_gzip = ['html', 'css', 'js']
    data_src_dir = join(env.get('PROJECT_DIR'), 'embedded_resources/web_interface')

    if not exists(data_src_dir):
        print(f'Error: Source directory "{data_src_dir}" does not exist!')
        return

    files_to_gzip = []
    for extension in filetypes_to_gzip:
        files_to_gzip.extend(glob.glob(join(data_src_dir, '*.' + extension)))

    print(f'[GZIP & EMBED INTO HEADER] - Processing {len(files_to_gzip)} files.')

    makedirs(dirname(HEADER_FILE), exist_ok=True)

    with open(HEADER_FILE, 'w') as header:
        header.write('#ifndef WEB_FILES_H\n#define WEB_FILES_H\n\n#include <Arduino.h>\n\n')
        header.write('// THIS FILE IS AUTOGENERATED DO NOT MODIFY IT. MODIFY FILES IN /embedded_resources/web_interface\n\n')

        for file in files_to_gzip:
            gz_file = file + '.gz'
            with open(file, 'rb') as src, gzip.open(gz_file, 'wb') as dst:
                dst.writelines(src)

            with open(gz_file, 'rb') as gz:
                compressed_data = gz.read()
                var_name = basename(file).replace('.', '_')

                header.write(f'const char {var_name}[] PROGMEM = {{\n')

                # Write hex values, inserting a newline every 15 bytes
                for i in range(0, len(compressed_data), 15):
                    hex_chunk = ', '.join(f'0x{byte:02X}' for byte in compressed_data[i:i+15])
                    header.write(f'  {hex_chunk},\n')

                header.write('};\n\n')
                header.write(f'const uint32_t {var_name}_size = {len(compressed_data)};\n\n')

            remove(gz_file)  # Clean up temporary gzip file

        header.write('#endif // WEB_FILES_H\n')

    print(f'[DONE] Gzipped files embedded into {HEADER_FILE}')

prepare_www_files()