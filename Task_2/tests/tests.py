import unittest
from main import (
    parse_nuspec,
    generate_dot_graph,
)

class TestPackageManager(unittest.TestCase):
    def test_parse_nuspec(self):
        nuspec_content = b'<dependencies><dependency id="Dep1"/><dependency id="Dep2"/></dependencies>'
        dependencies = parse_nuspec(nuspec_content)
        self.assertEqual(dependencies, {'Dep1', 'Dep2'})

    def test_generate_dot_graph(self):
        package_name = "TestPackage"
        dependencies = {"Dep1", "Dep2"}
        dot_graph = generate_dot_graph(package_name, dependencies)

        expected_dot = (
            'digraph G {\n'
            '    graph [layout=neato, overlap=false, splines=true];\n'
            '    "TestPackage"\n'
            '    "Dep1" -> "TestPackage";\n'
            '    "Dep2" -> "TestPackage";\n'
            '}'
        )
        self.assertEqual(dot_graph, expected_dot)

if __name__ == '__main__':
    unittest.main()
