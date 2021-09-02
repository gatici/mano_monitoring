#for  i  in  amf smf upf  udm udr  pcf ausf nrf 
#do
	tar -czvf  mslice1_$i'_vnfd.tar.gz'  mslice1_$i'_vnfd'
#done
tar  -czvf simple_ee_ns.tar.gz  simple_ee_ns
tar  -czvf simple_ee_vnf.tar.gz  simple_ee_vnf

