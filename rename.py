import os
import argparse

def collect_files(folder, ext):
    fileNames = []
    for file in os.listdir(folder):
        allPath = os.path.join(folder, file)
        if os.path.isfile(allPath) and file.endswith(ext):
            # name = os.path.splitext(file)[0]
            fileNames.append(file)
    return sorted(fileNames)  


def rename_files(fileName, prefix, number, index):
    name, ext_part = os.path.splitext(fileName)
    prefix_part = prefix
    if (number): 
        prefix_part += f"_{index:03d}"
    return f"{prefix_part}{name}{ext_part}"

def main():
    parser = argparse.ArgumentParser(description="Rename files in a folder with a given prefix and optional numbering.")
    parser.add_argument("folder", help="要处理的目录")
    parser.add_argument("-p", "--prefix", default="", help="添加前缀")
    parser.add_argument("-n", "--number", action="store_true", help="添加序号")
    parser.add_argument("-e", "--ext", default="", help="只处理后缀，如 .jpg")
    parser.add_argument("--dry-run", action="store_true", help="只预览不修改")

    arg = parser.parse_args()
    folder = arg.folder
    prefix = arg.prefix
    number = arg.number
    ext = arg.ext

    if not os.path.exists(folder):
        print(f"目录 {folder} 不存在")
        return
    files_to_rename = collect_files(folder, ext)

    if not files_to_rename:
        print(f"目录 {folder} 中没有找到符合条件的文件")
        return
    if (len(files_to_rename) == 0):
        print(f"目录 {folder} 中没有找到符合条件的文件")
        return

    operationList = []
    index = 1
    for file in files_to_rename:
        renamed_file = rename_files(file, prefix, number, files_to_rename.index(file) + 1)
        if (renamed_file != file):
            print(f"{file} -> {renamed_file}")
            operationList.append((file, renamed_file))

        if number:
            index += 1

    if not operationList:
        print("没有需要重命名的文件")
        return

    print("即将执行以下预览")
    if arg.dry_run:
        print(f"预览模式，{len(operationList)} 个文件将被重命名")
        return

    aswer = input(f"是否确认重命名 {len(operationList)} 个文件？(y/n): ")
    if aswer.lower() == 'y':
        for old_name, new_name in operationList:
            old_path = os.path.join(folder, old_name)
            new_path = os.path.join(folder, new_name)
            os.rename(old_path, new_path)
        print("重命名完成")

if __name__ == "__main__":
    main()