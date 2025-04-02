import untangle
xsd_file = "/Users/ksloan/Workbenches/OpenStudioWorkBench/utils/GBxml.xsd"
obj = untangle.parse(xsd_file)

res = obj.xs_schema.xs_element.xs_complexType.xs_sequence.xs_element.xs_complexType.xs_sequence.xs_element.xs_simpleType.xs_restriction.xs_enumeration
