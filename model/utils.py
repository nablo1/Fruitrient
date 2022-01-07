import os
import shutil

def split_images(input, output, debug = False):
    ret_train = [] # 70%
    ret_validation = [] # 20%
    ret_test = [] # 10%
    for root, _, files in os.walk(input, topdown=False):
        this = []
        for name in files:
            if name.endswith(".jpg") or name.endswith(".png"):
                this.append((os.path.join(root, name), os.path.basename(root), name))
                
        if len(this) == 0:
            continue

        tr = int(len(this) * 0.7)
        tec = int(len(this) * 0.2)
        tv = len(this) - (tr + tec) # rest

        train = this[:tr]
        validation = this[tr:tr+tec]
        test = this[tr+tec:]

        # sanity check
        real = (len(train) + len(validation) + len(test))
        exp = (tr + tec + tv)
        assert exp == real

        ret_train.extend(train)
        ret_validation.extend(validation)
        ret_test.extend(test)

    
    if not os.path.exists(output):
        os.mkdir(output)

    def copyout(subdir, arr):
        if os.path.exists(subdir):
            os.rmdir(subdir)

        trainpath = os.path.join(output, subdir)
        if not os.path.exists(trainpath):
            os.mkdir(trainpath)

        for path, base, name in arr:
            out = os.path.join(output, subdir, base)

            if not os.path.exists(out):
                os.mkdir(out)

            if debug:
                print(path, " -> ", out)
            shutil.copyfile(path, os.path.join(out, name))    

    copyout("validation", ret_validation)
    copyout("test", ret_test)
    copyout("train", ret_train)

    print(len(ret_train), len(ret_validation), len(ret_test))