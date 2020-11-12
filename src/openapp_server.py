#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
from collections import deque, defaultdict
import time
import logging
import os
from threading import Thread, Lock

import grpc

import openappwrapper_pb2
import openappwrapper_pb2_grpc
import openapp_common

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)

class Opener(openappwrapper_pb2_grpc.OpenerServicer):
    def __init__(self):
        self.command_queue = defaultdict(deque)
        self.connection_status = {}
        self.mutex = Lock()

    """
    # Direct Connect Mode.
    def Open(self, request, context):
        if request.mode == 'open':
            command = "open " + request.command
            os.system(command)
            message = '[Done]: ' + command
        elif request.mode == 'copy':
            command = "echo \"" + request.command + "\" | tr -d '\n' | pbcopy "
            os.system(command)
            message = '[Done]: ' + command
        else:
            message = '[Failed]: ' + request.mode + ' ' + request.command
        message = message.replace('\n', '\ n')
        logger.warning(message)
        return openappwrapper_pb2.DebugReply(message=message)
    """

    def Open(self, request, context):
        logger.warning('Command Received: {com}'.format(com=str(request)))
        self.mutex.acquire()
        self.command_queue[request.user].append(request)
        self.mutex.release()
        return openappwrapper_pb2.DebugReply(message='RPC SUC')

    def ListenForContent(self, request, context):
        machine_name = request.machine_name
        if machine_name in self.connection_status and self.connection_status[machine_name]:
            self.mutex.acquire()
            logger.warning('Disable original threads.')
            self.connection_status[machine_name] = False
            self.mutex.release()
            time.sleep(0.3)
        self.connection_status[machine_name] = True

        logger.warning('Start Listening for Machine: ' + request.machine_name)
        # Flush current pool
        logger.warning('--------- FLUSHING ---------')
        logger.warning(request)

        self.mutex.acquire()
        logger.warning(self.command_queue[request.machine_name])
        if self.command_queue[request.machine_name]:
            last_element = self.command_queue[request.machine_name].pop()
            self.command_queue[request.machine_name].clear()
            self.command_queue[request.machine_name].append(last_element)
        logger.warning('--------- DONE ---------')
        self.mutex.release()

        while True and self.connection_status[machine_name]:
            time.sleep(0.2)
            while self.command_queue[request.machine_name]:
                self.mutex.acquire()
                content = self.command_queue[request.machine_name].popleft()
                self.mutex.release()
                logger.warning('------ Content Yield ------')
                logger.warning(content)
                yield content
        logger.warning('Exit Listening...')

def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=20),
        options= openapp_common.GRPC_OPTIONS
    )
    openappwrapper_pb2_grpc.add_OpenerServicer_to_server(Opener(), server)
    server.add_insecure_port(openapp_common.SERVER_USED_CHANNEL)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
