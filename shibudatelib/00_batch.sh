FILENAME="DKB01"
python 01_test_unit.py data/${FILENAME}.xml
python 02_custom_when.py data/${FILENAME}.xml_inf.xml
python 03_custom_time.py data/${FILENAME}.xml_inf.xml_custom_when.xml
python 04_custom_head.py data/${FILENAME}.xml_inf.xml_custom_when.xml_custom_time.xml