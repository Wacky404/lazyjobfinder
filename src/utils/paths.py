import os.path as osp
import src

module: str = osp.dirname(osp.abspath(src.__file__))
dir_models: str = osp.join(module, "Models")
initialsql: str = osp.join(dir_models, "initial.sql")
