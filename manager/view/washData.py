#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
# from visitor.models import User,Province,City,Area
# from visitor import models
from django.http import JsonResponse, HttpResponse
import json
import string
from manager.mysqlNullWash import if_is_None, webType_to_strType
from django.views.decorators.csrf import csrf_exempt
from visitor.scripts.signin import *
from manager.scripts.sysscript import *
import pymysql  # 导入 pymysql
import re
import logging

logger = logging.getLogger('wash')


@csrf_exempt
def yuanshujubiao(request):
    wangzhan = request.POST
    # print("wangzhan",wangzhan)
    tablename = {}
    for i in wangzhan:
        # print(i)
        tablename = json.loads(i)
    dataList = []
    print("┗|｀O′|┛ 嗷~~")
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root",
                         password="461834084", db=tablename['sitename'], port=3306)
    # db = pymysql.connect(host="192.168.100.103", user="root",
    #                      password="root", db="linshitongji", port=3306)

    # 使用cursor()方法获取操作游标
    cur = db.cursor()

    # 1.查询操作
    # 编写sql 查询语句  user 对应我的表名
    # sql ="select TABLE_NAME,SCHEMA_NAME,WebSite,WebsiteType,NUM_ROWS from datatables,website_schema where SCHEMA_NAME=SchemaName"
    sql = "select * from " + tablename['tablename'] + " limit 50"
    sql2 = "SHOW COLUMNS FROM " + tablename['tablename']
    try:
        cur.execute(sql2)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        columns = []
        for row in results:
            columns.append(row[0])
        # print(columns)
        linshidiction = {}
        for row in columns:
            linshidiction[row] = row
        dataList.append(linshidiction)
        cur.execute(sql)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录

        for row in results:
            i = 0
            diction = {}
            for col in row:
                diction[columns[i]] = col
                i = i + 1
            # print(diction)
            dataList.append(diction)
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接
    data = {"data": dataList}
    # print(data)
    # print(type(HttpResponse(json.dumps(data))))
    #     # print(type(json.dumps(data)))
    #     # print(type(data))
    #     # print(len(data))
    return HttpResponse(json.dumps(data))


@csrf_exempt
def xuanzewangzhan(request):
    dataList = []
    wangzhan = request.POST
    val = ""
    for i in wangzhan:
        val = i
    tablenames = findtablenames(val)
    diction = {}
    for row in tablenames:
        # print(row[0])
        diction[row[0]] = row[0]
    dataList.append(diction)
    data = {"data": dataList}
    return HttpResponse(json.dumps(data))


def findtablenames(val):
    db = pymysql.connect(host="localhost", user="root",
                         password="461834084", db=val, port=3306)
    cur = db.cursor()
    sql = "show tables"
    try:
        cur.execute(sql)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        return results
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接


@csrf_exempt
def DIYfenye(request):
    dataList = []
    wangzhan = request.POST
    tablename = {}
    for i in wangzhan:
        tablename = json.loads(i)
    print(tablename)
    dataList = fenyedudb(tablename['sitename'], tablename['tablename'], tablename['page'], tablename['len'], )
    data = {"data": dataList}
    print(data)
    return HttpResponse(json.dumps(data))


@csrf_exempt
def tongji(request):
    dataList = []
    wangzhan = request.POST
    tablename = {}
    for i in wangzhan:
        print(i)
        tablename = json.loads(i)
    print(tablename)
    db = pymysql.connect(host="localhost", user="root",
                         password="461834084", db=tablename['sitename'], port=3306)
    cur = db.cursor()
    sql = "select " + tablename['columnname'] + ",count(*) as numnumnumnumnum from " + tablename[
        'tablename'] + " group by " + tablename['columnname'] + " ORDER BY numnumnumnumnum DESC LIMIT 10"
    try:

        cur.execute(sql)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        print(results)
        for row in results:
            i = 0
            diction = {}
            for col in row:
                if i == 0:
                    diction['name'] = col
                elif i == 1:
                    diction['value'] = col
                i = i + 1
            dataList.append(diction)
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接
    data = {"data": dataList}
    # print(data)
    return HttpResponse(json.dumps(data))


