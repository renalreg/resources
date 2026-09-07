# This script converts Shaun's XLS document
# Into 3 CSV files to match the table structure

import csv
import itertools


def main():
    # Code List

    csvreader = csv.reader(open("C:/Temp/PV2_Test_harmonisation.csv", "r"))

    code_list = list()
    code_conv_list = list()
    unit_conv_list = list()

    next(csvreader)
    for row in csvreader:

        test_code = row[0]
        unit_code = row[1]
        correct_test_code = row[3]
        correct_unit_code = row[4]
        record_type = row[5]

        # creatinine,µmol/l,68,creatinine,micromol/L,result,

        code_list.append(("PV", correct_test_code, None, record_type))
        if correct_test_code not in ("", None):
            code_conv_list.append(("PVMIGRATION", test_code, "PV", correct_test_code))
        if correct_unit_code not in ("", None):
            unit_conv_list.append(("PVMIGRATION", unit_code, "PV", correct_unit_code))

    # Code List
    code_list.sort()
    code_list = list(code_list for code_list, _ in itertools.groupby(code_list))

    csvwriter = csv.writer(open("C:/Temp/CodeList.csv", "w", newline=""))

    for row in code_list:
        csvwriter.writerow(row)

    # Code Conv List
    code_conv_list.sort()
    code_conv_list = list(
        code_conv_list for code_conv_list, _ in itertools.groupby(code_conv_list)
    )

    csvwriter = csv.writer(open("C:/Temp/CodeConvList.csv", "w", newline=""))

    for row in code_conv_list:
        csvwriter.writerow(row)

    # Unit Conv List
    unit_conv_list.sort()
    unit_conv_list = list(
        unit_conv_list for unit_conv_list, _ in itertools.groupby(unit_conv_list)
    )

    csvwriter = csv.writer(open("C:/Temp/UnitConvList.csv", "w", newline=""))

    for row in unit_conv_list:
        csvwriter.writerow(row)


if __name__ == "__main__":
    main()
