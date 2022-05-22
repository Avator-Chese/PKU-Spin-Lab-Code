QDInstrument.dll is necessary whether local or remote control. Specially, for remote operation(Ours is DynaCool), the local computer must have "QDInstrument.dll", 
the MultiVu computer must have "QDInstrument_server.exe", which connect the local and remote computer.

For PPMS(6000) and DynaCool, "PPMSControl.py" line-31,32 should be concerned.

"Defualt Port" should be checked on "QDInstrument_server.exe". "ip_adress" is should also find at remote computer.


"sqm.py" is the core control file which can control PPMS and 2002/2400,ect.

"RunFile.py" is the one user need to operate. The left files, users had better not change.