@csrf_exempt
def washaction(request):
    print(request.POST)
    dataList = []
    data = {}
    washform = request.POST
    # print(washform)
    actiontype = washform.get('formtype')
    columnname = washform.get('columnname')
    sitename = washform.get('sitename')
    tablename = washform.get('tablename')
    chehuiStack = washform.get('chehuiStack')
    adminname = washform.get('adminname')
    if actiontype == 'tihuan':
        tihuanbefore = washform.get('tihuanval1')
        tihuanafter = washform.get('tihuanval2')
        db = pymysql.connect(host="localhost", user="root",
                             password="461834084", db=sitename, port=3306)
        cur = db.cursor()
        sql = "DROP TABLE IF EXISTS " + "beifen_" + tablename + adminname + chehuiStack
        sql2 = "create table " + "beifen_" + tablename + adminname + chehuiStack + " like " + tablename
        sql3 = "insert into " + "beifen_" + tablename + adminname + chehuiStack + " select * from " + tablename
        sql4 = "UPDATE " + tablename + " SET " + columnname + "='" + tihuanafter + "' WHERE " + columnname + "='" + tihuanbefore + "'"
        # print(sql+";"+sql2+";"+sql3+";")
        # sql5 = sql+";"+sql2+";"+sql3+";"
        try:
            # print(sql4)
            cur.execute(sql)  #
            cur.execute(sql2)  #
            a = cur.execute(sql3)  #
            db.commit()
            a = cur.execute(sql4)
            db.commit()
            print(a)
            logdata = [sitename, tablename, request.session['user_name'], a, '替换', sql4]
            logger.debug(logdata)
            data = {"data": "success"}
        except Exception as e:
            # Rollback in case there is any error
            db.rollback()
            data = {"data": "error"}
            raise e
        finally:
            db.close()  # 关闭连接
    elif actiontype == 'queshizhi':
        tianzhongzhi = washform.get('tianzhongzhi')
        db = pymysql.connect(host="localhost", user="root",
                             password="461834084", db=sitename, port=3306)
        cur = db.cursor()
        sql = "DROP TABLE IF EXISTS " + "beifen_" + tablename + adminname + chehuiStack
        sql2 = "create table " + "beifen_" + tablename + adminname + chehuiStack + " like " + tablename
        sql3 = "insert into " + "beifen_" + tablename + adminname + chehuiStack + " select * from " + tablename
        if tianzhongzhi == 'null':
            sql4 = "UPDATE " + tablename + " SET " + columnname + "='" + "null" + "' WHERE " + columnname + "=''"
            db = pymysql.connect(host="localhost", user="root",
                                 password="461834084", db=sitename, port=3306)
            cur = db.cursor()
            try:
                cur.execute(sql)
                cur.execute(sql2)
                cur.execute(sql3)
                db.commit()
                a = cur.execute(sql4)  # 执行sql语句
                db.commit()
                logdata = [sitename, tablename, request.session['user_name'], a, '缺失值', sql4]
                logger.debug(logdata)
                data = {"data": "success"}
            except Exception as e:
                # Rollback in case there is any error
                db.rollback()
                data = {"data": "error"}
                raise e
            db.close()  # 关闭连接
        elif tianzhongzhi == 'avg':
            sql5 = "select avg(" + columnname + ") from " + tablename
            db = pymysql.connect(host="localhost", user="root",
                                 password="461834084", db=sitename, port=3306)
            cur = db.cursor()
            try:
                cur.execute(sql5)  # 执行sql语句
                results = cur.fetchall()  # 获取查询的所有记录
                average = ''
                for row in results:
                    print(row)
                    average = row[0]
                average = "%.0f" % average
                sql4 = "UPDATE " + tablename + " SET " + columnname + "='" + average + "' WHERE " + columnname + "=''"
                cur = db.cursor()
                cur.execute(sql)
                cur.execute(sql2)
                cur.execute(sql3)
                db.commit()
                numofchanges = cur.execute(sql4)  # 执行sql语句
                db.commit()
                logdata = [sitename, tablename, request.session['user_name'], numofchanges, '缺失值', sql4]
                logger.debug(logdata)
                data = {"data": "success"}
            except Exception as e:
                # Rollback in case there is any error
                db.rollback()
                data = {"data": "error"}
                raise e
            db.close()  # 关闭连接
        elif tianzhongzhi == 'max':
            sql5 = "select max(" + columnname + ") from " + tablename
            db = pymysql.connect(host="localhost", user="root",
                                 password="461834084", db=sitename, port=3306)
            cur = db.cursor()
            cur.execute(sql5)  # 执行sql语句
            results = cur.fetchall()  # 获取查询的所有记录
            max = ''
            for row in results:
                print(row)
                max = row[0]
            sql4 = "UPDATE " + tablename + " SET " + columnname + "='" + max + "' WHERE " + columnname + "=''"
            cur = db.cursor()
            try:
                cur.execute(sql)
                cur.execute(sql2)
                cur.execute(sql3)
                db.commit()
                a = cur.execute(sql4)  # 执行sql语句
                db.commit()
                logdata = [sitename, tablename, request.session['user_name'], a, '缺失值', sql4]
                logger.debug(logdata)
                data = {"data": "success"}
            except Exception as e:
                # Rollback in case there is any error
                db.rollback()
                data = {"data": "error"}
                raise e
            db.close()  # 关闭连接
        elif tianzhongzhi == 'min':
            sql5 = "select min(" + columnname + ") from " + tablename + " where " + columnname + "<>''"
            # print(sql5)
            db = pymysql.connect(host="localhost", user="root",
                                 password="461834084", db=sitename, port=3306)
            cur = db.cursor()
            cur.execute(sql5)  # 执行sql语句
            results = cur.fetchall()  # 获取查询的所有记录
            min = ''
            for row in results:
                print(row)
                min = row[0]
            sql4 = "UPDATE " + tablename + " SET " + columnname + "='" + min + "' WHERE " + columnname + "=''"
            cur = db.cursor()
            try:
                cur.execute(sql)
                cur.execute(sql2)
                cur.execute(sql3)
                db.commit()
                a = cur.execute(sql4)  # 执行sql语句
                db.commit()
                logdata = [sitename, tablename, request.session['user_name'], a, '缺失值', sql4]
                logger.debug(logdata)
                data = {"data": "success"}
            except Exception as e:
                # Rollback in case there is any error
                db.rollback()
                data = {"data": "error"}
                raise e
            db.close()  # 关闭连接
        elif tianzhongzhi == 'mid':
            sql7 = "DROP TABLE IF EXISTS " + "beifen_linshi_" + tablename + adminname + chehuiStack
            sql6 = "create table " + "beifen_linshi_" + tablename + adminname + chehuiStack + " as SELECT (@i:=@i+1) AS i," + columnname + " AS data FROM " + tablename + ",(select   @i:=0) as it ORDER BY " + columnname
            db = pymysql.connect(host="localhost", user="root",
                                 password="461834084", db=sitename, port=3306)
            cur = db.cursor()
            print(sql6)
            try:
                cur.execute(sql7)
                cur.execute(sql6)
                # except:
                #     # Rollback in case there is any error
                #     db.rollback()
                #     data = {"data": "error"}
                cur.execute("select count(*) from " + "beifen_linshi_" + tablename + adminname + chehuiStack)
                results = cur.fetchall()  # 获取查询的所有记录
                midid = 0
                print(results[0][0])
                total = int(results[0][0])
                if total % 2 == 1:
                    total = total + 1
                    midid = total / 2
                elif total % 2 == 0:
                    midid = total / 2
                cur.execute(
                    "select data from " + "beifen_linshi_" + tablename + adminname + chehuiStack + " where i=" + "%.0f" % midid)
                # print("select data from "+"beifen_linshi_" + tablename + adminname + chehuiStack+" where i="+"%.0f"%midid)
                results = cur.fetchall()  # 获取查询的所有记录
                for row in results:
                    print(row)
                    mid = row[0]
                cur.execute(sql7)
                sql4 = "UPDATE " + tablename + " SET " + columnname + "='" + mid + "' WHERE " + columnname + "=''"
                cur = db.cursor()
                cur.execute(sql)
                cur.execute(sql2)
                cur.execute(sql3)
                db.commit()
                a = cur.execute(sql4)  # 执行sql语句
                db.commit()
                logdata = [sitename, tablename, request.session['user_name'], a, '缺失值', sql4]
                logger.debug(logdata)
                data = {"data": "success"}
            except Exception as e:
                # Rollback in case there is any error
                db.rollback()
                data = {"data": "error"}
                raise e
            db.close()  # 关闭连接
        elif tianzhongzhi == 'frequent':
            sql5 = "select " + columnname + ",count(*) as numnumnumnumnum from " + tablename + " where " + columnname + "<>'' group by " + columnname + " ORDER BY numnumnumnumnum DESC LIMIT 1"
            db = pymysql.connect(host="localhost", user="root",
                                 password="461834084", db=sitename, port=3306)
            cur = db.cursor()
            cur.execute(sql5)  # 执行sql语句
            results = cur.fetchall()  # 获取查询的所有记录
            print(sql5)
            for row in results:
                # print(row)
                zuipinfanzhi = row[0]
            sql4 = "UPDATE " + tablename + " SET " + columnname + "='" + zuipinfanzhi + "' WHERE " + columnname + "=''"
            cur = db.cursor()
            try:
                cur.execute(sql)
                cur.execute(sql2)
                cur.execute(sql3)
                db.commit()
                a = cur.execute(sql4)  # 执行sql语句
                db.commit()
                logdata = [sitename, tablename, request.session['user_name'], a, '缺失值', sql4]
                logger.debug(logdata)
                data = {"data": "success"}
            except Exception as e:
                # Rollback in case there is any error
                db.rollback()
                data = {"data": "error"}
                raise e
            db.close()  # 关闭连接
        elif tianzhongzhi == 'inputval':
            inputval = washform.get('inputval')
            sql4 = "UPDATE " + tablename + " SET " + columnname + "='" + inputval + "' WHERE " + columnname + "=''"
            db = pymysql.connect(host="localhost", user="root",
                                 password="461834084", db=sitename, port=3306)
            cur = db.cursor()
            try:
                cur.execute(sql)
                cur.execute(sql2)
                cur.execute(sql3)
                db.commit()
                a = cur.execute(sql4)  # 执行sql语句
                db.commit()
                logdata = [sitename, tablename, request.session['user_name'], a, '缺失值', sql4]
                logger.debug(logdata)
                data = {"data": "success"}
            except Exception as e:
                # Rollback in case there is any error
                db.rollback()
                data = {"data": "error"}
                raise e
            db.close()  # 关闭连接
        elif tianzhongzhi == 'delthiscol':
            sql4 = "alter table " + tablename + " drop column " + columnname
            db = pymysql.connect(host="localhost", user="root",
                                 password="461834084", db=sitename, port=3306)
            cur = db.cursor()
            try:
                cur.execute(sql)
                cur.execute(sql2)
                cur.execute(sql3)
                db.commit()
                a = cur.execute(sql4)  # 执行sql语句
                db.commit()
                logdata = [sitename, tablename, request.session['user_name'], a, '缺失值', sql4]
                logger.debug(logdata)
                data = {"data": "success"}
            except Exception as e:
                # Rollback in case there is any error
                db.rollback()
                data = {"data": "error"}
                raise e
            db.close()  # 关闭连接
    if actiontype == 'shijiangeshi':
        shijiangeshi = washform.get('shijiangeshisel')
        sql = "DROP TABLE IF EXISTS " + "beifen_" + tablename + adminname + chehuiStack
        sql2 = "create table " + "beifen_" + tablename + adminname + chehuiStack + " like " + tablename
        sql3 = "insert into " + "beifen_" + tablename + adminname + chehuiStack + " select * from " + tablename
        db = pymysql.connect(host="localhost", user="root",
                             password="461834084", db=sitename, port=3306)
        cur = db.cursor()
        try:
            # print(sql4)
            cur.execute(sql)  #
            cur.execute(sql2)  #
            cur.execute(sql3)  #
            db.commit()
            cur.execute('desc ' + tablename)
            results = cur.fetchall()  # 获取查询的所有记录
            primarykey = []
            primarykeybit = []
            t = 0
            for i in results:
                if i[3] == 'PRI':
                    primarykey.append(i[0])
                    primarykeybit.append(t)
                t = t + 1
            sql4 = "select " + columnname
            for i in primarykey:
                sql4 = sql4 + "," + i
                print(i)
            sql4 = sql4 + " from " + tablename + " where " + columnname + "<> ''"
            print(sql4)
            cur.execute(sql4)
            results = cur.fetchall()  # 获取查询的所有记录
            for row in results:
                newrow = ''
                if ((shijiangeshi == '/') or (shijiangeshi == '-') or (shijiangeshi == '.')):
                    dateinrow = re.finditer(r'[1-9][0-9]*[\D][0-9]{1,2}[\D][0-9]{1,2}', row[0])
                    linshirow = row[0]
                    for i in dateinrow:
                        str = re.sub(r'[\D]', shijiangeshi, i.group())
                        newrow = re.sub(i.group(), str, linshirow)
                        linshirow = newrow
                    print(newrow)
                elif shijiangeshi == '1:':
                    timeinrow = re.finditer(r'[012][0-9][\D][0-6][0-9]', row[0])
                    linshirow = row[0]
                    for i in timeinrow:
                        str = re.sub(r'[\D]', ":", i.group())
                        newrow = re.sub(i.group(), str, linshirow)
                        linshirow = newrow
                    print(newrow)
                elif shijiangeshi == '2:':
                    longtimeinrow = re.finditer(r'[012][0-9][\D][0-6][0-9][\D][0-6][0-9]', row[0])
                    linshirow = row[0]
                    for i in longtimeinrow:
                        str = re.sub(r'[\D]', ":", i.group())
                        newrow = re.sub(i.group(), str, linshirow)
                        linshirow = newrow
                    print(newrow)
                elif shijiangeshi == '/2:':
                    newrow = rediyfun('/', 2, row[0])
                elif shijiangeshi == '-2:':
                    newrow = rediyfun('-', 2, row[0])
                elif shijiangeshi == '.2:':
                    newrow = rediyfun('.', 2, row[0])
                elif shijiangeshi == '/1:':
                    newrow = rediyfun('/', 1, row[0])
                elif shijiangeshi == '-1:':
                    newrow = rediyfun('-', 1, row[0])
                elif shijiangeshi == '.1:':
                    newrow = rediyfun('.', 1, row[0])
                sql5 = "update " + tablename + " set " + columnname + "='" + newrow + "' where " + primarykey[0] + "=" + \
                       row[primarykeybit[0]] + ""
                t = 0
                for i in primarykey:
                    if t > 0:
                        sql5 = sql5 + " and " + i + "=" + row[primarykeybit[t]]
                    t = t + 1
                print(sql5)
                if newrow != '':
                    a = cur.execute(sql5)  #
                    logdata = [sitename, tablename, request.session['user_name'], a, '统一时间格式', sql5]
                    logger.debug(logdata)
            db.commit()
            data = {"data": "success"}
        except Exception as e:
            # Rollback in case there is any error
            db.rollback()
            data = {"data": "error"}
            raise e
        finally:
            db.close()  # 关闭连接
    elif actiontype == 'updatearow':
        # tianzhongzhi = washform.get('tianzhongzhi')
        db = pymysql.connect(host="localhost", user="root",
                             password="461834084", db=sitename, port=3306)
        cur = db.cursor()
        sql = "DROP TABLE IF EXISTS " + "beifen_" + tablename + adminname + chehuiStack
        sql2 = "create table " + "beifen_" + tablename + adminname + chehuiStack + " like " + tablename
        sql3 = "insert into " + "beifen_" + tablename + adminname + chehuiStack + " select * from " + tablename
        cur.execute('desc ' + tablename)
        results = cur.fetchall()  # 获取查询的所有记录
        primarykey = []
        primarykeybit = []
        t = 0
        flgzhixing = 1
        for i in results:
            if i[3] == 'PRI':
                primarykey.append(i[0])
                primarykeybit.append(t)
            t = t + 1
        formlist = []
        formstructurelist = []
        for i in washform:
            # 如果i为未修改字段
            # if re.match('_LRXLRXLRXLRXLRXLRX', i) == None:
            # if (i != 'formtype') and (i != 'columnname') and (i != 'sitename') and (i != 'tablename') and (
            #         i != 'chehuiStack') and (i != 'adminname'):
            #     flg1 = 0
            #     for j in primarykey:
            #         if i == j:
            #             flg1 = 1
            #             break
            #     if flg1 == 0:
            #         formstructurelist.append(i)
            #         formlist.append(washform.get(i))
            # print(i+"+"+washform.get(i))
            if re.match('_LRXLRXLRXLRXLRXLRX', i) != None:
                washformgetxiugai = re.sub(r'_LRXLRXLRXLRXLRXLRX', "", i)
                for z in primarykey:
                    if washformgetxiugai == z:
                        print("不能修改主码")
                        flgzhixing = 0
                        break
                formstructurelist.append(washformgetxiugai)
                formlist.append(washform.get(washformgetxiugai))
        if flgzhixing == 1:
            sql4 = "UPDATE " + tablename + " SET " + formstructurelist[0] + "='" + formlist[0] + "'"
            t = 0
            for i in formstructurelist:
                if i != formstructurelist[0]:
                    sql4 = sql4 + "," + i + "='" + formlist[t] + "'"
                t = t + 1
            sql4 = sql4 + " where " + primarykey[0] + "=" + washform.get(primarykey[0])
            for i in primarykey:
                if i != primarykey[0]:
                    sql4 = sql4 + " and " + i + "=" + washform.get(i)
            print(sql4)
            try:
                cur.execute(sql)
                cur.execute(sql2)
                cur.execute(sql3)
                db.commit()
                a = cur.execute(sql4)  # 执行sql语句
                db.commit()
                logdata = [sitename, tablename, request.session['user_name'], a, '逐条修改', sql4]
                logger.debug(logdata)
                data = {"data": "success"}
            except:
                # Rollback in case there is any error
                db.rollback()
                data = {"data": "error"}
            db.close()  # 关闭连接
        else:
            data = {"data": "nopk"}
    elif actiontype == 'zifuchuangeshi':
        selectvalue = washform.get('zifuchuansel')
        sql = "DROP TABLE IF EXISTS " + "beifen_" + tablename + adminname + chehuiStack
        sql2 = "create table " + "beifen_" + tablename + adminname + chehuiStack + " like " + tablename
        sql3 = "insert into " + "beifen_" + tablename + adminname + chehuiStack + " select * from " + tablename
        db = pymysql.connect(host="localhost", user="root",
                             password="461834084", db=sitename, port=3306)
        cur = db.cursor()
        try:
            cur.execute(sql)  #
            cur.execute(sql2)  #
            cur.execute(sql3)  #
            db.commit()
            cur.execute('desc ' + tablename)
            results = cur.fetchall()  # 获取查询的所有记录
            primarykey = []
            primarykeybit = []
            t = 0
            for i in results:
                if i[3] == 'PRI':
                    primarykey.append(i[0])
                    primarykeybit.append(t)
                t = t + 1
            sql4 = "select " + columnname
            for i in primarykey:
                sql4 = sql4 + "," + i
                print(i)
            sql4 = sql4 + " from " + tablename + " where " + columnname + "<> ''"
            print(sql4)
            cur.execute(sql4)
            results = cur.fetchall()  # 获取查询的所有记录
            for row in results:
                newrow = ''
                if selectvalue == 'delkongge':
                    strinrow = re.finditer(r'[ ][^ ]+[ ]', row[0])
                    linshirow = row[0]
                    for i in strinrow:
                        str = re.sub(r'[ ]', '', i.group())
                        newrow = re.sub(i.group(), str, linshirow)
                        linshirow = newrow
                elif selectvalue == 'exchangekongge':
                    newrow = re.sub(r'[ ]', '&nbsp', row[0])
                if newrow != '':
                    newrow = re.sub(r"[']", '"', newrow)
                    # print(newrow)
                    sql5 = "update " + tablename + " set " + columnname + "='" + newrow + "' where " + primarykey[
                        0] + "=" + row[primarykeybit[0]] + ""
                    t = 0
                    for i in primarykey:
                        if t > 0:
                            sql5 = sql5 + " and " + i + "=" + row[primarykeybit[t]]
                        t = t + 1
                    # print(sql5)
                    a = cur.execute(sql5)  #
                    logdata = [sitename, tablename, request.session['user_name'], a, '统一字符串格式', sql5]
                    logger.debug(logdata)
            db.commit()
            data = {"data": "success"}
        except Exception as e:
            data = {"data": "error"}
            db.rollback()
            raise e
        finally:
            db.close()  # 关闭连接
    # print(data)
    return HttpResponse(json.dumps(data))


