#!/bin/sh
USEPath='/Users/ksloan/Workbenches/OpenStudioWorkBench/utils'
#python3.11 '/Users/ksloan/Workbenches/OpenStudioWorkBench/utils/gen_Obj_Dialog.py' ./GBxml.xsd Complex
echo 'test'
python3.11 $USEPath/elements2Class.py $USEPath/GBxml.xsd $USEPath/classDefs.py

