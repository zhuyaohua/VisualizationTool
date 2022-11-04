"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     GHDH.py
@Author:   shenfan
@Time:     2022/10/17 11:22
"""
from Xboard.Delivery.file_type import unzip
import json
from jsonpath import jsonpath
import os


class GHDH:
    def __init__(self, filepath, filename):
        self.filepath = filepath
        self.filename = filename
        self.padpath = os.path.join(unzip(self.filepath, self.filename), "pda.json")

        if os.path.exists(self.padpath):
            with open(self.padpath, "r", encoding="utf-8") as stream:
                self.data = json.loads(stream.read())
        else:
            self.data = None
        self.landList = jsonpath(self.data, "$.landList.*")
        self.buildingList = jsonpath(self.data, "$.buildingList.*")

    def landlist(self):
        return self.landList

    def buildinglist(self):
        buildingList = []
        for buildingList_items in self.buildingList:
            temp = buildingList_items.pop("buildingHeadList", None)
            temps = buildingList_items
            if temp:
                for item in temp:
                    temps.update(item)
                    buildingList.append(temps.copy())
        return buildingList

    def ghdh_data(self):
        landList = self.landlist()
        buildingList = self.buildinglist()
        checkTables = {}

        for itemLand in landList:
            checkTableHeaders = {"GH-A-301 总用地面积": {"value": 0.0, "uids": []},
                                 "GH-A-308 总建筑面积": {"value": 0.0, "uids": []},
                                 "GH-A-87 地上计容面积": {"value": 0.0, "uids": []},
                                 "GH-A-88 地上不计容面积": {"value": 0.0, "uids": []},
                                 "GH-A-309 地下建筑总面积": {"value": 0.0, "uids": []},
                                 "GH-A-403 地块计容总建筑面积": {"value": 0.0, "uids": []},
                                 "GH-A-89 建筑基底总面积": {"value": 0.0, "uids": []},
                                 "GH-A-90 道路广场面积": {"value": 0.0, "uids": []},
                                 "GH-A-473 绿地面积": {"value": 0.0, "uids": []},
                                 "GH-A-312 容积率": {"value": 0.0, "uids": []},
                                 "GH-A-317 建筑密度": {"value": 0.0, "uids": []},
                                 "GH-A-313 绿地率": {"value": 0.0, "uids": []},
                                 "GH-A-182 建筑高度（m）": {"value": 0.0, "uids": []},
                                 "GH-A-29 地上机动车位数": {"value": 0.0, "uids": []},
                                 "GH-A-32 地下机动车位数": {"value": 0.0, "uids": []},
                                 "GH-A-143 机动车位数": {"value": 0.0, "uids": []},
                                 "GH-A-358 无障碍车位数": {"value": 0.0, "uids": []},
                                 "GH-A-368 充电桩车位数量": {"value": 0.0, "uids": []},
                                 "GH-A-91 地上非机动车位数": {"value": 0.0, "uids": []},
                                 "GH-A-92 地下非机动车位数": {"value": 0.0, "uids": []},
                                 "GH-A-367 非机动车位数": {"value": 0.0, "uids": []},
                                 "GH-A-101 控规地块编号": {"value": 0.0, "uids": []},
                                 "GH-A-84 装配率": {"value": 0.0, "uids": []},
                                 "GH-A-117 户数统计（户）": {"value": 0.0, "uids": []},
                                 "GH-A-425 居住总人数": {"value": 0.0, "uids": []},
                                 "GH-A-85 住宅平均层数": {"value": 0.0, "uids": []},
                                 "GH-A-82 可建设用地面积（定线作业表）": {"value": 0.0, "uids": []},
                                 "buildings": {},
                                 }
            checkTables["{0}-{1}".format(itemLand["landNumber"], itemLand["landName"])] = checkTableHeaders
            landName = itemLand["landName"]
            landCode = itemLand["landNumber"]
            landGH_A_82 = float(itemLand["properties"]["GH-A-82"]["Value"])
            checkTableHeaders["GH-A-82 可建设用地面积（定线作业表）"]["value"] = landGH_A_82
            # landComponentList
            landComponentLists = itemLand["landComponentList"]
            # landArea
            landAreaLists = jsonpath(itemLand, "$..landComponentList[?(@.properties)]")
            for itemLandArea in landAreaLists:
                if jsonpath(itemLandArea, "$..GH-A-41"):
                    if itemLandArea["properties"]["GH-A-41"]["Value"] == "建设项目规划总用地":
                        checkTableHeaders["GH-A-301 总用地面积"]["value"] += float(
                            itemLandArea["properties"]["GH-A-176"]["Value"])
                        checkTableHeaders["GH-A-301 总用地面积"]["value"] = round(
                            checkTableHeaders["GH-A-301 总用地面积"]["value"],
                            2)
                        checkTableHeaders["GH-A-301 总用地面积"]["uids"].extend(itemLandArea["uids"])
                    if itemLandArea["properties"]["GH-A-41"]["Value"] == "可建设用地面积（定线作业表）":
                        checkTableHeaders["GH-A-312 容积率"]["value"] += float(
                            itemLandArea["properties"]["GH-A-176"]["Value"])
                        checkTableHeaders["GH-A-312 容积率"]["value"] = round(checkTableHeaders["GH-A-312 容积率"]["value"],
                                                                           2)
                        checkTableHeaders["GH-A-312 容积率"]["uids"].extend(itemLandArea["uids"])
                if itemLandArea["name"] == "建筑地坪":
                    checkTableHeaders["GH-A-89 建筑基底总面积"]["value"] += float(
                        itemLandArea["properties"]["GH-A-176"]["Value"])
                    checkTableHeaders["GH-A-89 建筑基底总面积"]["value"] = round(checkTableHeaders["GH-A-89 建筑基底总面积"]["value"],
                                                                          2)
                    checkTableHeaders["GH-A-89 建筑基底总面积"]["uids"].extend(itemLandArea["uids"])
                if jsonpath(itemLandArea, "$..GH-A-108"):
                    if itemLandArea["properties"]["GH-A-108"]["Value"] == "基地道路":
                        checkTableHeaders["GH-A-90 道路广场面积"]["value"] += float(
                            itemLandArea["properties"]["GH-A-176"]["Value"])
                        checkTableHeaders["GH-A-90 道路广场面积"]["value"] = round(
                            checkTableHeaders["GH-A-90 道路广场面积"]["value"],
                            2)
                        checkTableHeaders["GH-A-90 道路广场面积"]["uids"].extend(itemLandArea["uids"])
                    if itemLandArea["properties"]["GH-A-108"]["Value"] == "绿地":
                        checkTableHeaders["GH-A-473 绿地面积"]["value"] += float(
                            itemLandArea["properties"]["GH-A-176"]["Value"]) * float(
                            itemLandArea["properties"]["GH-A-83"]["Value"])
                        checkTableHeaders["GH-A-473 绿地面积"]["uids"].extend(itemLandArea["uids"])
                    if itemLandArea["properties"]["GH-A-108"]["Value"] == "非机动车位":
                        checkTableHeaders["GH-A-91 地上非机动车位数"]["value"] += float(
                            itemLandArea["properties"]["GH-A-176"]["Value"])
                        checkTableHeaders["GH-A-91 地上非机动车位数"]["uids"].extend(itemLandArea["uids"])
                if jsonpath(itemLandArea, "$..GH-A-93"):
                    if itemLandArea["properties"]["GH-A-93"]["Value"] == "是":
                        checkTableHeaders["GH-A-473 绿地面积"]["value"] += float(
                            itemLandArea["properties"]["GH-A-176"]["Value"]) * float(
                            itemLandArea["properties"]["GH-A-83"]["Value"])
                        checkTableHeaders["GH-A-473 绿地面积"]["uids"].extend(itemLandArea["uids"])
            # buildingArea
            buildingAreaList = jsonpath(buildingList,
                                        "$.[?(@.landName=='{0}')].areaList[?(@.properties)]".format(landName))
            for itembuildingArea in buildingAreaList:
                checkTableHeaders["GH-A-308 总建筑面积"]["value"] += float(
                    itembuildingArea["properties"]["GH-A-176"]["Value"]) * float(
                    itembuildingArea["properties"]["GH-A-129"]["Value"]) * len(itembuildingArea["properties"]["GH-A-175"]["Value"].split(";"))
                checkTableHeaders["GH-A-308 总建筑面积"]["value"] = round(checkTableHeaders["GH-A-308 总建筑面积"]["value"], 2)
                checkTableHeaders["GH-A-308 总建筑面积"]["uids"].append(itembuildingArea["uid"])
                if jsonpath(itembuildingArea, "$..GH-A-24"):
                    if itembuildingArea["properties"]["GH-A-135"]["Value"].startswith("F"):
                        if itembuildingArea["properties"]["GH-A-24"]["Value"] == "是":
                            checkTableHeaders["GH-A-87 地上计容面积"]["value"] += len(
                                itembuildingArea["properties"]["GH-A-175"]["Value"].split(";")) * float(
                                itembuildingArea["properties"]["GH-A-176"]["Value"]) * float(
                                itembuildingArea["properties"]["GH-A-40"]["Value"])
                            checkTableHeaders["GH-A-87 地上计容面积"]["value"] = round(
                                checkTableHeaders["GH-A-87 地上计容面积"]["value"], 2)
                            checkTableHeaders["GH-A-87 地上计容面积"]["uids"].append(itembuildingArea["uid"])
                        if itembuildingArea["properties"]["GH-A-24"]["Value"] == "否":
                            checkTableHeaders["GH-A-88 地上不计容面积"]["value"] += len(
                                itembuildingArea["properties"]["GH-A-175"]["Value"].split(";")) * float(
                                itembuildingArea["properties"]["GH-A-176"]["Value"]) * float(
                                itembuildingArea["properties"]["GH-A-129"]["Value"])
                            checkTableHeaders["GH-A-88 地上不计容面积"]["value"] = round(
                                checkTableHeaders["GH-A-88 地上不计容面积"]["value"], 2)
                            checkTableHeaders["GH-A-88 地上不计容面积"]["uids"].append(itembuildingArea["uid"])
                    if itembuildingArea["properties"]["GH-A-24"]["Value"] == "是":
                        checkTableHeaders["GH-A-403 地块计容总建筑面积"]["value"] += len(
                            itembuildingArea["properties"]["GH-A-175"]["Value"].split(";")) * float(
                            itembuildingArea["properties"]["GH-A-176"]["Value"]) * float(
                            itembuildingArea["properties"]["GH-A-40"]["Value"])
                        checkTableHeaders["GH-A-403 地块计容总建筑面积"]["value"] = round(
                            checkTableHeaders["GH-A-403 地块计容总建筑面积"]["value"], 2)
                        checkTableHeaders["GH-A-403 地块计容总建筑面积"]["uids"].append(itembuildingArea["uid"])
                if jsonpath(itembuildingArea, "$..GH-A-183"):
                    if itembuildingArea["properties"]["GH-A-183"]["Value"] == "是":
                        checkTableHeaders["GH-A-473 绿地面积"]["value"] += float(
                            itembuildingArea["properties"]["GH-A-176"]["Value"]) * float(
                            itembuildingArea["properties"]["GH-A-83"]["Value"])*len(itembuildingArea["properties"]["GH-A-175"]["Value"].split(";"))
                        checkTableHeaders["GH-A-473 绿地面积"]["value"] = round(checkTableHeaders["GH-A-473 绿地面积"]["value"],
                                                                            2)
                        checkTableHeaders["GH-A-473 绿地面积"]["uids"].append(itembuildingArea["uid"])
                if itembuildingArea["properties"]["GH-A-135"]["Value"].startswith("B"):
                    checkTableHeaders["GH-A-309 地下建筑总面积"]["value"] += float(
                        itembuildingArea["properties"]["GH-A-176"]["Value"]) * float(
                        itembuildingArea["properties"]["GH-A-129"]["Value"])*len(itembuildingArea["properties"]["GH-A-175"]["Value"].split(";"))
                    checkTableHeaders["GH-A-309 地下建筑总面积"]["value"] = round(
                        checkTableHeaders["GH-A-309 地下建筑总面积"]["value"],
                        2)
                    checkTableHeaders["GH-A-309 地下建筑总面积"]["uids"].append(itembuildingArea["uid"])
                if jsonpath(itembuildingArea, "$..GH-A-159"):
                    if itembuildingArea["properties"]["GH-A-159"]["Value"] == "室内非机动车停车库":
                        if itembuildingArea["properties"]["GH-A-135"]["Value"].startswith("B"):
                            checkTableHeaders["GH-A-92 地下非机动车位数"]["value"] += float(
                                itembuildingArea["properties"]["GH-A-176"]["Value"])
                            checkTableHeaders["GH-A-92 地下非机动车位数"]["uids"].append(itembuildingArea["uid"])
                        if itembuildingArea["properties"]["GH-A-135"]["Value"].startswith("F"):
                            checkTableHeaders["GH-A-91 地上非机动车位数"]["value"] += float(
                                itembuildingArea["properties"]["GH-A-176"]["Value"])
                            checkTableHeaders["GH-A-91 地上非机动车位数"]["uids"].append(itembuildingArea["uid"])
                if jsonpath(itembuildingArea, "$..GH-A-177"):
                    if itembuildingArea["properties"]["GH-A-177"]["Value"] == "户型":
                        checkTableHeaders["GH-A-117 户数统计（户）"]["value"] += 1
                        checkTableHeaders["GH-A-117 户数统计（户）"]["uids"].append(itembuildingArea["uid"])

            # landParking
            landParkingLists = jsonpath(itemLand, "$..parkingList[?(@.properties)]")
            landParkingLists = landParkingLists if landParkingLists else []
            for itemlandParking in landParkingLists:
                if itemlandParking["properties"]["GH-A-138"]["Value"] in ["自走式停车位", "大巴车位", "出租车位", "无障碍车位"]:
                    checkTableHeaders["GH-A-29 地上机动车位数"]["value"] += 1
                    checkTableHeaders["GH-A-29 地上机动车位数"]["uids"].append(itemlandParking["uid"])
                if itemlandParking["properties"]["GH-A-138"]["Value"] in ["装卸车位", "机械式停车位"]:
                    checkTableHeaders["GH-A-29 地上机动车位数"]["value"] += 1 * (
                        lambda: 1 if itemlandParking["properties"]["GH-A-596"]["Value"] == "" else int(
                            itemlandParking["properties"]["GH-A-596"]["Value"]))()
                    checkTableHeaders["GH-A-29 地上机动车位数"]["uids"].append(itemlandParking["uid"])

            # buildParking
            buildParkingList = jsonpath(buildingList,
                                        "$.[?(@.landName=='{0}')].parkingList[?(@.properties)]".format(landName))
            buildParkingList = buildParkingList if buildParkingList else []
            for itembuildParking in buildParkingList:
                if itembuildParking["properties"]["GH-A-138"]["Value"] in ["自走式停车位", "大巴车位", "出租车位", "无障碍车位"]:
                    if itembuildParking["properties"]["GH-A-135"]["Value"].startswith("B"):
                        checkTableHeaders["GH-A-32 地下机动车位数"]["value"] += 1
                        checkTableHeaders["GH-A-32 地下机动车位数"]["uids"].append(itembuildParking["uid"])
                    if itembuildParking["properties"]["GH-A-135"]["Value"].startswith("F"):
                        checkTableHeaders["GH-A-29 地上机动车位数"]["value"] += 1
                        checkTableHeaders["GH-A-29 地上机动车位数"]["uids"].append(itembuildParking["uid"])
                if itembuildParking["properties"]["GH-A-138"]["Value"] in ["装卸车位", "机械式停车位"]:
                    if itembuildParking["properties"]["GH-A-135"]["Value"].startswith("B"):
                        checkTableHeaders["GH-A-32 地下机动车位数"]["value"] += 1 * (
                            lambda: 1 if itembuildParking["properties"]["GH-A-596"]["Value"] == "" else int(
                                itembuildParking["properties"]["GH-A-596"]["Value"]))()
                        checkTableHeaders["GH-A-32 地下机动车位数"]["uids"].append(itembuildParking["uid"])
                    if itembuildParking["properties"]["GH-A-135"]["Value"].startswith("F"):
                        checkTableHeaders["GH-A-29 地上机动车位数"]["value"] += 1 * (
                            lambda: 1 if itembuildParking["properties"]["GH-A-596"]["Value"] == "" else int(
                                itembuildParking["properties"]["GH-A-596"]["Value"]))()
                        checkTableHeaders["GH-A-29 地上机动车位数"]["uids"].append(itembuildParking["uid"])

            # building
            itemLandbuildings = jsonpath(buildingList, "$.[?(@.landName=='{0}')]".format(landName))

            for itembuilding in itemLandbuildings:
                buildingcheck = {
                                 "GH-A-101 控规地块编号": {"value": 0.0, "uids": []},
                                 "GH-A-110 建筑类型": {"value": 0.0, "uids": []},
                                 "GH-A-109 建筑编号": {"value": 0.0, "uids": []},
                                 "GH-A-181 配套设施用地规模": {"value": 0.0, "uids": []},
                                 "GH-A-311 配套设施建筑面积": {"value": 0.0, "uids": []}}
                checkTableHeaders["buildings"][itembuilding["buildingNo"]] = buildingcheck
                buildingcheck["GH-A-101 控规地块编号"]["value"] = landCode
                buildingcheck["GH-A-110 建筑类型"]["value"] = itembuilding["properties"]["GH-A-110"]["Value"]
                buildingcheck["GH-A-109 建筑编号"]["value"] = itembuilding["properties"]["GH-A-109"]["Value"]

                for itemlandComponent in landComponentLists:
                    if jsonpath(itemlandComponent, "$.properties.GH-A-109"):
                        if itemlandComponent["properties"]["GH-A-109"]["Value"] == itembuilding["buildingNo"]:
                            buildingcheck["GH-A-181 配套设施用地规模"]["value"] += float(itemlandComponent["properties"]["GH-A-176"]["Value"])
                for itembuildingarae in itembuilding["areaList"]:
                    buildingcheck["GH-A-311 配套设施建筑面积"]["value"] += float(itembuildingarae["properties"]["GH-A-176"]["Value"])*float(itembuildingarae["properties"]["GH-A-129"]["Value"])*len(itembuildingarae["properties"]["GH-A-175"]["Value"].split(";"))
                    buildingcheck["GH-A-311 配套设施建筑面积"]["value"] = round(buildingcheck["GH-A-311 配套设施建筑面积"]["value"], 2)
                    buildingcheck["GH-A-311 配套设施建筑面积"]["uids"].append(itembuildingarae["uid"])

                if itembuilding["properties"]["GH-A-110"]["Value"] == "住宅":
                    checkTableHeaders["GH-A-85 住宅平均层数"]["value"] += (
                                int(itembuilding["properties"]["GH-A-392"]["Value"]) + int(
                            itembuilding["properties"]["GH-A-112"]["Value"]))
            checkTableHeaders["GH-A-85 住宅平均层数"]["value"] = checkTableHeaders["GH-A-85 住宅平均层数"]["value"] / len(
                itemLandbuildings)

            landparks = jsonpath(itemLand, "$..parkingList..GH-A-138.Value")
            landparks = landparks if landparks else []
            buidingparks = jsonpath(buildingList,
                                    "$.[?(@.landName=='{0}')].parkingList..GH-A-138.Value".format(landName))
            buidingparks = buidingparks if buidingparks else []
            checkTableHeaders["GH-A-358 无障碍车位数"]["value"] = landparks.count("无障碍车位") + buidingparks.count("无障碍车位")

            landcharge = jsonpath(itemLand, "$..parkingList..GH-A-370.Value")
            landcharge = landcharge if landcharge else []
            buidingcharge = jsonpath(buildingList,
                                     "$.[?(@.landName=='{0}')].parkingList..GH-A-370.Value".format(landName))
            buidingcharge = buidingcharge if buidingcharge else []
            checkTableHeaders["GH-A-368 充电桩车位数量"]["value"] = landcharge.count("是") + buidingcharge.count("是")

            checkTableHeaders["GH-A-182 建筑高度（m）"]["value"] = float(
                max(jsonpath(buildingList, "$.[?(@.landName=='{0}')].properties.GH-A-182.Value".format(landName))))
            checkTableHeaders["GH-A-312 容积率"]["value"] = round(
                checkTableHeaders["GH-A-403 地块计容总建筑面积"]["value"] / checkTableHeaders["GH-A-312 容积率"]["value"], 2)
            checkTableHeaders["GH-A-312 容积率"]["uids"].extend(checkTableHeaders["GH-A-403 地块计容总建筑面积"]["uids"])
            checkTableHeaders["GH-A-317 建筑密度"]["value"] = round(
                checkTableHeaders["GH-A-89 建筑基底总面积"]["value"] / checkTableHeaders["GH-A-82 可建设用地面积（定线作业表）"]["value"], 2)
            checkTableHeaders["GH-A-317 建筑密度"]["uids"].extend(checkTableHeaders["GH-A-89 建筑基底总面积"]["uids"])
            checkTableHeaders["GH-A-317 建筑密度"]["uids"].extend(checkTableHeaders["GH-A-301 总用地面积"]["uids"])

            checkTableHeaders["GH-A-313 绿地率"]["value"] = round(
                checkTableHeaders["GH-A-473 绿地面积"]["value"] / landGH_A_82, 2)
            checkTableHeaders["GH-A-313 绿地率"]["uids"].extend(checkTableHeaders["GH-A-473 绿地面积"]["uids"])
            checkTableHeaders["GH-A-143 机动车位数"]["value"] = checkTableHeaders["GH-A-32 地下机动车位数"]["value"] + \
                                                           checkTableHeaders["GH-A-29 地上机动车位数"]["value"]
            checkTableHeaders["GH-A-143 机动车位数"]["uids"].extend(checkTableHeaders["GH-A-32 地下机动车位数"]["uids"])
            checkTableHeaders["GH-A-143 机动车位数"]["uids"].extend(checkTableHeaders["GH-A-29 地上机动车位数"]["uids"])

            checkTableHeaders["GH-A-91 地上非机动车位数"]["value"] = checkTableHeaders["GH-A-91 地上非机动车位数"]["value"] // 2
            checkTableHeaders["GH-A-92 地下非机动车位数"]["value"] = checkTableHeaders["GH-A-92 地下非机动车位数"]["value"] // 2
            checkTableHeaders["GH-A-367 非机动车位数"]["value"] = checkTableHeaders["GH-A-91 地上非机动车位数"]["value"] + \
                                                            checkTableHeaders["GH-A-92 地下非机动车位数"]["value"]
            checkTableHeaders["GH-A-367 非机动车位数"]["uids"].extend(checkTableHeaders["GH-A-91 地上非机动车位数"]["uids"])
            checkTableHeaders["GH-A-367 非机动车位数"]["uids"].extend(checkTableHeaders["GH-A-92 地下非机动车位数"]["uids"])
            checkTableHeaders["GH-A-84 装配率"]["value"] = float(itemLand["properties"]["GH-A-84"]["Value"])
            checkTableHeaders["GH-A-101 控规地块编号"]["value"] = itemLand["properties"]["GH-A-101"]["Value"]
            checkTableHeaders["GH-A-425 居住总人数"]["value"] = itemLand["properties"]["GH-A-425"]["Value"]

        modelDataPath = os.path.join(os.path.abspath("."), "unzipfiles", self.filename[:-4], "checkdata")
        if not os.path.exists(modelDataPath): os.mkdir(modelDataPath)
        with open(os.path.join(modelDataPath, "%s.json" % self.filename[:-4]), "w+", encoding="UTF-8") as stream:
            stream.write(json.dumps(checkTables, ensure_ascii=False))


if __name__ == "__main__":
    r = GHDH(r"C:\Users\SHENFAN\Desktop\中设数字\CBIM-中设数字-CIM包\CIM\海口项目", "万花项目0927.cim")
    r.ghdh_data()
    r2 = GHDH(r"C:\Users\SHENFAN\Desktop\中设数字\CBIM-中设数字-CIM包\CIM\海口项目", "万花项目0928.cim")
    r2.ghdh_data()
    # r.ghdh("GH-DH-5", "用地基本信息（海口）")
