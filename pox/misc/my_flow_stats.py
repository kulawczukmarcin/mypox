#!/usr/bin/python
# Copyright 2012 William Yu
# wyu@ateneo.edu
#
# This file is part of POX.
#
# POX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# POX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with POX. If not, see <http://www.gnu.org/licenses/>.
#

"""
This is a demonstration file created to show how to obtain flow
and port statistics from OpenFlow 1.0-enabled switches. The flow
statistics handler contains a summary of web-only traffic.
"""

# standard includes
from pox.core import core
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of
from collections import defaultdict

# include as part of the betta branch
from pox.openflow.of_json import *

paths = defaultdict(lambda:defaultdict(lambda:[]))
log = core.getLogger()
sws = {} # switches
flow_list = [] # list of all flows
#host_switch_pair = defaultdict(lambda:None)

class Flow:
  def __init__ (self):
    self.proto = None # type of protocol [tcp/udp -> not 100% sure]
    self.ip_src = None
    self.ip_dst = None
    # ports of transport protocol [tcp/udp]
    self.tp_src = None
    self.tp_dst = None
    self.match = [self.proto, self.ip_src, self.ip_dst, self.tp_src, self.tp_dst]
    self.switch_src = None # switch connected to ip_src host
    self.switch_dst = None # switch connected to ip_dst host
    self.path = None
    self.byte_count = None
    self.byte_diff = None


# get paths from my_l2_multi module
def get_paths():
  global sws
  from pox.forwarding.my_l2_multi import switches
  if sws != switches:
    sws = switches
    log.debug("NOT EQUAL - switches has changed since last time we checked")
    # to do - > add some clearing for stats
  else:
    # log.debug("EQUAL")
    pass
  for sw in sws.values():
      #log.debug("Switch %s, ports %s", dpidToStr(sw.dpid), sw.ports)
      pass

  global paths
  from pox.forwarding.my_l2_multi import all_cooked_paths
  if paths != all_cooked_paths:
    paths = all_cooked_paths
    log.debug("NOT EQUAL - paths has changed since last time we checked")
    # to do - > add some clearing for stats
  else:
    log.debug("EQUAL - paths has not changed since last time we checked")

  from pox.forwarding.my_l2_multi import host_switch_pair
  global host_switch_pair



# when _handle_portstats_received will receive stats for port on switch
# it will send them here to be applied for paths,
# stats here are bytes sent by this port
def apply_stats_to_paths(switch, port, stats):
  # global paths
  # log.debug("Checking switch %s port %s ", switch, port )
  # for src in sws.values():
  #   for dst in sws.values():
  #     for path in paths[src][dst]:
  #       for switch_port_pair in path:
  #         #log.debug("switch-port pair %s, %s", dpidToStr(switch_port_pair[0].dpid), switch_port_pair[1] )
  #         if switch == dpidToStr(switch_port_pair[0].dpid) and port == switch_port_pair[1]:
  #           # log.debug("switch-port pair %s, %s", dpidToStr(switch_port_pair[0].dpid), switch_port_pair[1] )
  #           # log.debug(path)
  #           # switch_port_pair.append(stats) -> this isn't working, what is better?
  #           # to do -> how append stats?
  #           # print stats
  #           pass
  from pox.forwarding.my_l2_multi import CookedPath
  for cookedpathobj in CookedPath:
    for switch_port_pair in cookedpathobj.cooked_path:
       if switch == dpidToStr(switch_port_pair[0].dpid) and port == switch_port_pair[1]:
          cookedpathobj.bytes_diff_list[cookedpathobj.cooked_path.index(switch_port_pair)] = \
            stats - cookedpathobj.bytes_diff_list[cookedpathobj.cooked_path.index(switch_port_pair)]
          log.debug("Switch-port pair %s, %s", dpidToStr(switch_port_pair[0].dpid), switch_port_pair[1])
          log.debug("Bytes sent overall: %s", stats)
          log.debug("Path: %s", cookedpathobj.cooked_path)
          log.debug("Bytes diff list: %s", cookedpathobj.bytes_diff_list)
          cookedpathobj.path_coefficient = min(cookedpathobj.bytes_diff_list)
          log.debug("Path coeff: %s", cookedpathobj.path_coefficient)

