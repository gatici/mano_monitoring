#osm nst-delete  mslice1_nst
osm  nsd-delete  simple_ee-ns
#for  i  in  amf smf upf  udm udr  pcf ausf nrf 
#do
	#osm vnfd-delete  mslice1_$i'_vnfd'  
#done
osm vnfd-delete simple_ee-vnf
