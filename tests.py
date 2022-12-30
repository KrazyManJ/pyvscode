import unittest
from src import pyvscode

class pyvscodeTesting(unittest.TestCase):
    def test_type_errors(self):
        #open()
        self.assertRaises(TypeError,pyvscode.open,1)
        self.assertRaises(TypeError,pyvscode.open,[1])
        #goto_file()
        self.assertRaises(TypeError,pyvscode.goto_file,"myfile.txt","line 68")
        self.assertRaises(TypeError,pyvscode.goto_file,"myfile.txt",68,"char 89")
        #open_difference()
        self.assertRaises(TypeError,pyvscode.open_difference,5,"myfile.txt")
        self.assertRaises(TypeError,pyvscode.open_difference,"myfile.txt",5)
        #extension functions()
        self.assertRaises(ValueError,pyvscode.install_extension,"publisher name")
        self.assertRaises(ValueError,pyvscode.uninstall_extension,"publisher name")

if __name__ == '__main__':
    unittest.main()
