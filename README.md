# Shell-Tools
Different kinds of shell tools developed by Python are used for controlling PC and dealing small errands

Files:
shell_tools is the main program of this shell tool sets
WolCmd.exe is the program which is used to wake on lan in Windows platform

The following is an example for auto waking on LAN and remote connecting to the PC

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
