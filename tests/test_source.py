"""Stdlib checks only; no notebook execution, training, plots or dependency imports."""
import ast
import csv
import importlib.util
import json
import math
from pathlib import Path
import tempfile
import types
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('synthetic',ROOT/'generate_synthetic_data.py')
synthetic=importlib.util.module_from_spec(spec);spec.loader.exec_module(synthetic)


class SourceTests(unittest.TestCase):
    def notebook(self):return json.loads((ROOT/'neural_network_basics.ipynb').read_text())

    def test_notebook_is_code_only_and_all_outputs_metadata_removed(self):
        notebook=self.notebook()
        self.assertEqual(notebook['metadata'],{})
        self.assertEqual(len(notebook['cells']),27)
        for cell in notebook['cells']:
            self.assertEqual(cell['cell_type'],'code')
            self.assertEqual(cell['metadata'],{})
            self.assertEqual(cell['outputs'],[])
            self.assertIsNone(cell['execution_count'])
            ast.parse(''.join(cell['source']))

    def test_initial_guard_refuses_before_dependency_imports(self):
        source=''.join(self.notebook()['cells'][0]['source'])
        with self.assertRaises(RuntimeError):exec(compile(source,'notebook_guard','exec'),{})

    def test_selected_reviewed_sigmoid_function_handles_extreme_values(self):
        node=next(node for cell in self.notebook()['cells'] for node in ast.parse(''.join(cell['source'])).body if isinstance(node,ast.FunctionDef) and node.name=='sigmoid')
        namespace={'np':types.SimpleNamespace(exp=math.exp,clip=lambda x,lower,upper:max(lower,min(upper,x)))}
        exec(compile(ast.Module(body=[node],type_ignores=[]),'reviewed_sigmoid','exec'),namespace)
        self.assertEqual(namespace['sigmoid'](0),0.5)
        self.assertTrue(math.isfinite(namespace['sigmoid'](-100000)))
        self.assertEqual(namespace['sigmoid'](100000),1.0)

    def test_synthetic_generator_is_repeatable_and_refuses_overwrite(self):
        parent=ROOT/'.test-work';parent.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=parent) as temporary:
            a=Path(temporary)/'first.csv';b=Path(temporary)/'second.csv'
            synthetic.generate(a,8);synthetic.generate(b,8)
            self.assertEqual(a.read_bytes(),b.read_bytes())
            with a.open(encoding='utf-8') as stream:
                self.assertEqual(len(list(csv.DictReader(stream))),8)
            with self.assertRaises(FileExistsError):synthetic.generate(a,8)
        with self.assertRaises(ValueError):synthetic.generate('not-created.csv',1001)


if __name__=='__main__':unittest.main()
