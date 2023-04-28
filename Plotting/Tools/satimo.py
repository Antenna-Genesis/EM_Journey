"""
class to deal with 1d data from Satimo
"""
import pandas as pd
import warnings


class Result1d(object):
    """
    1D Result from Satimo Export
    """
    data_unique_line_allowed = ['1']

    def __init__(self, filename, data_unique_line=data_unique_line_allowed):
        self.data_unique_line = data_unique_line
        self.read_txt(filename)
        self.legends = []
        self.plot_xlabel = 'x-axis'
        self.plot_ylabel = 'y-axis'
        self.all_lines = 'import_data'

    def read_txt(self, filename):
        with open(filename, 'r') as raw_data:
            self.all_lines = raw_data.readlines()
            #  "with" ensures the file is always cleaned up promptly and correctly
            print('Importing lines from CST table txt file...')
        first_two_lines = self.all_lines[:2]  # to check how the data is obtained
        if self.data_unique_line[0] in first_two_lines[0]:
            print('CST data was obtained via Copy-Paste method')
        elif self.data_unique_line[1] in first_two_lines[1]:
            print('CST data was obtained via Export method')
            """
            data format of exported ASCII file
                    Frequency / GHz                Gain_RHCP,theta=0,phi=0.0,Value (Mesh Pass=1)/real\n
                    ----------------------------------------------------------------------\n
                    ...
                    \n
                    ...
                    \n
                    \n (however, this line will not show with file opening method)
            """
            self.importdata2pd()
        else:
            warnings.warn('Only method of Copy-Paste and Export are allowed.')

    def importdata2pd(self):
        self.legends = []
        all_lines_num = len(self.all_lines)
        curve_num = self.all_lines.count(self.data_unique_line[1])
        single_line_num = int(all_lines_num / curve_num)
        x_list = [[item.split()[0]] for item in self.all_lines[2:single_line_num - 1]]
        data_list = x_list
        self.plot_xlabel = self.all_lines[0].split()[0]
        self.plot_ylabel = self.all_lines[0].split()[3]
        for curve_indx in range(curve_num):
            self.legends.append(self.all_lines[curve_indx * single_line_num].split("(")[1].split(")")[0])
            for x_indx in range(2, single_line_num - 1):
                all_indx = curve_indx * single_line_num + x_indx
                line_content = self.all_lines[all_indx].split()
                data_line = float(line_content[1])
                x_indx_pd = x_indx - 2  # skip two line on top
                data_list[x_indx_pd].append(data_line)
        self.legends.insert(0, self.plot_xlabel)
        self.data_df = pd.DataFrame(data_list, columns=self.legends)

# if __name__ == '__main__':
#     import os
#     import pysnooper
#     import time
#
#     start_time = time.time()
#     named_tuple = time.localtime()  # get struct_time
#     time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
#     print(f'This program started at: {time_string}')
#     current_dir = os.getcwd()  # get current dir
#     log_dir = os.path.join(current_dir, 'LogFiles')
#     if not os.path.exists(log_dir):
#         os.makedirs(log_dir)
#     log_file = os.path.join(log_dir, 'time_string.log')