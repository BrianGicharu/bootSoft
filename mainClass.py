import sys
import shutil

from subprocess import *

import re

import pymsgbox

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class window(QWidget):
    def __init__(self, parent=None):
        super(window, self).__init__(parent)

        self.resize(200, 50)
        self.setWindowTitle("BootSoft v1")
        self.setFixedSize(350, 400)
        self.setWindowIcon(QIcon('bootsoftlogo.png'))
        self.setStyleSheet("background-color:lightgray;background-repeat: no-repeat;background-position: center;")

        window_layout = QVBoxLayout()
        self.setLayout(window_layout)
        top_layout = QHBoxLayout()
        term_layout = QHBoxLayout()
        center_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()
        disk_display_layout = QHBoxLayout()

        font = QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(9)

        font1 = QFont()
        font1.setFamily("Segoe Print")
        font1.setPointSize(10)

        hyperlink_font = QFont()
        hyperlink_font.setFamily("Segoe Script")
        hyperlink_font.setPointSize(10)
        hyperlink_font.setItalic(True)

        # Colours
        green = QColor(100, 255, 100)

        # Global variables(in class)
        self.terminal_progress_text = ""
        # First diskpart system call
        prg_var = self.disk_part_call("list disk")
        mixed_stdout = str(prg_var).replace("\\r", "").replace("b'", "").replace("(", "").replace(")", "").replace(
            "\\n", "\n")

        # regex expression code to obtain the matching commands(stdout from diskpart)
        pattern = r"D\w+\s[\d]\s+\W+\w+\s+\d+\W+.."
        final_clean_stdout = "\n".join(re.findall(pattern, mixed_stdout))
        feed = final_clean_stdout.split("\n")

        # Guiding label on the purpose of disk_chooser widget
        self.label = QLabel(self)
        self.label.setText("Select the disk ---------->")
        self.label.setFont(font)
        window_layout.addLayout(top_layout)

        top_layout.addWidget(self.label)

        self.disk_chooser = QComboBox()
        self.disk_chooser.addItems(feed)
        index = self.disk_chooser.findText(feed[0], Qt.MatchFixedString)
        self.disk_chooser.setCurrentIndex(index)
        self.disk_chooser.setFont(font)

        top_layout.addWidget(self.disk_chooser)

        self.ok_button = QPushButton()
        self.ok_button.setText("START")
        self.ok_button.setFont(font1)
        self.ok_button.clicked.connect(self.click)

        window_layout.addLayout(center_layout)
        center_layout.addWidget(self.ok_button)

        window_layout.addLayout(term_layout)

        self.terminal_progress = QTextEdit()
        self.terminal_progress.setTextColor(green)
        self.terminal_progress.setReadOnly(True)
        self.terminal_progress.setText(mixed_stdout)
        self.terminal_progress.setFontPointSize(8)
        self.terminal_progress.setStyleSheet("background-color:black;background-repeat: "
                                             "no-repeat;background-position: center;")
        term_layout.addWidget(self.terminal_progress)

        self.disks_display = QTextEdit()
        self.disks_display.setReadOnly(True)
        line = "--------------------------------------------------\n"
        terminal_text = "DISK NO. STATUS   SIZE      BOOT FLAG\
            \n" + line + final_clean_stdout
        self.disks_display.setText(terminal_text)
        self.disks_display.setFontPointSize(10)
        disk_display_layout.addWidget(self.disks_display)

        window_layout.addLayout(disk_display_layout)

        follow_us = QLabel()
        follow_us.setAlignment(Qt.AlignLeft)
        follow_us.setFont(hyperlink_font)
        follow_us.setText("Plancks Code\nLab KE")
        follow_us.setOpenExternalLinks(True)

        support_me = QLabel()
        s_font = QFont()
        s_font.setFamily("Arial Black")
        support_me.setFont(s_font)
        support_me.setText("Contact Developer...0790431217")

        # ("briangicharu.wixsite.com/planckscodelab")

        bottom_layout.addWidget(follow_us)
        bottom_layout.addWidget(support_me)
        window_layout.addLayout(bottom_layout)

    # This method copies OS installation files to the
    def copyFiles(self):
        files = QFileDialog().getOpenFileName(self, 'CHOOSE OS FILES TO BE COPIED', 'C:\\Users')
        files.setFileMode(QFileDialog.AnyFile)
        if files.exec_():
            filenames = files.selectedFiles()
            shutil.copy(filenames, 'F:\\')

    def click(self):
        final_pattern = r"D\w+\s[\d]"
        selected_dsk = self.disk_chooser.currentText()
        returned = "select " + (("".join(re.findall(final_pattern, selected_dsk))).lower())
        pymsgbox.alert(returned.upper(), "confirm this selection...k")

        # The following code blocks the program from formatting 'disk 0' which is usually the default OS installation
        # drive
        # This saves your drive from involuntary data expungement/deletion/loss
        if returned == 'select disk 0':
            returned = 'exit'
            pymsgbox.alert("Working on OS HDD is very risky\nAlways select a HDD without a currently\nrunning "
                           "OS\nYour safety first", "WARNING!", "EXIT")
        # The following code forces the app to exit after the OS disk preventive measure against data loss
            sys.exit(QApplication.exec_())
            pass

        # A list of commands to be piped to popen stdin are initialized on the following code
        cmds = [returned, "clean", "create partition primary", "active", "format fs=fat32 quick"]
        pymsgbox.alert("THE SELECTED DISK\n"+returned+"\nWILL LOSE ALL ITS DATA", "WARNING!", "CONTINUE")
        p = Popen('diskpart.exe', stdin=PIPE, stdout=PIPE, stderr=PIPE)
        for cmd in cmds:
            x = cmd + '\n'
            p.stdin.write(x.encode("utf-8"))
        p.stdin.close()
        self.copyFiles()

    # open diskpart via popen pipe and send the output to the terminal-like widget
    @staticmethod
    def disk_part_call(disk_cmd):

        print(disk_cmd)
        call_text = Popen("C:\\Windows\\System32\\diskpart.exe", shell=True, stdin=PIPE, stdout=PIPE) \
            .communicate(input=disk_cmd.encode('utf-8'))

        green_text = str(call_text).replace("\\r", "").replace("b'", "").replace("(", "") \
            .replace(")", "").replace("\\n", "\n").replace("None", "")
        terminal_progress_text = disk_cmd + green_text
        print(terminal_progress_text)
        return green_text


# The program is invoked from here
def main():
    app = QApplication(sys.argv)
    ex = window()
    ex.show()
    sys.exit(app.exec_())


# condition that aids on invoking 'main' function
if __name__ == '__main__':
    main()
