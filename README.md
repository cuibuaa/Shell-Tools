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
#set your local ip and netmask here
st.cmd_wol(mac, '172.16.8.10', '255.255.255.0')
#set your local scanning ip range 
ip = st.cmd_rarp(mac, '172.16.8', 10, 20)
if ip :
    st.cmd_remote(ip)
else:
    print('Can not find the IP according to this mac: %s ' % mac)
