# Copyright (C) 2014 Google Inc.
#
# This file is part of ycmd.
#
# ycmd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ycmd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ycmd.  If not, see <http://www.gnu.org/licenses/>.

import os
import ycm_core

# These are the compilation flags that will be used in case there's no
# compilation database set (by default, one is not set).
# CHANGE THIS LIST OF FLAGS. YES, THIS IS THE DROID YOU HAVE BEEN LOOKING FOR.
flags = [
    "-std=c++17",
    "-pedantic",
    "-Wall",
    "-Wextra",
    "-fno-exceptions",
    "-fno-rtti",
    "-x",
    "c++",
    # system
    "-isystem",
    "/usr/local/include",
    "-isystem",
    "/Library/Developer/CommandLineTools/usr/bin/../include/c++/v1",
    "-isystem",
    "/Library/Developer/CommandLineTools/usr/lib/clang/11.0.0/include",
    "-isystem",
    "/Library/Developer/CommandLineTools/usr/include",
    "-isystem",
    "/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include",
    # third
    "-isystem",
    "/usr/local/Cellar/opencv/4.2.0_1/include/opencv4",
    "-isystem",
    "/usr/local/Cellar/eigen/3.3.7/include/eigen3",
    "-isystem",
    "/usr/local/Cellar/fmt/6.1.2/include",
    "-isystem",
    "/usr/local/Cellar/openblas/0.3.7/include",
    # proj
    "-isystem",
    "/Users/ling/Projects/cmake_cxx_submodule/include",
    "-isystem",
    "/Users/ling/Projects/cmake_cxx_submodule/inner/include/",
    "-isystem",
    "/Users/ling/Projects/cmake_cxx_submodule/gtest/googletest/include",
]


# Set this to the absolute path to the folder (NOT the file!) containing the
# compile_commands.json file to use that instead of 'flags'. See here for
# more details: http://clang.llvm.org/docs/JSONCompilationDatabase.html
#
# Most projects will NOT need to set this to anything; you can just change the
# 'flags' list of compilation flags.
compilation_database_folder = ""

if os.path.exists(compilation_database_folder):
    database = ycm_core.CompilationDatabase(compilation_database_folder)
else:
    database = None

SOURCE_EXTENSIONS = [".cpp", ".cxx", ".cc", ".c", ".m", ".mm"]


def DirectoryOfThisScript():
    return os.path.dirname(os.path.abspath(__file__))


def IsHeaderFile(filename):
    extension = os.path.splitext(filename)[1]
    return extension in [".h", ".hxx", ".hpp", ".hh"]


def GetCompilationInfoForFile(filename):
    # The compilation_commands.json file generated by CMake does not have entries
    # for header files. So we do our best by asking the db for flags for a
    # corresponding source file, if any. If one exists, the flags for that file
    # should be good enough.
    if IsHeaderFile(filename):
        basename = os.path.splitext(filename)[0]
        for extension in SOURCE_EXTENSIONS:
            replacement_file = basename + extension
            if os.path.exists(replacement_file):
                compilation_info = database.GetCompilationInfoForFile(replacement_file)
                if compilation_info.compiler_flags_:
                    return compilation_info
        return None
    return database.GetCompilationInfoForFile(filename)


# This is the entry point; this function is called by ycmd to produce flags for
# a file.
def FlagsForFile(filename, **kwargs):
    if not database:
        return {
            "flags": flags,
            "include_paths_relative_to_dir": DirectoryOfThisScript(),
        }

    compilation_info = GetCompilationInfoForFile(filename)
    if not compilation_info:
        return None

    # Bear in mind that compilation_info.compiler_flags_ does NOT return a
    # python list, but a "list-like" StringVec object.
    return {
        "flags": list(compilation_info.compiler_flags_),
        "include_paths_relative_to_dir": compilation_info.compiler_working_dir_,
    }
