import sys, os

testdir = os.path.dirname(__file__)
srcdir = '../'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import filesystem_limitations

#if __name__ == '__main__':
#    unittest.main()

#fl = filesystem_limitations()
#filename = test_options.get_shortened_substitution_filename(test_options.template, test_options.temp_dict)
#print(filename)
#test_options.get_output_directory();
#print(test_options.get_max_chars_for_output_directory_files())
#print(fl.get_filesystem_limitations(os.getcwd()))
#print(fl._get_windows_volume_info_with_kernel32(os.getcwd()))

current_dir = os.getcwd()
limits = filesystem_limitations.get(current_dir)
print("Current dir:")
print(current_dir)
print("Limits:")
print(limits)