# handler for timer function that sends the requests to all the
# switches connected to the controller.
def _timer_func ():
  get_paths()
  for connection in core.openflow._connections.values():
    connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
    connection.send(of.ofp_stats_request(body=of.ofp_port_stats_request()))
  log.debug("Sent %i flow/port stats request(s)", len(core.openflow._connections))

# handler to display flow statistics received in JSON format
# structure of event.stats is defined by ofp_flow_stats()
def _handle_flowstats_received (event):
  stats = flow_stats_to_list(event.stats)
  log.debug("FlowStatsReceived from %s: %s",
    dpidToStr(event.connection.dpid), stats)
  for flow_stats in event.stats:
    # log.debug("Bytes in flow match%s: %s",
    #   flow_stats.match, flow_stats.byte_count)

    # We want to gather stats for flow only in switch connected to src host
    # to avoid duplication

    # ALL THIS HAS TO BE CHECK YET !!! - > no duplications, add flow deleting after some time, etc.
    #log.debug("Flow stats found %s %s %s %s", flow_stats.match.dl_src, type(flow_stats.match.dl_src), \
    # host_switch_pair[flow_stats.match.dl_src],  event.connection.dpid)
    if host_switch_pair[flow_stats.match.dl_src] == event.connection.dpid:
      # log.debug("Flow stats found ", flow_stats.match.dl_src, host_switch_pair[flow_stats.match.dl_src], event.connection.dpid)
      # Only IP flows
      if flow_stats.match.dl_type == 0x800:
        print 'IP Matched'
        flow_match5 = [flow_stats.match.nw_proto, flow_stats.match.nw_src, flow_stats.match.nw_dst, \
                       flow_stats.match.tp_src, flow_stats.match.tp_dst]
        for flow in flow_list:
          if flow.match == flow_match5:
            # TO DO -> handle timeouts, different switches etc.
            # we want to take stats only from switch connected to host to avoid complications
            flow.byte_diff = flow.byte_count - flow_stats.byte_count
            flow.byte_count = flow_stats.byte_count
            continue

        # if no match for flow is found in flow list we add new instance
        f = Flow()
        f.proto = flow_stats.match.nw_proto # type of protocol [tcp/udp -> not 100% sure]
        f.ip_src = flow_stats.match.nw_src
        f.ip_dst = flow_stats.match.nw_dst
        # ports of transport protocol [tcp/udp]
        f.tp_src = flow_stats.match.tp_src
        f.tp_dst = flow_stats.match.tp_dst

        # to do -> how to do this?
        f.switch_src = None # switch connected to ip_src host
        f.switch_dst = None # switch connected to ip_dst host
        f.path = None

        f.byte_count = flow_stats.byte_count
        flow_list.append(f)



  # not really needed
  # Get number of bytes/packets in flows for web traffic only
  # web_bytes = 0
  # web_flows = 0
  # web_packet = 0
  # for f in event.stats:
  #   if f.match.tp_dst == 80 or f.match.tp_src == 80:
  #     web_bytes += f.byte_count
  #     web_packet += f.packet_count
  #     web_flows += 1
  #log.info("Web traffic from %s: %s bytes (%s packets) over %s flows",
  #   dpidToStr(event.connection.dpid), web_bytes, web_packet, web_flows)

# handler to display port statistics received in JSON format
def _handle_portstats_received (event):
  stats = flow_stats_to_list(event.stats)
  # log.debug("PortStatsReceived from %s: %s",
  #  dpidToStr(event.connection.dpid), stats)

  for f in event.stats:
    if int(f.port_no)<65534:
      apply_stats_to_paths(dpidToStr(event.connection.dpid), f.port_no, f.tx_bytes)


# main functiont to launch the module
def launch ():
  from pox.lib.recoco import Timer

  # attach handsers to listners
  core.openflow.addListenerByName("FlowStatsReceived",
    _handle_flowstats_received)
  core.openflow.addListenerByName("PortStatsReceived",
    _handle_portstats_received)

  # timer set to execute every five seconds
  Timer(5, _timer_func, recurring=True)