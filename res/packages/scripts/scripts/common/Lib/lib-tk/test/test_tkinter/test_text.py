# 2017.08.29 21:57:29 St�edn� Evropa (letn� �as)
# Embedded file name: scripts/common/Lib/lib-tk/test/test_tkinter/test_text.py
import unittest
import Tkinter
from test.test_support import requires, run_unittest
from ttk import setup_master
requires('gui')

class TextTest(unittest.TestCase):

    def setUp(self):
        self.root = setup_master()
        self.text = Tkinter.Text(self.root)

    def tearDown(self):
        self.text.destroy()

    def test_debug(self):
        text = self.text
        olddebug = text.debug()
        try:
            text.debug(0)
            self.assertEqual(text.debug(), 0)
            text.debug(1)
            self.assertEqual(text.debug(), 1)
        finally:
            text.debug(olddebug)
            self.assertEqual(text.debug(), olddebug)

    def test_search(self):
        text = self.text
        self.assertRaises(Tkinter.TclError, text.search, None, '1.0')
        self.assertRaises(Tkinter.TclError, text.search, 'a', None)
        self.assertRaises(Tkinter.TclError, text.search, None, None)
        self.assertRaises(Tkinter.TclError, text.search, '', 0)
        text.insert('1.0', 'hi-test')
        self.assertEqual(text.search('-test', '1.0', 'end'), '1.2')
        self.assertEqual(text.search('test', '1.0', 'end'), '1.3')
        return


tests_gui = (TextTest,)
if __name__ == '__main__':
    run_unittest(*tests_gui)
# okay decompyling c:\Users\PC\wotmods\files\originals\res\packages\scripts\scripts\common\Lib\lib-tk\test\test_tkinter\test_text.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.08.29 21:57:30 St�edn� Evropa (letn� �as)
