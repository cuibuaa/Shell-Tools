from os import system
from os import popen
import re
import threading
import time
import platform
import socket

class shell_tools:

    def __init__(self):
        cmd_dic = {
            'Windows':{'ARP':'arp -a',
                       'PING':'ping %s -n 1',
                       'REMOTE': 'mstsc /v:%s',
                       'WOL':'wolcmd %s %s %s 7'},
            'Linux':{'ARP':'arp -a',
                     'PING':'ping %s -c 1',
                     'REMOTE':'vncviewer %s'},
            'Mac':None #TBD
            }
        self.system = platform.system()
        #print(self.system)
        self.cmd_dic = cmd_dic.get(self.system)
        #print(self.cmd_dic)
        if not self.cmd_dic :
            raise RuntimeError("None cmd list matched, please check the cmd_dic")

    def cmd_ping(self, ip):
        popen(self.cmd_dic['PING'] % ip)

    def cmd_remote(self, ip):
        popen(self.cmd_dic['REMOTE'] % ip)

    def cmd_wol(self, mac, ip, mask):
        #first convert the mac format to the command pattern
        mac = mac.replace('-','')
        ret = popen(self.cmd_dic['WOL'] % (mac, ip, mask)).read()
        print(ret)

    def cmd_rarp(self, mac, domain, start = 1, end = 255, timeout = 30):

        start = max(1,start)
        end = min(255,end)
                
        for i in range(0, timeout):
            self.scan_lan(domain, start, end)
            ret = self.find_ip(mac)
            if ret :
                return ret
            time.sleep(1)
        return None

    def scan_lan (self, domain, start = 1, end = 255) :

        start = max(1,start)
        end = min(255,end)
        
        thread_list = []
        for i in range (start, end):
            t = threading.Thread(target = self.cmd_ping, args = (('%s.%d' % (domain, i)),))
            thread_list.append(t)
            t.start()
            print("Thread %d is started \n" % i)

        for t in thread_list:
            t.join()

    def find_ip (self, mac):
        reg = r'((\d{1,3}\.){3}\d{1,3})\s*%s' % mac
        ipre = re.compile(reg)
        ret = popen(self.cmd_dic['ARP']).read()
        iplist = re.findall(ipre,ret)

        if iplist:
            return iplist[0][0]
        else:
            return None

    def get_localip(self):
        ret = popen(self.cmd_dic['IP']).read()
        reg = r'((\d{1,3}\.){3}\d{1,3})'
        ipre = re.compile(reg)
        iplist = re.findall(ipre,ret)

        for ip in iplist:
            if ip[0].find('255') == -1:
                return ip[0]
        return None

    def convert_ip2domain(self, ip):
        ret_ip = ip.split('.')
        if len(ret_ip) != 4:
            raise RuntimeError("The IP address format is error")
        del ret_ip[-1]
        ret_ip = '.'.join(ret_ip)
        return ret_ip

    def check_idle_ip(self, domain, start = 1, end = 255) :
        #scan the lan first to make sure the ARP cache is flushed
        self.scan_lan(domain, start, end)
        
        reg = r'%s\.(\d{1,3})' % domain
        ipre = re.compile(reg)
        ret = popen(self.cmd_dic['ARP']).read()
        iplist = re.findall(ipre,ret)
        lastip = 0
        idle_list = []

        for ip in iplist:
            iip = int(ip)
            if iip >= start:
                if not lastip:
                    lastip = iip
                else:
                    for i in range(lastip + 1, iip):
                        idle_list.append('%s.%d' % (domain,i))
                lastip = iip

        for i in range(lastip + 1, end):
            idle_list.append('%s.%d' % (domain,i))


        print('Idle IP is following')
        for idle_ip in  idle_list :
            print(idle_ip)
        
if __name__ == '__main__':  
    # an example for auto wake on LAN and remote connect to the PC
    
    st = shell_tools()
    #set your remote PC MAC address here
    mac = 'xx-xx-xx-xx-xx-xx'
    mac = mac.lower()
    #get local ip and ip domain
    ip = st.get_localip()
    ip_domain = st.convert_ip2domain(ip)
    #wake on LAN the target PC
    st.cmd_wol(mac, ip, '255.255.255.0')
    #RAPP the target IP
    ip = st.cmd_rarp(mac, ip_domain, 10, 20)
    #Remote connection
    if ip :
        st.cmd_remote(ip)
    else:
        print('Can not find the IP according to this mac: %s ' % mac)
    
                
        
