import sys
import os

sys.path.append(os.getcwd())

if __name__ == "__main__":
    from uml_interpreter.deserializer.enterprise_architect.ea_xml_deserializer import (
        EAXMLDeserializer,
    )

    model = EAXMLDeserializer.from_path("samples/MODEL_XMI.xml").read_model()
    model.print()
