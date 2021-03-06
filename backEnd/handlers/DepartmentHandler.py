# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Copyright 2018 ZhangT. All Rights Reserved.
# Author: ZhangT
# Author-Github: github.com/zhangt2333
# DepartmentHandler.py 2018/12/3 21:19
import logging

from utils import DAO
from utils.commons import required_login, required_admin
from utils.response_code import RET
from .BaseHandler import BaseHandler

class QueryHandler(BaseHandler):
    @required_login
    def post(self):
        sql = """
        SELECT di_id, di_name, di_dean, di_address
        FROM ms_department_info
        WHERE CONCAT(di_id, '') like %(id)s AND
              di_name like %(name)s;
        """.strip()
        retKeys = ['id', 'name', 'dean', 'address']
        self.json_args['id'] = '%{}%'.format(self.json_args['id'])
        self.json_args['name'] = '%{}%'.format(self.json_args['name'])
        try:
            res = DAO.db_query(self, sql, self.json_args, retKeys)
            return self.write(dict(errcode=RET.OK, errmsg="OK", data=res))
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.PARAMERR, errmsg="出错"))

class EditHandler(BaseHandler):
    @required_login
    @required_admin
    def post(self):
        sql = """
        UPDATE ms_department_info
        SET di_name=%(name)s, di_dean=%(dean)s, di_address=%(address)s
        WHERE di_id=%(id)s;
        """.strip()
        try:
            DAO.db_execute(self, sql, self.json_args)
            return self.write(dict(errcode=RET.OK, errmsg="修改成功"))
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.PARAMERR, errmsg="出错"))


class AddHandler(BaseHandler):
    @required_login
    @required_admin
    def post(self):
        sql = """
        INSERT INTO ms_department_info
        (di_name, di_dean, di_address) VALUES
        (%(name)s, %(dean)s, %(address)s);
        """.strip()
        try:
            DAO.db_execute(self, sql, self.json_args)
            return self.write(dict(errcode=RET.OK, errmsg="添加成功"))
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.PARAMERR, errmsg="出错"))


class DeleteHandler(BaseHandler):
    @required_login
    @required_admin
    def post(self):
        sql = """
        DELETE FROM ms_department_info
        WHERE di_id=%(id)s;
        """.strip()
        try:
            DAO.db_execute(self, sql, self.json_args)
            return self.write(dict(errcode=RET.OK, errmsg="删除成功"))
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.PARAMERR, errmsg="出错"))
