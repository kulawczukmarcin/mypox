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

from pox.forwarding.my_l2_multi import Switch


time_period = 5 # time between stats requests
threshhold = 3000000 # = 3Mbit/s
paths = defaultdict(lambda:defaultdict(lambda:[]))
log = core.getLogger()
sws = {} # switches
#host_switch_pair = defaultdict(lambda:None)


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
       if switch == dpidToStr(switch_port_pair[0].dpid) and port == switch_port_pair[2]:
          cookedpathobj.bytes_diff_list[cookedpathobj.cooked_path.index(switch_port_pair)] = \
            stats - cookedpathobj.bytes_diff_list[cookedpathobj.cooked_path.index(switch_port_pair)]
          # log.debug("Switch-port pair %s, %s", dpidToStr(switch_port_pair[0].dpid), switch_port_pair[2])
          # log.debug("Bytes sent overall: %s", stats)
          log.debug("Path: %s", cookedpathobj.cooked_path)
          log.debug("Bytes diff list: %s", cookedpathobj.bytes_diff_list)
          cookedpathobj.path_coefficient = max(cookedpathobj.bytes_diff_list[:-1])
          # log.debug("Path coeff: %s", cookedpathobj.path_coefficient)

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
  #log.debug("FlowStatsReceived from %s: %s",
  #  dpidToStr(event.connection.dpid), stats)
  for flow_stats in event.stats:
    # log.debug("Bytes in flow match%s: %s",
    #   flow_stats.match, flow_stats.byte_count)

    # ALL THIS HAS TO BE CHECK YET !!! - > no duplications, add flow deleting after some time, etc.
    # We want to gather stats for flow only in switch connected to src host
    # to avoid duplication
    if host_switch_pair[flow_stats.match.dl_src][0] == event.connection.dpid:
      # log.debug("Flow stats found ", flow_stats.match.dl_src, host_switch_pair[flow_stats.match.dl_src], event.connection.dpid)
      # Only IP flows
      if flow_stats.match.dl_type == 0x800:
        log.debug('IP Matched')
        flow_match5 = [flow_stats.match.nw_proto, flow_stats.match.nw_src, flow_stats.match.nw_dst, \
                       flow_stats.match.tp_src, flow_stats.match.tp_dst]
        from pox.forwarding.my_l2_multi import flow_list
        for flow in flow_list:
          #print "Flow match stat", flow_match5
          #print "Flow match List", flow.match, "\n"
          if flow.match5 == flow_match5:
            log.debug("Flow 5 Match found")
            if flow.changed == 1:
              break # we only change path once
            # TO DO -> handle timeouts, different switches etc.
            # we want to take stats only from switch connected to host to avoid complications
            flow.byte_diff = flow_stats.byte_count - flow.byte_count
            log.debug("Bytes: received from stats %s, from this flow last checked %s, diff %s, bandwith in bits %s",
                      flow_stats.byte_count, flow.byte_count,  flow.byte_diff, flow.byte_diff/time_period*8)
            flow.byte_count = flow_stats.byte_count

            if flow.byte_diff/time_period*8 > threshhold:
              log.debug("Uuuuuu, found big flow! %s", flow.match)
              print "Sw src, sw dst: ", flow.switch_src, flow.switch_dst
              best_path = find_best_path(flow.switch_src, flow.switch_dst)
              print "best path, flow path:"
              print best_path, "\n", flow.path
              if best_path != flow.path and best_path is not None:
                print "Path of big flow is not the best path!"
                Switch.delete_path(sws[event.connection.dpid], flow.path, flow.match)
                Switch._install_path(sws[event.connection.dpid], best_path, flow.match)
                flow.path = best_path
                flow.changed = 1

            break


# handler to display port statistics received in JSON format
def _handle_portstats_received (event):
  stats = flow_stats_to_list(event.stats)
  # log.debug("PortStatsReceived from %s: %s",
  #  dpidToStr(event.connection.dpid), stats)

  for f in event.stats:
    if int(f.port_no)<65534:
      apply_stats_to_paths(dpidToStr(event.connection.dpid), f.port_no, f.tx_bytes)


def find_best_path(src, dst):
  best_path_coeff = None
  best_path = None
  from pox.forwarding.my_l2_multi import CookedPath
  print "Cooked paths:"
  for cookedpathobj in CookedPath:
    if cookedpathobj.switch_src == src and cookedpathobj.switch_dst == dst:
      print cookedpathobj.cooked_path
      print cookedpathobj.bytes_diff_list, cookedpathobj.path_coefficient

      if best_path_coeff is None:
        best_path_coeff = cookedpathobj.path_coefficient
        best_path = cookedpathobj.cooked_path
        log.debug("Best path: %s, coeff: %s", best_path, best_path_coeff)
      elif cookedpathobj.path_coefficient < best_path_coeff:
        best_path_coeff = cookedpathobj.path_coefficient
        best_path = cookedpathobj.cooked_path
        log.debug("Best path: %s, coeff: %s", best_path, best_path_coeff)
  return best_path




# main functiont to launch the module
def launch ():
  from pox.lib.recoco import Timer

  # attach handsers to listners
  core.openflow.addListenerByName("FlowStatsReceived",
    _handle_flowstats_received)
  core.openflow.addListenerByName("PortStatsReceived",
    _handle_portstats_received)

  # timer set to execute every five seconds
  Timer(time_period, _timer_func, recurring=True)