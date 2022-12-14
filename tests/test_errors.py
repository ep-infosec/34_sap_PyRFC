#!/usr/bin/env python

# SPDX-FileCopyrightText: 2013 SAP SE Srdjan Boskovic <srdjan.boskovic@sap.com>
#
# SPDX-License-Identifier: Apache-2.0

# -*- coding: utf-8 -*-

import datetime
import socket
import unittest
from pyrfc import (
    Connection,
    RFCError,
    LogonError,
    ABAPApplicationError,
    ExternalRuntimeError,
)

from decimal import Decimal
from tests.config import PARAMS as params, CONFIG_SECTIONS as config_sections, get_error


class TestErrors:
    def setup_method(self, test_method):
        self.conn = Connection(**params)
        assert self.conn.alive

    def teardown_method(self, test_method):
        self.conn.close()
        assert not self.conn.alive

    def test_no_connection_params(self):
        try:
            Connection()
        except RFCError as ex:
            assert ex.args[0] == "Connection parameters missing"

    # todo: test correct status after error -> or to the error tests?
    def test_incomplete_params(self):
        incomplete_params = params.copy()
        for p in ["ashost", "gwhost", "mshost"]:
            if p in incomplete_params:
                del incomplete_params[p]
        try:
            Connection(**incomplete_params)
        except RFCError as ex:
            error = get_error(ex)
        assert error["code"] == 20
        assert error["key"] == "RFC_INVALID_PARAMETER"
        assert error["message"][0] in [
            "Parameter ASHOST, GWHOST, MSHOST or SERVER_PORT is missing.",
            "Parameter ASHOST, GWHOST, MSHOST or PORT is missing.",
            "Parameter ASHOST, GWHOST or MSHOST is missing.",
        ]

    def test_denied_users(self):
        denied_params = params.copy()
        denied_params["user"] = "BLAFASEL"
        try:
            Connection(**denied_params)
        except LogonError as ex:
            error = get_error(ex)

        assert error["code"] == 2
        assert error["key"] == "RFC_LOGON_FAILURE"
        assert error["message"][0] == "Name or password is incorrect (repeat logon)"

    def test_call_without_RFM_name(self):
        try:
            self.conn.call()
        except Exception as ex:
            assert isinstance(ex, TypeError) is True
            assert ex.args[0] == "call() takes at least 1 positional argument (0 given)"

    def test_call_non_existing_RFM(self):
        try:
            self.conn.call("undefined")
        except ABAPApplicationError as ex:
            error = get_error(ex)
        assert error["code"] == 5
        assert error["key"] == "FU_NOT_FOUND"
        assert error["message"][0] == "ID:FL Type:E Number:046 undefined"

    def test_call_non_string_RFM_name(self):
        try:
            self.conn.call(1)
        except RFCError as ex:
            assert ex.args == (
                "Remote function module name must be unicode string, received:",
                1,
                int,
            )

    def test_call_non_existing_RFM_parameter(self):
        try:
            self.conn.call("STFC_CONNECTION", undefined=0)
        except ExternalRuntimeError as ex:
            error = get_error(ex)
        assert error["code"] == 20
        assert error["key"] == "RFC_INVALID_PARAMETER"
        assert error["message"][0] == "field 'undefined' not found"

    def test_non_existing_field_structure(self):
        IMPORTSTRUCT = {"XRFCCHAR1": "A", "RFCCHAR2": "BC", "RFCCHAR4": "DEFG"}
        try:
            result = self.conn.call("STFC_STRUCTURE", IMPORTSTRUCT=IMPORTSTRUCT)
        except ExternalRuntimeError as ex:
            assert ex.code == 20
            assert ex.key == "RFC_INVALID_PARAMETER"
            assert ex.message == "field 'XRFCCHAR1' not found"

    def test_non_existing_field_table(self):
        IMPORTSTRUCT = {"XRFCCHAR1": "A", "RFCCHAR2": "BC", "RFCCHAR4": "DEFG"}
        try:
            result = self.conn.call("STFC_STRUCTURE", RFCTABLE=[IMPORTSTRUCT])
        except ExternalRuntimeError as ex:
            assert ex.code == 20
            assert ex.key == "RFC_INVALID_PARAMETER"
            assert ex.message == "field 'XRFCCHAR1' not found"


if __name__ == "__main__":
    unittest.main()
