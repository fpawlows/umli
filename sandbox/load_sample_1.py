import sys
import os

sys.path.append(os.getcwd())

if __name__ == "__main__":
    from uml_interpreter.deserializer.deserializer import EnterpriseArchitectXMLDeserializer

    model = EnterpriseArchitectXMLDeserializer.from_path("samples/sample_1.xml").read_model()

    diagram = model.diagrams[0]
    pass
