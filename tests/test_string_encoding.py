import xml.etree.ElementTree as ET

import testutils

if __name__ == "__main__":
    testutils.run_using_pytest(globals())

import suds
import suds.store

import pytest

def test_string_preserved():
    def client(xsd, *input):
        wsdl = testutils.wsdl(xsd, input=input, xsd_target_namespace="toolyan",
            operation_name="f")
        return testutils.client_from_wsdl(wsdl, nosend=True, prettyxml=True)

    client_bare_single = client("""<xsd:element name="Elemento" type="xsd:string"/>""", "Elemento")

    data = "Maestro n=\n r=\r rn=\r\n tada!"
    def call_single(c):
        return c.service.f(data)

    msg = call_single(client_bare_single)
    print(msg.envelope)
    
    root = ET.fromstring(msg.envelope)
    print(root)

    namespaces = {'SOAP-ENV': 'http://schemas.xmlsoap.org/soap/envelope/','ns0':"http://schemas.xmlsoap.org/soap/envelope/", 'ns1' : 'toolyan'} # add more as needed
    assert root.find("ns0:Body/ns1:Elemento", namespaces).text == data
