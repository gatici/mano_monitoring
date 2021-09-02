#for  i  in  amf smf upf  udm udr  pcf ausf nrf 
#do
	#osm vnfd-create  mslice1_$i'_vnfd.tar.gz'  
#done
osm vnfd-create snmp_ee_vnf.tar.gz
osm  nsd-create  snmp_ee_ns.tar.gz  
#osm nst-create mslice1_nst3.yaml