def rediyfun(fuhao, num, row):
    newrow = ''
    str = ''
    if num == 2:
        datetimeinrow = re.finditer(
            r'[1-9][0-9]*[\D][0-9]{1,2}[\D][0-9]{1,2}[\D][012][0-9][\D][0-6][0-9][\D][0-6][0-9]',
            row)
        for i in datetimeinrow:
            # print("kasihi "+i.group())
            str = re.sub(r'[\D]', ":", i.group())
            str = re.sub(r'[\D]', " ", str, 3)
            str = re.sub(r'[\D]', fuhao, str, 2)
            newrow = re.sub(i.group(), str, row)
            row = newrow
        print(newrow)
    elif num == 1:
        datetimeinrow = re.finditer(
            r'[1-9][0-9]*[\D][0-9]{1,2}[\D][0-9]{1,2}[\D][012][0-9][\D][0-6][0-9]',
            row)
        for i in datetimeinrow:
            str = re.sub(r'[\D]', ":", i.group())
            str = re.sub(r'[\D]', " ", str, 3)
            str = re.sub(r'[\D]', fuhao, str, 2)
            newrow = re.sub(i.group(), str, row)
            row = newrow
        print(newrow)
    return newrow


@csrf_exempt
def rollback(request):
    print(request.POST)
    dataList = []
    wangzhan = request.POST

    linshi = {}
    for i in wangzhan:
        linshi = json.loads(i)
    sitename = linshi['sitename']
    tablename = linshi['tablename']
    chehuiStack = linshi['chehuiStack']
    # columnname = linshi['columnname']
    adminname = linshi['adminname']
    db = pymysql.connect(host="localhost", user="root",
                         password="461834084", db=sitename, port=3306)
    cur = db.cursor()
    sql = "DROP TABLE IF EXISTS " + tablename
    sql2 = "create table " + tablename + " like " + "beifen_" + tablename + adminname + chehuiStack
    sql3 = "insert into " + tablename + " select * from " + "beifen_" + tablename + adminname + chehuiStack
    sql4 = "drop table " + "beifen_" + tablename + adminname + chehuiStack
    try:
        # print(sql4)
        cur.execute(sql)  #
        cur.execute(sql2)  #
        a = cur.execute(sql3)  #
        db.commit()
        if a == 1:
            print("yes" + str(a))
        else:
            print("no " + str(a))
        cur.execute(sql4)
        logdata = [sitename, tablename, request.session['user_name'], a, '撤回', sql3]
        logger.debug(logdata)
    except Exception as e:
        # Rollback in case there is any error
        db.rollback()
        raise e
    finally:
        db.close()  # 关闭连接
    data = {"data": dataList}
    print(data)
    return HttpResponse(json.dumps(data))


def fenyedudb(sitename, tablename, page, len):
    db = pymysql.connect(host="localhost", user="root",
                         password="461834084", db=sitename, port=3306)
    cur = db.cursor()
    sql = "select * from " + tablename + " limit " + str(int(page) * int(len)) + "," + str(int(len) * 5)
    sql2 = "SHOW COLUMNS FROM " + tablename
    # print(sql)
    try:
        dataList = []
        cur.execute(sql2)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        columns = []
        for row in results:
            columns.append(row[0])
        # print(columns)
        linshidiction = {}
        for row in columns:
            linshidiction[row] = row
        dataList.append(linshidiction)
        cur.execute(sql)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        for row in results:
            i = 0
            diction = {}
            for col in row:
                diction[columns[i]] = col
                i = i + 1
            dataList.append(diction)
        return dataList
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接
