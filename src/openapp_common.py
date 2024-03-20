#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020-03-21 Hanxiao <hah114@ucsd.edu>
#
# Distributed under terms of the MIT license.

"""
Common global values in openapp module
"""

CLIENT_DEBUG_CHANNEL = 'localhost:50051'
CLIENT_REAL_CHANNEL = '35.226.152.53:9100'
SERVER_DEBUG_CHANNEL = '[::]:50051'
SERVER_REAL_CHANNEL = '[::]:9100'
USER = 'hanxiaoh_corp'
GRPC_OPTIONS = (
    ('grpc.keepalive_time_ms', 10000),
    # send keepalive ping every 10 second, default is 2 hours
    ('grpc.keepalive_timeout_ms', 5000),
    # keepalive ping time out after 5 seconds, default is 20 seoncds
    ('grpc.keepalive_permit_without_calls', True),
    # allow keepalive pings when there's no gRPC calls
    ('grpc.http2.max_pings_without_data', 0),
    # allow unlimited amount of keepalive pings without data
    ('grpc.http2.min_time_between_pings_ms', 10000),
    # allow grpc pings from client every 10 seconds
    ('grpc.http2.min_ping_interval_without_data_ms',  5000),
    # allow grpc pings from client without data every 5 seconds
)

CLIENT_USED_CHANNEL = CLIENT_REAL_CHANNEL
SERVER_USED_CHANNEL = SERVER_REAL_CHANNEL
