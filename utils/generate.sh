#!/bin/sh
USEPath='/Users/ksloan/Workbenches/OpenStudioWorkBench/utils'
#python3.11 '/Users/ksloan/Workbenches/OpenStudioWorkBench/utils/gen_Obj_Dialog.py' ./GBxml.xsd Complex
python3.11 $USEPath/save9.py $USEPath/GBxml.xsd Campus
python3.11 $USEPath/save9.py $USEPath/GBxml.xsd Building
python3.11 $USEPath/save9.py $USEPath/GBxml.xsd Space

